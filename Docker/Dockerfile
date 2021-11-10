FROM python:3.7

RUN apt-get update && \
	apt-get install -y git

RUN mkdir /app
WORKDIR /app

RUN git clone https://github.com/DCBIA-OrthoLab/Utilities.git
#RUN unzip 3.2.zip
#RUN mv OAI-3.2 OAI
#RUN rm -rf 3.2.zip \
	#rm -rf OAI-3.2

WORKDIR /app/Utilities/py
RUN pip3 install -r ./requirements.txt
