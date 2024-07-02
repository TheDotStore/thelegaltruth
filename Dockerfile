# Use the python:3.9-slim image for a smaller size
FROM python:3.9-slim

WORKDIR /myapp

# Update and install required packages for Pillow and PyMuPDF
# uncomment if required
# RUN apt-get update && apt-get install -y \
#     libffi-dev \
#     libssl-dev \
#     zlib1g-dev \
#     libjpeg-dev \
#     libfreetype6-dev \
#     liblcms2-dev \
#     libopenjp2-7-dev \
#     libtiff-dev \
#     libharfbuzz-dev \
#     libfribidi-dev \
#     libcairo2-dev \
#     gcc \
#     g++ \
#     make \
#     && rm -rf /var/lib/apt/lists/*

COPY . .

ENV OPENAI_API_KEY="sk-proj-aF0Qm3FL0k2rpWVn6MZiT3BlbkFJblLhIPzDk7g6ATJxklCg"

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
