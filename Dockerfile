#Container for Kafka - Spark streaming - Cassandra
FROM centos:centos7

RUN yum -y update;
RUN yum -y clean all;

# Install basic tools
RUN yum install -y  wget dialog curl sudo lsof vim axel telnet nano openssh-server openssh-clients bzip2 passwd tar bc git unzip

#Install Java
RUN yum install -y java-1.8.0-openjdk java-1.8.0-openjdk-devel 

#Create guest user. IMPORTANT: Change here UID 1000 to your host UID if you plan to share folders.
RUN useradd guest -u 1000
RUN echo guest | passwd guest --stdin

ENV HOME /home/guest
WORKDIR $HOME

USER guest

#Install Spark (Spark 2.1.1 - 02/05/2017, prebuilt for Hadoop 2.7 or higher)
RUN wget http://apache.mediamirrors.org/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz
RUN tar xvzf spark-2.4.0-bin-hadoop2.7.tgz
RUN mv spark-2.4.0-bin-hadoop2.7 spark

ENV SPARK_HOME $HOME/spark
RUN rm -f spark-2.4.0-bin-hadoop2.7.tgz

#Install Kafka
RUN wget http://apache.mediamirrors.org/kafka/2.1.0/kafka_2.11-2.1.0.tgz
RUN tar xvzf kafka_2.11-2.1.0.tgz
RUN mv kafka_2.11-2.1.0 kafka
RUN rm -f kafka_2.11-2.1.0.tgz

ENV PATH $HOME/spark/bin:$HOME/spark/sbin:$HOME/kafka/bin:$PATH

#Install Python3 distribution
RUN wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
RUN tar xvzf Python-3.7.1.tgz
RUN rm -f Python-3.7.1.tgz
RUN mv Python-3.7.1 python3
RUN cd python3
RUN yum groupinstall -y "Development Tools"
RUN ./configure
RUN make
RUN make install

#Install Python modules
ENV PYTHON_PIP_VERSION 18.1
RUN set -ex; \
	\
	wget -O get-pip.py 'https://bootstrap.pypa.io/get-pip.py'; \
	\
	python get-pip.py \
		--disable-pip-version-check \
		--no-cache-dir \
		"pip==$PYTHON_PIP_VERSION"

RUN pip install requests bs4 html5lib sklearn pandas numpy scipy seaborn matplotlib plotly dash PyGithub cassandra-driver kafka-python jupyter 

USER root

#Install Cassandra
ADD datastax.repo /etc/yum.repos.d/datastax.repo
RUN yum install -y datastax-ddc
RUN echo "/usr/lib/python2.7/site-packages" |tee /home/guest/anaconda2/lib/python2.7/site-packages/cqlshlib.pth

#Environment variables for Spark and Java
ADD setenv.sh /home/guest/setenv.sh
RUN chown guest:guest setenv.sh
RUN echo . ./setenv.sh >> .bashrc

#Startup (start SSH, Cassandra, Zookeeper, Kafka producer)
ADD startup_script.sh /usr/bin/startup_script.sh
RUN chmod +x /usr/bin/startup_script.sh

#Init Cassandra 
ADD init_cassandra.cql /home/guest/init_cassandra.cql
RUN chown guest:guest init_cassandra.cql