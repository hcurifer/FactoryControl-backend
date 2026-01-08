-- script_plantilla.sql

BEGIN;

-- INSERTAR DATOS FICTICIOS

-- USUARIOS table usuarios

INSERT INTO usuarios (
    numero_empresa,
    nombre,
    apellidos,
    correo,
    contrasena_hash,
    rol,
    estado_disponible,
    imagen
) VALUES
-- hash de password 1001
('1001', 'Jose', 'Martinez Lopez', 'jose.martinez@factorycontrol.com',
 '$2b$12$nyr4eRdSxxc1whpTjqz8G.TOyGhz/p10fLwRd/6QXI1ORiE63KLnO',
 'tecnico', false, 'Jose.png'),
-- hash de password 1002
('1002', 'Carlos', 'Gomez Ruiz', 'carlos.gomez@factorycontrol.com',
 '$2b$12$9LjScBkgxotvExoYD.GbsOshXPJBIDKMISIV8Mjw87DnQ6uTgkr7i',
 'tecnico', false, 'Carlos.png'),
-- hash de password 1003
('1003', 'Laura', 'Sanchez Ortega', 'laura.sanchez@factorycontrol.com',
 '$2b$12$9n4sLro6Af5IGuJThdb7mO.b85f/Bq/Bk82N5nHIpWGpZ5Ky2Z9bC',
 'tecnico', false, 'Laura.png'),
-- hash de password 1234
('1004', 'David', 'Fernandez Gil', 'david.fernandez@factorycontrol.com',
 '$2b$12$MdgDcJ3WjpAjWX7LUGlIm.9Ppt765hhNFfsx/miFNs5qL2jFDnsUa',
 'tecnico', false, 'David.png'),
-- hash de password 1234
('1005', 'Ana', 'Moreno Diaz', 'ana.moreno@factorycontrol.com',
 '$2b$12$MdgDcJ3WjpAjWX7LUGlIm.9Ppt765hhNFfsx/miFNs5qL2jFDnsUa',
 'tecnico', false, 'Ana.png'),
-- hash de password 9001
('9001', 'Miguel', 'Navarro Perez', 'miguel.navarro@factorycontrol.com',
 '$2b$12$YynVN8QBL5MUEvKtaYT4Hu7.dt1RfZB9JL/uzw2GcjQt1RlqKm9yG',
 'mando', false, 'Miguel.png'),
-- hash de password 9002
('9002', 'Raquel', 'Iglesias Soto', 'raquel.iglesias@factorycontrol.com',
 '$2b$12$NKt9T5bznn.g0pzUcHhaJeuCVUp10uTa43ULkGglqYwRTDln576cm',
 'mando', false, 'Raquel.png'),
-- hash de password 9003
('9003', 'Javier', 'Hernandez Vega', 'javier.hernandez@factorycontrol.com',
 '$2b$12$MKhkVfcNcK.UWd1wNkEW6OX2YRR7hv58ekschk4t0jkP5NTKyaAze',
 'mando', false, 'Javier.png'),
 -- hash de password 1234
('9004', 'Patricia', 'Romero Cano', 'patricia.romero@factorycontrol.com',
 '$2b$12$MdgDcJ3WjpAjWX7LUGlIm.9Ppt765hhNFfsx/miFNs5qL2jFDnsUa',
 'mando', false, 'Patricia.png'),
-- hash de password 1234
('9005', 'Alberto', 'Torres Molina', 'alberto.torres@factorycontrol.com',
 '$2b$12$MdgDcJ3WjpAjWX7LUGlIm.9Ppt765hhNFfsx/miFNs5qL2jFDnsUa',
 'mando', false, 'Alberto.png');


-- MAQUINAS table maquinas

INSERT INTO maquinas (
    nombre,
    codigo_maquina,
    ubicacion,
    estado,
    alarma_activa,
    descripcion,
    imagen
) VALUES
('Taladro Industrial', 'MAQ-TAL-001', 'Linea 1 - Zona A',
 'disponible', false,
 'Taladro industrial para mecanizado de piezas metálicas',
 'Taladro Industrial.png'),

('Prensa Hidraulica', 'MAQ-PRE-002', 'Linea 1 - Zona B',
 'disponible', false,
 'Prensa hidráulica de alta presión',
 'Prensa Hidraulica.png'),

('Cinta Transportadora', 'MAQ-CIN-003', 'Linea 2 - Zona A',
 'disponible', false,
 'Cinta transportadora de piezas entre estaciones',
 'Cinta Transportadora.png'),

('Robot Soldadura', 'MAQ-ROB-004', 'Linea 2 - Zona C',
 'disponible', false,
 'Robot automático de soldadura',
 'Robot Soldadura.png'),

