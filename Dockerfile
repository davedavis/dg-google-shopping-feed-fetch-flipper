# From Alpine, for keeping things small.
FROM python:alpine

# Just me
MAINTAINER Dave Davis

# Setting the workdir on the container
WORKDIR /feed-flipper

# Copy and install the script dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all the files over.
COPY . .

# Run the main.py file.
CMD [ "python", "./main.py" ]

# ToDo: Extract key/secrets
# docker build -t feed-flipper-alpine .
# docker run -it feed-flipper-alpine