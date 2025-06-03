FROM pytorch/pytorch:2.7.0-cuda12.6-cudnn9-runtime

WORKDIR /src

COPY requirements.txt .

RUN apt update && \
    apt install -y nano wget curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src .

CMD ["python", "main.py"]