('Compresor Aire', 'MAQ-COM-005', 'Sala Tecnica',
 'disponible', false,
 'Compresor principal de aire industrial',
 'Compresor Aire.png'),

('Torno CNC', 'MAQ-TOR-006', 'Linea 3 - Zona A',
 'disponible', false,
 'Torno CNC de precisión',
 'Torno CNC.png'),

('Fresadora', 'MAQ-FRE-007', 'Linea 3 - Zona B',
 'disponible', false,
 'Fresadora industrial para mecanizado',
 'Fresadora.png'),

('Horno Industrial', 'MAQ-HOR-008', 'Linea 4 - Zona A',
 'disponible', false,
 'Horno industrial de tratamiento térmico',
 'Horno Industrial.png'),

('Elevador Hidraulico', 'MAQ-ELE-009', 'Zona Mantenimiento',
 'disponible', false,
 'Elevador hidráulico para mantenimiento',
 'Elevador Hidraulico.png'),

('Pulidora Automatizada', 'MAQ-PUL-010', 'Linea 4 - Zona B',
 'disponible', false,
 'Pulidora automática de acabado',
 'Pulidora Automatizada.png');

 -- AVERIAS table averias_urgentes

INSERT INTO averias_urgentes (
    id_maquina,
    id_usuario_asignado,
    id_usuario_creador,
    descripcion,
    estado,
    prioridad,
    fecha_cierre,
    motivo_no_realizada
) VALUES
-- Avería pendiente
(1, 1, 6,
 'Vibración anormal detectada durante operación',
 'pendiente',
 'alta',
 NULL,
 NULL),

-- Avería completada
(2, 2, 6,
 'Fuga hidráulica leve en manguera',
 'completada',
 'media',
 NOW(),
 NULL),

-- Avería pendiente
(3, 3, 7,
 'Parada intermitente de la cinta transportadora',
 'pendiente',
 'alta',
 NULL,
 NULL),

-- Avería no realizada
(4, 3, 8,
 'Error de calibración en robot de soldadura',
 'no_realizada',
 'media',
 NOW(),
 'Se requiere intervención externa especializada'),

-- Avería completada
(5, 4, 6,
 'Presión insuficiente en compresor',
 'completada',
 'alta',
 NOW(),
 NULL),

-- Avería pendiente
(6, 5, 7,
 'Desgaste excesivo en herramienta del torno',
 'pendiente',
 'baja',
 NULL,
 NULL),

-- Avería completada
(7, 1, 6,
 'Ruido anómalo en cabezal de fresadora',
 'completada',
 'media',
 NOW(),
 NULL),

-- Avería no realizada
(8, 2, 9,
 'Temperatura fuera de rango en horno industrial',
 'no_realizada',
 'alta',
 NOW(),
 'Producción no autorizó la parada de la máquina'),

-- Avería pendiente
(9, 4, 10,
 'Elevador hidráulico no mantiene altura',
 'pendiente',
 'alta',
 NULL,
 NULL),

-- Avería completada
(10, 3, 6,
 'Pulido irregular detectado en ciclo automático',
 'completada',
 'baja',
 NOW(),
 NULL);

-- GAMAS DE PREVENTIVO table gamas_preventivo

INSERT INTO gamas_preventivo (
    nombre,
    descripcion,
    activa
) VALUES
('Mantenimiento Diario Básico',
 'Revisión visual general, limpieza superficial y comprobación de ruidos anómalos',
 true),

('Engrase Semanal',
 'Engrase de componentes móviles según especificaciones del fabricante',
 true),

('Revisión Mensual Mecánica',
 'Comprobación de holguras, aprietes y desgaste mecánico',
 true),

('Revisión Eléctrica Mensual',
 'Inspección de cableado, sensores y cuadros eléctricos',
 true),

('Mantenimiento Trimestral Preventivo',
 'Revisión completa de elementos críticos y ajuste general',
 true),

('Chequeo de Seguridad',
 'Verificación de paradas de emergencia, resguardos y sistemas de seguridad',
 true),

('Calibración de Sensores',
 'Calibración de sensores de posición, temperatura y presión',
 true),

('Mantenimiento Semestral Profundo',
 'Desmontaje parcial, limpieza profunda y sustitución de elementos de desgaste',
 true),

('Inspección de Sistemas Hidráulicos',
 'Revisión de mangueras, presión, válvulas y posibles fugas',
 true),

('Gama Obsoleta en Revisión',
 'Gama desactivada pendiente de redefinición',
 false);

-- CATALOGO GAMAS table tareas_catalogo_gamas

