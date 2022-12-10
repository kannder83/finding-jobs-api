# finding jobs API

Finding Work API - Technical Proof

Esta API esta desarrollada con:

- FastAPI

- Docker

- Postgres

## Programs

Se requiere teneer instalado los siguientes programas:

- Python3

- Docker

## Enviroment File

```bash
# Utilizar el comando para copiar el template al archivo .env
cp env.template .env
```

## Build Docker

Para crear el contenedor, ejecutarlo y crear las tablas de la base de datos.

```bash
# Crea el contenedor:
docker-compose -f Developer.yml build

# Inicializa el contenedor:
docker-compose -f Developer.yml up -d

# Ingresar al contenedor:
docker exec -it dev_api_finding_jobs bash

# Ejecutar achivo para crear las tablas en la base de datos y copiar los datos a la BD:
python3 create_tables.py

# Para salir del contenedor
exit
```

## Acceder a la API

Para ingresar a la aplicación dar clic en el link.

[localhost:8000](http://localhost:8000/)

## Creación y consulta de User

1. Se debe crear un usuario desde el endpoint:

![Alt text](./documentation/img/image_01.png "image 01")

El JSON para crearlo es:

```json
{
  "FirstName": "Daniela",
  "LastName": "Perez",
  "Email": "example1@xyz.com",
  "YearsPreviousExperience": 2
}
```

2. Para agregar la experiencia al usuario se utiliza el endpoint:

![Alt text](./documentation/img/image_02.png "image 02")

Se requiere conocer el UserId, luego usando el JSON se agega la experiencia:

UserID: 5f318a0d-4d33-4f28-b725-c4566610aaa4

```json
{
  "SkillName": "react",
  "YearsOfExperience": 2
}
```

Para confirma que la experiencia fue agregada al usuario utilizar el endpoint de consulta por UserId:

![Alt text](./documentation/img/image_03.png "image 03")

Se tiene un JSON de respuesta como el siguiente:

```json
{
  "FirstName": "Daniela",
  "LastName": "Perez",
  "Email": "example1@xyz.com",
  "YearsPreviousExperience": 2,
  "UserId": "5f318a0d-4d33-4f28-b725-c4566610aaa4",
  "Skills": [
    {
      "SkillName": "python",
      "YearsOfExperience": 1,
      "SkillId": 1
    },
    {
      "SkillName": "react",
      "YearsOfExperience": 2,
      "SkillId": 2
    }
  ]
}
```

Se puede obtener información de todos los usuarios consultando el endpoint:

![Alt text](./documentation/img/image_04.png "image 04")

## Borrar la información

```bash
# Borra toda la configuración:
docker-compose -f Developer.yml down --remove-orphans -v
```
