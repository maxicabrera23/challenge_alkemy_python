from sqlalchemy import create_engine , select , exists, table
import psycopg2
import os
from decouple import config

#variables de entorno importadas del archivo .env
host = config('PS_HOST')
puerto = config('PS_PORT')
usuario = config('PS_USER')
clave = config('PS_PASSWORD')
base = config('PS_DB')

#genero la conexion con la base
engine = create_engine('postgresql+psycopg2://'+ usuario +':'+ clave +'@'+ host +':'+ puerto +'/'+ base +'')

#preparo el nombre y la ruta del script
nombreScript = ('script.sql')
ruta = os.getcwd() + "/src"
rutaNombre = os.path.join(ruta , nombreScript)


#leo el archivo 
lectura = open(rutaNombre , 'r').read() 

#genero una ecxepcion para correr el script si sale bien escribe satisfactorio sino imprime error
try:
    with engine.connect() as conn:
        conn.execute(lectura)
        print(f'Se ejecuto sactifactoriamente el script{nombreScript}')

except Exception as err:
    print(f'No se pudo ejecutar el script {nombreScript}')
    print(f'Por la razon:\n{err}')