INSERT INTO tareas_catalogo_gamas (
    id_gama,
    nombre_tarea,
    descripcion,
    duracion_horas,
    orden
) VALUES
-- GAMA 1: Mantenimiento Diario Básico
(1, 'Inspección visual general',
 'Revisión visual del estado general de la máquina',
 0.25, 1),

(1, 'Limpieza superficial',
 'Eliminación de polvo, virutas y residuos visibles',
 0.50, 2),

(1, 'Comprobación de ruidos',
 'Detección de ruidos anómalos durante funcionamiento',
 0.25, 3),

-- GAMA 2: Engrase Semanal
(2, 'Engrase de guías',
 'Aplicación de lubricante en guías y carriles',
 0.50, 1),

(2, 'Engrase de rodamientos',
 'Lubricación de rodamientos principales',
 0.75, 2),

(2, 'Comprobación de niveles',
 'Verificación de niveles de aceite y lubricante',
 0.25, 3),

-- GAMA 3: Revisión Mensual Mecánica
(3, 'Revisión de holguras',
 'Comprobación de holguras mecánicas en ejes',
 1.00, 1),

(3, 'Ajuste de tornillería',
 'Reapriete de tornillos y fijaciones críticas',
 0.75, 2),

(3, 'Inspección de desgaste',
 'Evaluación del desgaste de piezas móviles',
 1.00, 3),

-- GAMA 4: Revisión Eléctrica Mensual
(4, 'Inspección de cableado',
 'Revisión visual del cableado eléctrico',
 0.75, 1),

(4, 'Comprobación de sensores',
 'Verificación de funcionamiento de sensores',
 0.50, 2),

(4, 'Revisión de cuadro eléctrico',
 'Inspección de protecciones y conexiones',
 1.00, 3),

(4, 'Prueba de paradas de emergencia',
 'Verificación de paradas de seguridad',
 0.50, 4);

-- TAREAS ASIGNADAS table tareas_catalogo_preventivo

INSERT INTO tareas_catalogo_preventivo (
    id_gama,
    id_maquina,
    id_usuario,
    id_tarea_catalogo_gamas,
    estado,
    fecha_asignada,
    fecha_completado,
    observaciones,
    duracion_horas
) VALUES
-- GAMA 1 – Mantenimiento Diario Básico (Máquina 1)
(1, 1, 1, 1, 'completada', CURRENT_DATE, NOW(),
 'Sin anomalías detectadas', 0.25),

(1, 1, 1, 2, 'completada', CURRENT_DATE, NOW(),
 'Limpieza realizada correctamente', 0.50),

(1, 1, 1, 3, 'pendiente', CURRENT_DATE, NULL,
 NULL, 0.25),

-- GAMA 2 – Engrase Semanal (Máquina 2)
(2, 2, 2, 4, 'completada', CURRENT_DATE, NOW(),
 'Engrase correcto', 0.50),

(2, 2, 2, 5, 'pendiente', CURRENT_DATE, NULL,
 NULL, 0.75),

(2, 2, 2, 6, 'pendiente', CURRENT_DATE, NULL,
 NULL, 0.25),

-- GAMA 3 – Revisión Mensual Mecánica (Máquina 6)
(3, 6, 3, 7, 'completada', CURRENT_DATE, NOW(),
 'Ligera holgura corregida', 1.00),

(3, 6, 3, 8, 'completada', CURRENT_DATE, NOW(),
 'Tornillería ajustada', 0.75),

(3, 6, 3, 9, 'pendiente', CURRENT_DATE, NULL,
 NULL, 1.00),

-- GAMA 4 – Revisión Eléctrica Mensual (Máquina 4)
(4, 4, 4, 10, 'completada', CURRENT_DATE, NOW(),
 'Cableado en buen estado', 0.75),

(4, 4, 4, 11, 'pendiente', CURRENT_DATE, NULL,
 NULL, 0.50),

(4, 4, 4, 12, 'pendiente', CURRENT_DATE, NULL,
 NULL, 1.00);

-- NOTIFICACIONES table notificaciones

INSERT INTO notificaciones (
    id_averia,
    id_tarea,
    id_maquina,
    id_usuario_origen,
    id_usuario_destino,
    tipo,
    contenido_resumen,
    asunto,
    fecha_envio
) VALUES
-- Avería creada
(1, NULL, 1, 1, 6,
 'averia_creada',
 'Se ha detectado una vibración anormal en la máquina.',
 'Nueva avería registrada',
 NOW()),

-- Avería completada
(2, NULL, 2, 2, 6,
 'averia_completada',
 'La fuga hidráulica ha sido reparada correctamente.',
 'Avería completada',
 NOW()),

-- Avería no realizada
(4, NULL, 4, 3, 8,
 'averia_no_realizada',
 'No ha sido posible completar la avería por necesidad de soporte externo.',
 'Avería no realizada',
 NOW()),

