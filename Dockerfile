FROM python:3.12-slim
WORKDIR /app
COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt
COPY . .
ENV FLASK_APP=flask_app.py
ENV FLASK_CONFIG=production
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "flask_app:app"]
