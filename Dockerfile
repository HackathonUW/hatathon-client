FROM python

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "runner.py" ]
