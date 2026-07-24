# choose an operating system
FROM python:3.11-slim

# set the working directory in the container
WORKDIR /app

# copy the requirements.txt file to the container
COPY requirements.txt .

# install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# create a non-root user
RUN useradd -m appuser

# bring in project files and give ownership to the new user
#(this must be done while are still ROOT)
COPY --chown=appuser:appuser . . 

# Security: Switch to the non-root user for excuting the app
USER appuser

# expose the port 5000 and run the app
EXPOSE 5000
CMD ["python", "app.py"]

