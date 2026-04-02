# Use an official Python 3.12 runtime
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements first to cache the pip install step
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir keeps the Docker image size extremely small
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the rest of the application code into the container
COPY . .

# Expose port 8501 (Streamlit UI) and 6006 (Phoenix Observability)
EXPOSE 8501
EXPOSE 6006

# Command to run our Streamlit app
CMD ["streamlit", "run", "src/bot.py", "--server.address=0.0.0.0"]
