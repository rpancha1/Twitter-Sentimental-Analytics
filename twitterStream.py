import findspark
findspark.init()
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
#import matplotlib.pyplot as plt

def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")
    sc.setLogLevel("WARN")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    #make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    # YOUR CODE HERE
    plt.ylabel('Word Count')
    plt.xlabel('Time Step')
    plt.axis([0,11,0,300])

    y=[]
    for a in counts:
        y.append(a[0])
    x = [0,1,2,3,4,5,6,7,8,9,10,11]
    plt.plot(x,y,color='b')
    plt.plot(x,y,'b-',marker = 'o')

    y=[]
    for a in counts:
        y.append(a[1])
    plt.plot(x,y,color='r')
    plt.plot(x,y,'ro')

    #plt.show()
    plt.savefig("trial")



def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    with open(filename) as f:
        li = set(f.read().splitlines())
    return set(li)

    # YOUR CODE HERE

def updateFunction(newValues, runningCount):
    if runningCount is None:
        runningCount = 0
    return sum(newValues, runningCount)


def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1])

    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).
    # YOUR CODE HERE
	
    #relevant_words = tweets.flatMap(lambda x:x.split(" "))
    words = tweets.flatMap(lambda x:x.split(" "))
    words = words.filter(lambda x: x in pwords or x in nwords)
    pairs = words.map(lambda x:("positive",1) if x in pwords else ("negative",1))
    wordCounts = pairs.reduceByKey(lambda x,y:x+y)
    #wordCounts = wordCounts.updateStateByKey(updateFunction)
    wordCounts.pprint()

    runningCount = pairs.updateStateByKey(updateFunction)
    
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    wordCounts.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    
    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    return counts


if __name__=="__main__":
    main()
