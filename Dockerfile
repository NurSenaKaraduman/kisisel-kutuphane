# Python 3.13 bulunan küçük bir temel sistem kullan.
# Use a small base system that includes Python 3.13.
FROM python:3.13-slim

# Konteyner içindeki çalışma klasörünü belirle.
# Set the working directory inside the container.
WORKDIR /app

# Önce gerekli paketlerin listesini kopyala.
# Copy the dependency list first.
COPY requirements.txt .

# Python paketlerini yükle.
# Install the Python packages.
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını konteynere kopyala.
# Copy the application files into the container.
COPY icerik ./icerik

# Uygulamanın kullandığı portu belirt.
# Declare the port used by the application.
EXPOSE 8000

# FastAPI sunucusunu başlat.
# Start the FastAPI server.
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "icerik"]