FROM python:3.11-alpine

WORKDIR /app

ENV TZ=America/Sao_Paulo

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:5000", "run:app"]