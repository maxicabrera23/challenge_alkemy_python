from sqlalchemy import create_engine
import psycopg2
import requests 
from datetime import datetime
import os
import pandas as pd
from sqlalchemy import case
from decouple import config
import unidecode

#se generan las variables de fecha para los nombres de los archivos
fecha=datetime.now()
mes=fecha.strftime('%Y-%B')
d_m_a=fecha.strftime('%d-%m-%Y')


#variables de los nombres de archivos
museos='museos/'+ mes 
cines='sala de cines/'+ mes 
bibliotecas='bibliotecas/'+ mes 
#"""
#comprobar si los directorios existen sino se crean
if not os.path.exists(museos):
    os.makedirs(museos)
    print ('se creo el directorio museos')


#cines
if not os.path.exists(cines):
    os.makedirs(cines)
    print ('se creo el directorio cines')


#bibliotecas
if not os.path.exists(bibliotecas):
    os.makedirs(bibliotecas)
    print ('se creo el directorio bibliotecas')


#guarda ls datos del archivo en la variable consulta
l_museos = config('link_museos')
l_cines = config('link_cines')
l_bibliotecas = config ('link_bibliotecas')


consulta_museos = requests.get(l_museos) 
consulta_cines = requests.get(l_cines)
consulta_bibliotecas = requests.get(l_bibliotecas)




#genera el archivo museo csv en la carpeta local correspondiente 
open(museos+'/museos-'+ d_m_a +'.csv', 'w', encoding='ISO-8859-1').write(consulta_museos.text)
open(cines+'/cines-'+d_m_a+'.csv','w' , encoding='ISO-8859-1').write(consulta_cines.text)
open(bibliotecas+'/bibliotecas-'+d_m_a+'.csv','w',encoding='ISO-8859-1').write(consulta_bibliotecas.text)
#"""
############################################################################################################################
#Procesamiento de datos

#traigo ubicacion de archivo
archivo_museos=os.getcwd()+'/'+museos+'/museos-'+ d_m_a +'.csv'
archivo_cines=os.getcwd()+'/'+cines+'/cines-'+d_m_a+'.csv'
archivo_bibliotecas=os.getcwd()+'/'+bibliotecas+'/bibliotecas-'+d_m_a+'.csv'

#genero un dataframe con todos los datos del archivo
df_museos=pd.read_csv(archivo_museos)
df_cines = pd.read_csv(archivo_cines)
df_bibliotecas=pd.read_csv(archivo_bibliotecas)


#saco acentos y mayusculas de las columnas
dataframes=[df_museos, df_cines, df_bibliotecas]
for data in dataframes:
    for columnas in data:
        valor=unidecode.unidecode(columnas.lower())
        data.rename(columns = {columnas:valor},inplace=True)


#########################################   tabla 1   ##################################################################
#funcion para traer los valores pedidos para la tabla 1 del dataframe
def extraer_datos(val1):
    buscar=['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 
        'localidad', 'nombre' ,'direccion','domicilio','cp', 'telefono', 'mail', 'web' ]
    resultado=[]
    for colums in val1:
        for x in range(0,len(buscar)):
            if (colums)==(buscar[x]):
                resultado.append(colums)
    
    #genero un dataframe con los valores pedidos para la tabla 1
    campos_requeridos=val1.loc[:,resultado]
    
    #renombro las columnas de los dataframes para que todas tengan el mismo nombre y poder concatenar
    campos_requeridos.columns=['cod_loc', 'idprovincia', 'iddepartamento', 'categoria', 'provincia', 
        'localidad', 'nombre' ,'direccion','cp', 'telefono', 'mail', 'web' ]
    
    return campos_requeridos




#seleccciono las columnas pedidas 
museos_mod=extraer_datos(df_museos)
cines_mod=extraer_datos(df_cines)
bibliotecas_mod=extraer_datos(df_bibliotecas)

#concateno los 3 dataframes para formar la tabla 1
df_union=pd.concat([museos_mod, cines_mod, bibliotecas_mod], axis=0)

#agrego la columna de fecha de creacion
df_union_fecha=df_union.assign(fecha_de_creacion=d_m_a)

#convierto valores nan en null
df_union_fecha=df_union_fecha.fillna('null')

