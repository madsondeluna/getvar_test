# Use the official Python 3.8 image as the base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/requirements.txt

# Install the dependencies using pip install -r requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Set the default command to run the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
