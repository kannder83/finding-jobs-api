# finding jobs API

Finding Work API - Technical Proof

## Programs

- Python3

- Docker

## Enviroment File

```bash
# Utilizar el comando para copiar el template al archivo .env
cp env.template .env
```

## Build Docker

```bash
# Crea el contenedor:
docker-compose -f Developer.yml build

# Inicializa el contenedor:
docker-compose -f Developer.yml up -d

# Ingresar al contenedor:
docker exec -it dev_api_finding_jobs bash

# Ejecutar achivo para crear las tablas en la base de datos y copiar los datos a la BD:
python3 create_tables.py

exit
```

## Acceder a la API

[localhost:8000](http://localhost:8000/)

## Borrar la información

```bash
# Borra toda la configuración:
docker-compose -f Developer.yml down --remove-orphans -v
```
