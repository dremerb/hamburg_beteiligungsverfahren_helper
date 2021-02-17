FROM python:3

WORKDIR /usr/src/app

EXPOSE 5000

#RUN git clone https://github.com/dremerb/hamburg_beteiligungsverfahren_helper.git
COPY . .
#WORKDIR /usr/src/app/hamburg_beteiligungsverfahren_helper/summarizer
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python"]

CMD ["main.py"]
