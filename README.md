# Twitter-Sentiment-Analytics

INTRODUCTION : 
In this project, I learned about processing live data streams using Spark’s streaming APIs and Python. Performed a basic sentiment analysis of realtime tweets. In addition, also got a basic introduction to Apache Kafka, which is a queuing service for data streams.

Steps to run :

1) Download the 16M.txt.zip file from the following link :

      ```https://drive.google.com/open?id=1k5tP7-6lrDIyGaOzvN4_288vN40Yut37```
2) Unzip it
3) Start Zookeeper Service 
      ```$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties```
      
4) Start Kafka Servie 
      ```$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties```
      
5) Create a topic named twitterstream in kafka 
      ```$KAFKA_HOME/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic twitterstream```
      
6) Run ```twitter_to_kafka.py```

7) Run the stream analysis program in the following way :
      ```$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 twitterStream.py```
      
OUTPUT : 

![alt text](https://github.com/prmody96/Twitter-Sentiment-Analytics/blob/master/twitter_git.png)
      
