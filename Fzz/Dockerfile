FROM python:3.10-slim
WORKDIR /app
COPY . ./app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000 5880
CMD [ "python", "./input_db.py" ]
