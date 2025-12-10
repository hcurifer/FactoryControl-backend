-- ______________________________
--  TABLA USUARIOS
-- ______________________________

CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    numero_empresa VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contrasena_hash TEXT NOT NULL,
    rol VARCHAR(20) NOT NULL CHECK (rol IN ('tecnico','mando')),
    estado_disponible BOOLEAN DEFAULT FALSE,
    imagen TEXT,
    fecha_alta DATE DEFAULT CURRENT_DATE,
    fecha_baja DATE
);

-- ______________________________
--  TABLA MAQUINAS
-- ______________________________

CREATE TABLE maquinas (
    id_maquina SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    codigo_maquina VARCHAR(50) UNIQUE NOT NULL,
    ubicacion VARCHAR(150),
    estado VARCHAR(30) NOT NULL CHECK (estado IN ('disponible','parada','pendiente_preventivo')),
    alarma_activa BOOLEAN DEFAULT FALSE,
    descripcion TEXT,
    fecha_alta DATE DEFAULT CURRENT_DATE,
    fecha_baja DATE,
    imagen TEXT
);

-- ______________________________
--  TABLA AVERIAS URGENTES
-- ______________________________

CREATE TABLE averias_urgentes (
    id_averia SERIAL PRIMARY KEY,
    id_maquina INT NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    id_usuario_asignado INT REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    id_usuario_creador INT REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('pendiente','completada','no_realizada')),
    prioridad VARCHAR(20), 
    fecha_cierre TIMESTAMP,
    motivo_no_realizada TEXT
);

-- ______________________________
--  TABLA GAMAS DE PREVENTIVO
-- ______________________________

CREATE TABLE gamas_preventivo (
    id_gama SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE
);

-- ______________________________
--  TABLA TAREAS DEL CATALOGO PARA GAMAS
-- ______________________________

CREATE TABLE tareas_catalogo_gamas (
    id_tarea_catalogo_gamas SERIAL PRIMARY KEY,
    id_gama INT REFERENCES gamas_preventivo(id_gama) ON DELETE CASCADE,
    nombre_tarea VARCHAR(150) NOT NULL,
    descripcion TEXT,
    duracion_horas NUMERIC(4,2) NOT NULL,
    orden INT NOT NULL
);


-- ______________________________
--  TABLA TAREAS ASIGNADAS PARA PREVENTIVO
-- ______________________________

CREATE TABLE tareas_catalogo_preventivo (
    id_tarea_asignada SERIAL PRIMARY KEY,
    id_gama INT NOT NULL REFERENCES gamas_preventivo(id_gama) ON DELETE CASCADE,
    id_maquina INT NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    id_tarea_catalogo_gamas INT REFERENCES tareas_catalogo_gamas(id_tarea_catalogo_gamas) ON DELETE SET NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente','completada')),
    fecha_asignada DATE DEFAULT CURRENT_DATE,
    fecha_completado TIMESTAMP,
    observaciones TEXT,
    duracion_horas NUMERIC(4,2)
);

-- ______________________________
--  TABLA NOTIFICACIONES
-- ______________________________

CREATE TABLE notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_averia INT REFERENCES averias_urgentes(id_averia) ON DELETE SET NULL,
    id_tarea INT REFERENCES tareas_catalogo_preventivo(id_tarea_asignada) ON DELETE SET NULL,
    id_maquina INT NOT NULL REFERENCES maquinas(id_maquina) ON DELETE CASCADE,
    id_usuario_origen INT REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    id_usuario_destino INT REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    tipo VARCHAR(100) NOT NULL,
    contenido_resumen TEXT NOT NULL,
    asunto VARCHAR(150),
    fecha_envio TIMESTAMP DEFAULT NOW()
);

-- ______________________________
--  TABLA FICHAJES
-- ______________________________

CREATE TABLE fichajes (
    id_fichaje SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    fecha DATE DEFAULT CURRENT_DATE,
    hora_entrada TIME,
    hora_salida TIME,
    comentario TEXT
);

-- ______________________________
--  TABLA PETICIONES DE DIA
-- ______________________________

CREATE TABLE peticiones_dia (
    id_peticion SERIAL PRIMARY KEY,
    id_usuario INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    tipo_peticion VARCHAR(50) NOT NULL,
    comentario TEXT,
    estado VARCHAR(20) DEFAULT 'pendiente',
    fecha_resolucion DATE
);
