FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /wifix

# Copy the requirements.txt file and install the dependencies
# Installing client libraries and any other package you need

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /logs
# Copy the rest of the application code to the container
COPY .. .

# Expose the port that the Flask application will run on
EXPOSE 8080

# Start the Flask application
CMD ["python3", "backend/db_server/app.py"]
