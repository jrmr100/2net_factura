#!/bin/bash

# Reemplaza con el nombre de usuario deseado
USERNAME="jmonroy"

# Reemplaza con la contraseña deseada
PASSWORD="Jmon**9911"

# Reemplaza con el nombre de la base de datos a la que se dará acceso
DATABASE_NAME="Mikrowisp6"

# Comando para acceder a la consola de MariaDB como usuario root (o un usuario con privilegios)
# Es posible que se te solicite la contraseña de root
mysql -u root -p

# Dentro de la consola de MariaDB, ejecuta los siguientes comandos:

# 1. Crear el nuevo usuario con permiso para acceder desde cualquier host (%)
CREATE USER '$USERNAME'@'%' IDENTIFIED BY '$PASSWORD';

# 2. Otorgar permisos SELECT (ver tablas) y UPDATE, INSERT, DELETE (editar) en la base de datos especificada
GRANT SELECT, UPDATE, INSERT, DELETE ON $DATABASE_NAME.* TO '$USERNAME'@'%';

# 3. Aplicar los cambios de permisos
FLUSH PRIVILEGES;

# 4. Salir de la consola de MariaDB
EXIT;

echo "Usuario '$USERNAME' creado con permisos para ver y editar la base de datos '$DATABASE_NAME' desde cualquier host."
echo "Recuerda reemplazar 'nuevo_usuario', 'contraseña_segura' y 'nombre_de_la_base_de_datos' con tus valores."
echo "Asegúrate de configurar correctamente el firewall de tu servidor para permitir conexiones al puerto de MariaDB (por defecto 3306) desde las IPs deseadas."