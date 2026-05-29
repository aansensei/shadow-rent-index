FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=7860", "--server.address=0.0.0.0"]
