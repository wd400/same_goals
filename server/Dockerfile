FROM python:3.8

WORKDIR /app/src


#RUN apt-get update && apt-get install python3.8-pip python3.8 -y && apt-get install wget -y && apt-get install zip -y

RUN mkdir -p /app/src/models

RUN wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/paraphrase-mpnet-base-v2.zip

RUN unzip paraphrase-mpnet-base-v2.zip -d /app/src/models/paraphrase-mpnet-base-v2/

COPY requirements.txt /app/requirements.txt

RUN pip3 --default-timeout=1000 install -r /app/requirements.txt 

COPY . /app

CMD python3 main.py         
