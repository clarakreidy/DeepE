FROM nikolaik/python-nodejs:python3.10-nodejs18-slim

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY . .

RUN npm install
RUN npm install -D tailwindcss

RUN npx tailwindcss -i ./static/src/input.css -o ./static/dist/css/output.css

RUN pip install -r requirements.txt

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
