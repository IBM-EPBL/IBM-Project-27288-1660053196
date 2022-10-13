FROM python:3.10.6
WORKDIR /app
COPY REquirements.txt ./
RUN pip install -r REquirements.txt
COPY . .
EXPOSE 5000
CMD ["python","./main.py"]