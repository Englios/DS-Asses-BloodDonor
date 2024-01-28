FROM ubuntu:latest

WORKDIR /app
# Add user guest
RUN useradd -m -d /home/guest guest

# Add crontab file in the cron directory
RUN apt-get update && apt-get -y install cron
RUN apt-get -y install vim

# Install Python
COPY requirements.txt /app/requirements.txt
RUN apt-get install -y python3 \
    && apt-get -y install python3-pip \  
    && pip install --upgrade pip && pip install -r requirements.txt \ 
    && python3 -m nltk.downloader stopwords punkt wordnet 

COPY . /app

# Copy cron job file and set permissions
RUN touch /var/log/cron.log \
    && touch /var/log/analyse_aggregate.log\ 
    && touch /var/log/analyse_gran.log

COPY cron /etc/cron.d/cron
RUN chmod 644 /etc/cron.d/cron \ 
    && crontab /etc/cron.d/cron

# Run the command on container startup
CMD cron && python3 /app/main.py