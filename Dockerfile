#using slim because its light weight base image 
From python:3.10-slim
#setting working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
build-essential \
libgl1 \
libglib2.0-0 && \
rm -rf /var/lib/apt/lists/*   

RUN pip install --upgrade pip
COPY . /app/
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

