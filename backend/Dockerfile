FROM python:3.10-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
COPY  backend/foodgram .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
