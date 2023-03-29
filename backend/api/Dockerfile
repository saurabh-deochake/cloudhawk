FROM python:3.10-slim
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . .

# Define environment variable
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
EXPOSE 8080

ENTRYPOINT ["python"]
CMD ["api.py"]