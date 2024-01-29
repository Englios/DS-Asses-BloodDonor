FROM ubuntu:latest

ENV PYTHONUNBUFFERED 1
# Add user guest
RUN useradd -m -d /home/guest guest

# Add crontab file in the cron directory
RUN apt-get update && apt-get -y install cron
RUN apt-get -y install vim

COPY . /app
WORKDIR /app

RUN apt-get install -y python3 \
    && apt-get -y install python3-pip \  
    && pip install --upgrade pip && pip install -r requirements.txt \ 
    && python3 -m nltk.downloader stopwords punkt wordnet 

# Copy cron job file and set permissions
RUN touch /var/log/cron.log \
    && touch /var/log/analyse_aggregate.log\ 
    && touch /var/log/analyse_gran.log\
    && touch /var/log/main.log

COPY cron /etc/cron.d/cron
RUN chmod 644 /etc/cron.d/cron \ 
    && crontab /etc/cron.d/cron

# Run the command on container startup
RUN python3 /app/analysis/analyse_aggregate.py \
    && python3 /app/analysis/analyse_gran.py
    
CMD cron && python3 /app/main.py