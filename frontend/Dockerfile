# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy all files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir streamlit streamlit-webrtc requests av

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit on container start
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]