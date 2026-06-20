FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

WORKDIR /app

# copy requirements ก่อน เพื่อใช้ Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy โค้ดทั้งหมดเข้า container
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]