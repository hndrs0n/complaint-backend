# Usar una imagen base de Python
FROM python:3.11.4-alpine

# Establecer una variable de entorno para asegurarse de que la salida de Python se envíe directamente al terminal
ENV PYTHONUNBUFFERED 1

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
