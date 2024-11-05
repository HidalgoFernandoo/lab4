import mysql.connector


def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host="localhost", user="root", password="root"
        )
        cursor = conexion.cursor()

        if crear_schema_tablas(cursor, conexion):

            conexion.database = "proyecto_final"

            if conexion.is_connected():
                print("Conexión exitosa a la base de datos")
            return conexion

        conexion.close()
        print("ocurrio un error con la conexion")

    except mysql.connector.Error as error:
        print(f"Error al conectarse: {error}")
        return None


def crear_schema_tablas(cursor, conexion):
    try:
        nombre_schema = "proyecto_final"

        # Verificar si el esquema existe
        cursor.execute(f"SHOW DATABASES LIKE '{nombre_schema}';")
        result = cursor.fetchone()

        if not result:
            cursor.execute(f"CREATE DATABASE {nombre_schema};")
            print(f"Base de datos '{nombre_schema}' creada exitosamente.")

            tabla_productos = """
            CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            marca VARCHAR(30) NOT NULL,
            categoria VARCHAR(30) NOT NULL, 
            precio_compra DECIMAL(10, 2) NOT NULL,
            precio_venta DECIMAL(10, 2) NOT NULL
            ) ENGINE=INNODB;
            """

            tabla_lotes = """
            CREATE TABLE IF NOT EXISTS lotes (
            lote_id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            producto_id INT NOT NULL,
            cantidad INT NOT NULL,
            fecha_vencimiento DATE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) 
            ) ENGINE=INNODB; 
            """
            # (ENGINE-INNODB;) Es el motor de almacenamiento Avanzado

            # Seleccionamos el nuevo schema
            conexion.database = nombre_schema

            # Crear la tabla en el nuevo esquema
            cursor.execute(tabla_productos)
            cursor.execute(tabla_lotes)
            print("Se creó una base de datos nueva.")

        return True

    except mysql.connector.Error as err:
        print(f"Error al crear el esquema o la tabla: {err}")
        return False


# Conectar a la base de datos
conexion = conectar_db()
