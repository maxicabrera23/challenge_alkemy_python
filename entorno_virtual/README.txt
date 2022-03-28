1° Guardar la carpeta "src" y los archivos .env y config.txt en una carpeta local,
dentro de dicha carpeta generar un entorno virtual y activarlo, "ESTE SERA EL DIRECTORIO RAIZ".

2° Ejecutar el comando pip install -r ruta_archivo/config.txt para descargar las librerias necesarias para que el proyecto funcione correctamente.

3° Configure la conexion a la base de datos en el archivo ".env".

4° Desde el DIRECTORIO RAIZ ejecute el script "estructura_db.py" (EJ: python3 src/estructura_db.py) para crear las tablas en la base de datos.

5° Desde el DIRECTORIO RAIZ ejecute el script "main.py" (EJ: python3 src/main.py)este script descarga los archivos,los procesa y envia la informacion requerida a las tablas.

6° Comprobar que en el diectorio raiz esten las carpetas con los archivos ".csv" y que las tablas contengan la informacion requerida.
