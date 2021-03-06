FROM python:3.11.0a1-slim-bullseye
ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
ARG HOST=0.0.0.0
ARG PORT=80
ARG API_USERNAME=ubuntu
ARG API_PASSWORD=debian
ARG API_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ARG API_ALGORITHM=HS256
ARG API_ACCESS_TOKEN_EXPIRE_MINUTES=5256000000
ARG DATABASE_URL=sqlite:///database.db
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && \
    apt-get install -y gcc g++ libffi-dev && \
    pip install --no-cache-dir pip==21.3.1 cython && \
    pip install --no-cache-dir -r /code/requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY . /code/
CMD ["gunicorn" , "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:80"]
