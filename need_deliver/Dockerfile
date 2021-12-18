# Install Python
FROM python:latest
RUN apt-get update && apt-get install -y --no-install-recommends nano sudo iputils-ping && rm -rf /var/lib/apt/lists/*

# Create folder code and copy all files
RUN mkdir /home/needdeliver/
RUN mkdir /home/needdeliver/prod/
ADD requirements.txt /home/needdeliver/prod/
ADD . /home/needdeliver/prod/
WORKDIR /home/needdeliver/prod/
RUN ls -al
# Install Python
RUN pip install --upgrade pip && pip install -r requirements.txt