FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN  pip install -r requirements.txt
RUN mkdir templates
COPY app/* .
COPY templates/* ./templates
ENV OPENAI_API_KEY="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"
ENTRYPOINT [ "python" ]
CMD ["app.py" ]

# docker build --platform linux/arm64 -t cybereason/einav-flask-tst:1.2 .
# docker run -p 80:5001  cybereason/einav-flask-tst:1.3