FROM python:3.8

COPY requirements/nlp_requirements.txt ./
RUN pip3 install -r nlp_requirements.txt