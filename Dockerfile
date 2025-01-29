# Use an official Ubuntu as a parent image
FROM ubuntu:latest

# Install necessary packages
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y python3 python3-pip python3-venv wine64 wine32 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a virtual environment and activate it
RUN python3 -m venv /app/venv

# Ensure pip is up to date in the virtual environment
RUN /app/venv/bin/pip install --upgrade pip

# Copy the application code
COPY . /app

# Install Python dependencies in the virtual environment
RUN /app/venv/bin/pip install -r requirements.txt

# Ensure the uploads directory exists and has the correct permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Expose the port the app runs on
EXPOSE 8080

# Use the virtual environment's Python to run the app
CMD ["/app/venv/bin/python", "main.py"]
