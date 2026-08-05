FROM python:3.11-slim

WORKDIR /app

# রিকোয়ারমেন্টস কপি ও ইনস্টল
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# পুরো প্রজেক্ট কপি
COPY . .

# পোর্ট খোলা
EXPOSE 10000

# অ্যাপ রান করা (মনে রাখবেন, আপনার main.py যদি app ফোল্ডারের ভেতরে থাকে, তাহলে "app.main:app")
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
