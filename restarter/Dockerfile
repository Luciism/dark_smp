FROM python:3.12-alpine
RUN pip install --no-cache-dir mcrcon
COPY restart_scheduler.py /app/restart_scheduler.py
ENTRYPOINT ["python", "/app/restart_scheduler.py"]