###############################################  tabla 2   #########################################################
                                                #funciones

#funcion para extraer datos de funte
def traer_fuentes(val1, val2, val3):
    fuente_museos=val1[['fuente']]
    fuente_cines=val2[['fuente']]
    funte_bibliotecas=val3[['fuente']]

    df_union_funte=pd.concat([fuente_museos, fuente_cines, funte_bibliotecas], axis=0)
    return df_union_funte

def concatenar(val1,val2,val3):
        #cambio el nombe de columnas para concatenar
        val1.columns=['fuente','cantidad de registros totales']
        val2.columns=['fuente','cantidad de registros totales']
        val3.columns=['fuente','cantidad de registros totales']
        concatenado=pd.concat([val1,val2,val3])

        return concatenado
    

#cantidad total de registros por categoria
df_categorias=df_union_fecha.groupby(['categoria']).size().reset_index(name='cantidad_de_registros')

#traigo valores de fuente de los 3 archivos
df_fuentes=traer_fuentes(df_museos, df_cines, df_bibliotecas)

#cantidad total de registros por fuente
df_fuentes_conteo=df_fuentes.groupby(['fuente']).size().reset_index(name='cantidad_de_registros')


#agrupo por provincia y categoria
df_prov_cat=df_union_fecha.groupby(['provincia','categoria',]).size().reset_index(name='cantidad_de_registros')

#uno las columnas provincia y categoria
df_prov_cat['provincias_categorias']=df_prov_cat[['provincia','categoria']].apply(' - '.join,axis=1 )

#cantidad total de registros por provincia y categoria
df_provincias_categorias=df_prov_cat[['provincias_categorias','cantidad_de_registros']]

#concateno los 3 dataframes para la tabla 2
df_final=concatenar(df_categorias,df_fuentes_conteo,df_provincias_categorias)

#agrego columna fecha de creacion
df_final=df_final.assign(fecha_de_creacion=d_m_a)

##################################################### tabla 3 ##########################################################

#dataframe con datos tabla 3
df_datos_cines=df_cines[['provincia', 'pantallas', 'butacas','espacio_incaa' ]]

#convierto valores nan en null
df_datos_cines=df_datos_cines.fillna('0')

#remplazo los valores "si" para poder contarlos
df_datos_cines['espacio_incaa']=df_datos_cines['espacio_incaa'].str.replace('si','1' ,case=False)

#cambio el tipo de dato de la columna par poder sumar
df_datos_cines[['espacio_incaa']]=df_datos_cines[['espacio_incaa']].astype('int64')

#agrupo y sumo
df_agrupar=df_datos_cines.groupby(['provincia']).sum()

#agrego columna fecha de creacion
df_agrupar=df_agrupar.assign(fecha_de_creacion=d_m_a)


#Actualizacion de DB
#variables de entorno importadas del archivo .env
host = config('PS_HOST')
puerto = config('PS_PORT')
usuario = config('PS_USER')
clave = config('PS_PASSWORD')
base = config('PS_DB')

#genero la conexion con la base
engine = create_engine('postgresql+psycopg2://'+ usuario +':'+ clave +'@'+ host +':'+ puerto +'/'+ base +'')

#se pasan los datos a la tabla informaciongeneral
try:
    df_union_fecha.to_sql('informaciongeneral',engine,if_exists='replace', index=False)
    print(f'Se pasaron los datos a la tabla informaciongeneral correctamente')

except Exception as err:
    print(f'No se pasaron los datos a la tabla informaciongeneral')
    print(f'Por la razon:\n{err}')


#se pasan los datos a la tabla registros_totales
try:
    df_final.to_sql('registros_totales',engine,if_exists='replace', index=False)
    print(f'Se pasaron los datos a la tabla registros_totales correctamente')

except Exception as err:
    print(f'No se pasaron los datos a la tabla registros_totales')
    print(f'Por la razon:\n{err}')


#se pasan los datos a la tabla datos_cines
try:
    df_agrupar.to_sql('datos_cines',engine,if_exists='replace' )
    print(f'Se pasaron los datos a la tabla datos_cines correctamente')

except Exception as err:
    print(f'No se pasaron los datos a la tabla datos_cines')
    print(f'Por la razon:\n{err}')
