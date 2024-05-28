FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN  pip install -r requirements.txt
RUN mkdir templates
COPY app/* .
COPY templates/* ./templates
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENTRYPOINT [ "python" ]
CMD ["app.py" ]

# docker build --platform linux/arm64 --build-arg OPENAI_API_KEY -t cybereason/einav-flask-tst:1.10 .
# docker run -p 5001:5001  cybereason/einav-flask-tst:1.10