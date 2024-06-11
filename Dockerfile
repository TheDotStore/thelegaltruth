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

ENV OPENAI_API_KEY="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"

# Install dependencies
RUN pip uninstall -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
