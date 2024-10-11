FROM base-image

# Set the working directory to /usr/src (or any other directory that does not conflict with "app")
WORKDIR /usr/src

# Set PYTHONPATH to include the /usr/src/app directory, so Python can find the app module
ENV PYTHONPATH="${PYTHONPATH}:/usr/src/"

# Copy the rest of the application into the container
COPY . ./app

# Command to run the application
CMD ["python", "app/main.py"]

