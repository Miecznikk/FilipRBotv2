FROM python:3.10

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY main.py .
COPY requirements.txt .
COPY Controllers/rest_controller.py .
COPY .env .
COPY utils ./utils
COPY utils/commands_config.yaml .


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]