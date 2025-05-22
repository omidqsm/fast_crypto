FROM python:3.13.0-alpine
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python3 src/main.py