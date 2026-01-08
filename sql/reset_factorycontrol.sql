-- script reset_factorycontrol.sql

BEGIN;

-- DESACTIVAR RESTRICCIONES

SET session_replication_role = replica;

-- LIMPIEZA DE TABLAS
-- (orden inverso a dependencias)

TRUNCATE TABLE
    notificaciones,
    peticiones_dia,
    fichajes,
    tareas_catalogo_preventivo,
    tareas_catalogo_gamas,
    averias_urgentes,
    gamas_preventivo,
    maquinas,
    usuarios
RESTART IDENTITY
CASCADE;

-- REACTIVAR RESTRICCIONES

SET session_replication_role = DEFAULT;

COMMIT;