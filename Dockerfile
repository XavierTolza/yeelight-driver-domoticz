FROM python:alpine

WORKDIR /app
ADD * /app/
RUN pip install -r requirements.txt
EXPOSE 5000
ENV YEELIGHT_DEBUG=False

CMD ["python","/app/app.py"]
