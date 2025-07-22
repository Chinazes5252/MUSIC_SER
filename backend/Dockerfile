FROM python:3.11.9-slim

# Обновляем pip и устанавливаем Uvicorn с автоперезапуском
RUN pip install --upgrade pip && pip install "uvicorn[standard]"

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем весь код
COPY . .

# Указываем порт (если хочешь)
EXPOSE 8000

# Запускаем FastAPI через Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
