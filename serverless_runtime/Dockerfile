FROM python:3.9-bullseye
WORKDIR /root

RUN pip install -r requirements.txt

COPY runtime.py ./

ENTRYPOINT python runtime.py