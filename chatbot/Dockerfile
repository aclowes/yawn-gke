FROM python:3.12

WORKDIR /opt/yawn

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --progress-bar off

COPY chatbot.py .
CMD ["python", "chatbot.py"]
