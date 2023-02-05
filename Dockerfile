FROM ubuntu:22.10 

WORKDIR /app

COPY src src 
COPY data data
ADD virtualenv/requirements.x86_64.txt requirements.txt


RUN apt update  &&  apt install -y rustc cargo python3.10-dev python3-pip python3-pip-whl  
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt 

ADD do_20_start_main.sh . 
RUN chmod a+x do_20_start_main.sh 

EXPOSE 443 

RUN pwd && ls  

CMD  /bin/sh ./do_20_start_main.sh --gptj 
