FROM python:3.7

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

CMD ["gunicorn", "flaskr:app", "-b", "0.0.0.0:5000"]