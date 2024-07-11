
"EJEMPLO DE LA BD DEL PROYECTO"



-- Crear la base de datos
CREATE DATABASE mysong;

-- Conectar a la base de datos
\d mysong;

-- Crear la tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contraseña VARCHAR(100) NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL
);

-- Crear la tabla de canciones
CREATE TABLE canciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    artista VARCHAR(100) NOT NULL,
    album VARCHAR(100),
    archivo_mp3 VARCHAR(255) NOT NULL,
    likes INT DEFAULT 0
);

-- Crear la tabla de listas de reproducción
CREATE TABLE listas_reproduccion (
    id SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);

-- Crear la tabla de relaciones entre canciones y listas de reproducción
CREATE TABLE canciones_en_lista (
    id_cancion INT NOT NULL,
    id_lista INT NOT NULL,
    FOREIGN KEY (id_cancion) REFERENCES canciones(id),
    FOREIGN KEY (id_lista) REFERENCES listas_reproduccion(id),
    PRIMARY KEY (id_cancion, id_lista)
);

-- Conectar a la base de datos
\c mysong;

-- Añadir el campo 'data' de tipo BYTEA a la tabla 'canciones'
ALTER TABLE canciones ADD COLUMN data BYTEA;

-- Añadir la clave foránea 'usuario_id' a la tabla 'canciones'
ALTER TABLE canciones ADD COLUMN usuario_id INT;
ALTER TABLE canciones ADD CONSTRAINT fk_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id);
ALTER TABLE canciones ALTER COLUMN data TYPE bytea USING data::bytea;


ALTER TABLE canciones
ALTER COLUMN data TYPE bytea
USING data::bytea;

ALTER TABLE canciones
ALTER COLUMN data SET DATA TYPE bytea
USING data::bytea;



-- Primero, eliminamos la columna data
ALTER TABLE canciones DROP COLUMN if EXISTS data;

-- Luego, agregamos la columna data nuevamente con el tipo bytea
ALTER TABLE canciones ADD COLUMN data bytea;


SHOW ALL;

select * from canciones where id=17;

SET default_transaction_isolation TO 'SERIALIZABLE';
