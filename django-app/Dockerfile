# 1. Start with an official Python base image
FROM python:3.13.9-slim

# 2. Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /kickhub


#4. Install depencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

# 5. Copy and install dependencies

# 6. Copy your application code into the container
COPY . .

COPY entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# 7. Expose the port Django runs on
EXPOSE 8000

# 8. Specify the command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]