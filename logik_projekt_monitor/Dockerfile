FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir watchdog ffmpeg-python Pillow

COPY monitor_service.py /app/monitor_service.py

VOLUME ["/PROJEKTS"]

ENV ARTIST_NAME="Monitor Service"
ENV PROJECT_NAME=""

CMD ["python", "/app/monitor_service.py", "--project", "/PROJEKTS/${PROJECT_NAME}", "--db", "/PROJEKTS/${PROJECT_NAME}/db/${PROJECT_NAME}.db", "--artist", "${ARTIST_NAME}"]
