# imagen base de python
#FROM python:3.8-slim
FROM python:3.9.1

# habilitar los mensajes por consola
ENV PYTHONUNBUFFERED=1

# definir la ubicacion de nuestros archivos
WORKDIR /app

# instalar dependencias
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# copiar archivos del app a la imagen
COPY . .

# exponer el puerto que utiliza el sistema
EXPOSE 9098

# lanzar la aplicación
CMD python3 main.py