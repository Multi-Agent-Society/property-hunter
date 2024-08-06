FROM python:3.11.9-slim

# Update the package list
RUN apt-get update

# Set the working directory
WORKDIR /src

# Copy requirements file and install dependencies
COPY src/requirements.txt src/requirements.txt
RUN pip install -r src/requirements.txt

# Copy the application code
COPY src /src

# Set the environment variable for the port
ENV PORT 8080

# Expose the port
EXPOSE $PORT

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py"]

