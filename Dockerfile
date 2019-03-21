FROM python:3

WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "flaskr:app", "-b", "0.0.0.0:5000"]