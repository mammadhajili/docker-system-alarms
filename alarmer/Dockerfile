FROM debian:jessie-slim
MAINTAINER Mammad Hajili mammadhajili@gmail.com

# Oracle Instant Client layer
COPY instantclient/* /tmp/

RUN apt-get update && apt-get install -y alien && \
    alien -iv /tmp/oracle-instantclient12.2-basiclite-12.2.0.1.0-1.x86_64.rpm && \
    alien -iv /tmp/oracle-instantclient12.2-devel-12.2.0.1.0-1.x86_64.rpm && \
    apt-get purge -y alien perl perl5 && apt-get -y autoremove && apt-get clean && \
    rm -rf /tmp/oracle-* && rm -rf /usr/share/docs && rm -rf /usr/share/man && \
    mkdir /home/alarmer

# Environment variables
ENV ORACLE_HOME=/usr/lib/oracle/12.2/client64
ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib
ENV PATH=$ORACLE_HOME/bin:$PATH

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY app/requirements.txt /home/alarmer/requirements.txt

# Python3 + cx_Oracle layer + Psycopg2 + YAML 
RUN apt-get install -y python3 python3-dev python3-pip libaio1
RUN pip3 install -r /home/alarmer/requirements.txt
RUN pip3 install --upgrade urllib3
RUN apt-get purge -y python3-dev python3-pip && apt-get -y autoremove && apt-get clean
RUN rm -rf /usr/share/doc && rm -rf /usr/share/man

# Application layer

COPY app /home/alarmer
ADD wait-for-it.sh  /home/alarmer/

WORKDIR /home/alarmer

CMD ["./wait-for-it.sh", "postgre", "python3", "AlarmApp.py"]
