from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# Reemplaza estos valores con tus credenciales de MySQL
MYSQL_USER = "root"
MYSQL_PASSWORD = "123"
MYSQL_HOST = "127.0.0.1"  # o la IP de tu servidor MySQL
MYSQL_PORT = "3306" 
MYSQL_DATABASE = "bodegon4"

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Crear una instancia de motor para la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Crear una clase de sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base para la creación de modelos de datos
Base = declarative_base()

# Crear todas las tablas
Base.metadata.create_all(bind=engine)


# Test de conexión
if __name__ == "__main__":
    try:
        # Intenta crear una sesión y cerrar la conexión
        db = SessionLocal()
        print("Conexión exitosa a la base de datos!")
        db.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")