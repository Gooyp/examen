FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python create_db.py
EXPOSE 5000
CMD ["python", "run.py"]