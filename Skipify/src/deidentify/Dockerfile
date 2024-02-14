# Use the Python 3.8 slim base image
FROM python:3.8-slim

# Create app directory
WORKDIR /app

# Create a user and group with unique UID and GID
RUN groupadd -g 15001 deid_group && \
    useradd -u 150001 -g deid_group deid_user

# Copy the entire application logic including requirements.txt
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt


# Remove unnecessary files after installing dependencies
RUN rm /app/requirements.txt

# Expose Flask port
EXPOSE 5000

# Set up needed environment variables
ENV project_name="skipify-demo"
ENV surrogate_name="CC"

# Set container user uid/gid
USER deid_user:deid_group

# Set max memory footprint for container process
# (Adjust the value according to your requirements)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]

