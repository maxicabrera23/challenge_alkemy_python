from itsdangerous import encoding
import requests 
from datetime import datetime
import os

#se generan as variables de fecha para los nombres de los archivos
fecha = datetime.now()
mes=fecha.strftime('%Y-%B')
d_m_a=fecha.strftime('%d-%m-%Y')


#variables de los nombres de archivos
museos='museos/'+ mes 
cines='sala de cines/'+ mes 
bibliotecas='bibliotecas/'+ mes 

#comprobar si los directorios existen sino se crean
if not os.path.exists(museos):
    os.makedirs(museos)
    print ('se creo el directorio de museos porque no existia')

#cines
if not os.path.exists(cines):
    os.makedirs(cines)
    print ('se creo el directorio de cines porque no existia')

#bibliotecas
if not os.path.exists(bibliotecas):
    os.makedirs(bibliotecas)
    print ('se creo el directorio de bibliotecas porque no existia')


#guarda ls datos del archivo en la variable consulta
consulta_museos = requests.get('https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museo.csv') 

consulta_cines = requests.get('https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv')

consulta_bilbiotecas = requests.get('https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv')


#genera el archivo museo csv en la carpeta museos 
open(museos+'/museos-'+ d_m_a +'.csv', 'w', encoding='ISO-8859-1').write(consulta_museos.text)
open(cines+'/cines-'+d_m_a+'.csv','w' , encoding='ISO-8859-1').write(consulta_cines.text)
open(bibliotecas+'/bibliotecas'+d_m_a+'.csv','w',encoding='ISO-8859-1').write(consulta_bibliotecas.text)

#mostrar = consulta.text
#print (consulta.encoding)
