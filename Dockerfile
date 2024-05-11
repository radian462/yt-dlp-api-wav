FROM python:3.11
WORKDIR /usr/src/app
COPY . .
RUN apt update && apt install -y ffmpeg
RUN pip install -r requirements.txt
EXPOSE 8080
ENV NAME World
CMD ["python", "./main.py"]
