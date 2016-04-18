FROM python:3

ADD /src /app
RUN pip install /app
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/wakeup.py", "--config=/app/config.toml"]
