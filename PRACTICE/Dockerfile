FROM python:3.10-buster
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5010
CMD ["python","./flaskDocker.py"]