FROM python:3.10

WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY app.py ./app.py
COPY config.toml ./config.toml


RUN pip install -r requirements.txt
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "--server.port","8501", "--server.address","0.0.0.0"]
CMD ["./app.py"]e