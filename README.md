# CREAR FACTURAS
Proyecto para crear facturas prorateadas solicitadas por CONATEL

# ALGORITMO
- Descargar de MW el reporte de los clientes (SOLO ACTIVOS)
- Buscar la ultima factura de cada cliente y sacar la fecha de emision de la ultima factura del servicio
- Crear nueva factura a partir del dia siguiente de la fecha de vencimiento hasta el 30 de Abril de 2025
- A partir del 1 de Mayo se factura normal

# INSTALACION
- Instalar dependencias        
        
        sudo apt update
        sudo apt install python3-dev libmariadb-dev

- Crear usuario en BD para acceder desde afuera

      mysql -u root -p
      CREATE USER 'MIUSER'@'%' IDENTIFIED BY 'MIPASSWORD';
      GRANT SELECT, UPDATE, INSERT, DELETE ON Mikrowisp6.* TO 'MIUSER'@'%';
      FLUSH PRIVILEGES;
      EXIT;

# USO
