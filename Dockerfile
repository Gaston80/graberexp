# Указываем базовый образ
FROM python:3.9-slim

# Обновляем пакетный менеджер и устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y python3-opencv


# Устанавливаем библиотеку OpenCV с помощью pip
RUN pip install opencv-python flack pymodbus redis

VOLUME /code
WORKDIR /code
COPY . /code

CMD ["python", "toNet.py"]
