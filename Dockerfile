# # NOT WORKS!!!
# FROM ubuntu:20.10 
# RUN apt-get update \
#   && apt-get install -y python3-pip python3-dev libcairo2-dev libsdl-pango-dev\
#   && cd /usr/local/bin \
#   && ln -s /usr/bin/python3 python \
#   && pip3 install --upgrade pip

# ENTRYPOINT ["python3"]
# RUN python3 -V
# RUN pip install
# RUN pip install -U pip setuptools
# RUN pip install --upgrade setuptools

# RUN apt-get update 
# RUN  apt-get install -y make build-essential libssl-dev zlib1g-dev \
# libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
# libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev  
# RUN curl https://pyenv.run | bash  
# RUN echo 'export PATH="$HOME/.pyenv/bin:$PATH"'>> ~/.bashrc
# RUN echo 'eval "$(pyenv init -)"'>> ~/.bashrc
# RUN echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
# RUN pyenv install --list | grep " 3\.[678]"
# RUN pyenv install 3.8.1
# RUN pyenv global 3.8.1

# NOT WORKS!!!
FROM ubuntu:20.04
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get install -y tzdata libcairo2-dev libsdl-pango-dev 
# pull official base image
FROM python:3.8.3

# set work directory
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CHANGE!
WORKDIR /root/test_dock/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
RUN pip install django gunicorn
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CHANGE!
# RUN chmod -R 664 /root/test_dock/static/
RUN chmod -R 664 ./static
# EXPOSE 8000