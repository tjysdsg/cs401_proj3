FROM python:3.9-bullseye
WORKDIR /root

RUN pip install redis matplotlib numpy pandas requests scikit-learn tqdm

COPY runtime.py ./

ENTRYPOINT python runtime.py