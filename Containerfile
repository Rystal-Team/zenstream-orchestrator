FROM python:3.10.0-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY orchestrator/ ./orchestrator/
CMD ["python", "-m", "orchestrator.__init__"]