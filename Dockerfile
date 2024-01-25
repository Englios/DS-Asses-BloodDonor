FROM ubuntu:latest

WORKDIR /app

RUN apt-get update && apt-get -y install cron
RUN apt-get update && \
    apt-get -y install sudo
RUN sudo useradd -m -d /home/guest guest
# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Python
RUN apt-get -y install python3
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /app

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log