-- Avería crítica pendiente
(9, NULL, 9, NULL, 10,
 'averia_pendiente',
 'El elevador hidráulico no mantiene la altura. Avería sin técnico asignado.',
 'Avería urgente pendiente',
 NOW()),

-- Preventivo completado
(NULL, 1, 1, 1, 6,
 'preventivo_completado',
 'Se ha completado la inspección visual general sin incidencias.',
 'Preventivo completado',
 NOW()),

-- Preventivo completado
(NULL, 4, 2, 2, 6,
 'preventivo_completado',
 'Engrase de guías realizado correctamente.',
 'Preventivo completado',
 NOW()),

-- Preventivo pendiente detectado
(NULL, 5, 2, NULL, 6,
 'preventivo_pendiente',
 'Existen tareas de engrase pendientes de ejecución.',
 'Preventivo pendiente',
 NOW()),

-- Preventivo con observaciones
(NULL, 7, 6, 3, 7,
 'preventivo_observacion',
 'Durante la revisión mecánica se detectó ligera holgura corregida.',
 'Observación en preventivo',
 NOW()),

-- Revisión eléctrica pendiente
(NULL, 11, 4, NULL, 8,
 'preventivo_pendiente',
 'Queda pendiente la comprobación de sensores eléctricos.',
 'Tarea preventiva pendiente',
 NOW()),

-- Aviso general de sistema
(NULL, NULL, 5, 6, 1,
 'aviso_sistema',
 'Se recomienda revisar el estado general del compresor esta semana.',
 'Aviso de mantenimiento',
 NOW());

-- FICHAJES table fichajes

INSERT INTO fichajes (
    id_usuario,
    fecha,
    hora_entrada,
    hora_salida,
    comentario
) VALUES
-- Técnico fichado y ya salido
(1, CURRENT_DATE, '06:00', '14:00',
 'Turno de mañana completado'),

-- Técnico fichado y ya salido
(2, CURRENT_DATE, '06:05', '14:10',
 'Revisión de preventivos'),

-- Técnico con fichaje abierto (TRABAJANDO)
(3, CURRENT_DATE, '14:00', NULL,
 'Turno de tarde en curso'),

-- Técnico con fichaje abierto (TRABAJANDO)
(4, CURRENT_DATE, '14:10', NULL,
 NULL),

-- Técnico fichado y ya salido
(5, CURRENT_DATE, '22:00', '06:00',
 'Turno de noche'),

-- Mando fichado
(6, CURRENT_DATE, '08:00', '16:00',
 'Supervisión general'),

-- Mando con fichaje abierto
(7, CURRENT_DATE, '08:30', NULL,
 'Reuniones y seguimiento'),

-- Mando fichado
(8, CURRENT_DATE, '09:00', '17:00',
 NULL),

-- Mando fichado
(9, CURRENT_DATE, '07:45', '15:30',
 'Revisión de incidencias'),

-- Mando con fichaje abierto
(10, CURRENT_DATE, '10:00', NULL,
 'Guardia de incidencias');

-- PETICIONES DE DIA table peticiones_dia

INSERT INTO peticiones_dia (
    id_usuario,
    tipo_peticion,
    comentario,
    estado,
    fecha_resolucion
) VALUES
-- Técnico – pendiente
(1, 'dia_libre',
 'Solicitud de día libre por asuntos personales',
 'pendiente',
 NULL),

-- Técnico – aprobada
(2, 'dia_libre',
 'Solicitud de día libre para gestión médica',
 'aprobada',
 CURRENT_DATE),

-- Técnico – rechazada
(3, 'asuntos_propios',
 'Necesito ausentarme por motivos personales',
 'rechazada',
 CURRENT_DATE),

-- Técnico – pendiente
(4, 'licencia',
 'Solicitud de licencia por formación técnica',
 'pendiente',
 NULL),

-- Técnico – aprobada
(5, 'dia_libre',
 'Solicitud de día libre con antelación',
 'aprobada',
 CURRENT_DATE),

-- Mando – pendiente
(6, 'asuntos_propios',
 'Ausencia por gestión administrativa',
 'pendiente',
 NULL),

-- Mando – aprobada
(7, 'dia_libre',
 'Vacaciones día suelto',
 'aprobada',
 CURRENT_DATE),

-- Mando – rechazada
(8, 'licencia',
 'Permiso no compatible con planificación',
 'rechazada',
 CURRENT_DATE),

-- Mando – pendiente
(9, 'dia_libre',
 'Solicitud de día libre',
 'pendiente',
 NULL),

-- Mando – aprobada
(10, 'asuntos_propios',
 'Gestión externa autorizada',
 'aprobada',
 CURRENT_DATE);


COMMIT;
