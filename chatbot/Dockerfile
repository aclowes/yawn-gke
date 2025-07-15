FROM python:3.12

WORKDIR /opt/yawn

COPY requirements.txt .
RUN pip install -r requirements.txt --progress-bar off

COPY chatbot.py .
CMD ["python", "chatbot.py"]
