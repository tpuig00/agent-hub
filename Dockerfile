# Imagen base con Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /code

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY app ./app

# Puerto de la aplicación
EXPOSE 8000

# Iniciar el servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]