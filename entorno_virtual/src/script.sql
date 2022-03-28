create table informacionGeneral(
  	cod_loc INT PRIMARY KEY,
 	idprovincia INT,
	iddepartamento INT,
	categoria VARCHAR,
	provincia VARCHAR,
 	localidad VARCHAR,
	nombre VARCHAR,
	direccion VARCHAR,
	cp VARCHAR, 
	telefono INT, 
	mail VARCHAR, 
	web VARCHAR,
	fecha_de_creacion DATE
);

create table registros_totales (
	fuente VARCHAR PRIMARY KEY,
	cantidad_de_registros_totales INT,
	fecha_de_creacion DATE
);

create table datos_cines(
	provincia VARCHAR PRIMARY KEY,
	pantallas INT,
	butacas INT,
	espacio_incaa INT,
	fecha_de_creacion DATE
);
