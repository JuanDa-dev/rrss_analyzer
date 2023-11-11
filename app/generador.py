import os
import networkx as nx 
import glob 
import json 
import shutil,bz2,getopt,sys
from collections import defaultdict
import bz2
from datetime import datetime
import graphlib
import os
import timeit


def generate_retweet_graph(tweets):
    G = nx.DiGraph()
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            G.add_edge(retweeted_user, retweeting_user)
    return G

def create_retweet_json(tweets):
    retweets = {}
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            tweet_id = tweet['id']
            if retweeted_user not in retweets:
                retweets[retweeted_user] = {'receivedRetweets': 1, 'tweets': [{'id': tweet_id, 'retweeted_by': retweeting_user}]}
            else:
                retweets[retweeted_user]['receivedRetweets'] += 1
                retweets[retweeted_user]['tweets'].append({'id': tweet_id, 'retweeted_by': retweeting_user})
    with open('rt.json', 'w') as f:
        json.dump(retweets, f)


def generate_co_retweet_graph(tweets):
    G = nx.Graph()
    retweets = defaultdict(list)
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            retweets[retweeted_user].append(retweeting_user)
    for users in retweets.values():
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                G.add_edge(users[i], users[j])
    return G

def create_coretweet_json(tweets):
    coretweets = {}
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            if retweeted_user not in coretweets:
                coretweets[retweeted_user] = {'totalCoretweets': 1, 'retweeters': [retweeting_user]}
            else:
                coretweets[retweeted_user]['totalCoretweets'] += 1
                coretweets[retweeted_user]['retweeters'].append(retweeting_user)
    coretweets = {user: data for user, data in coretweets.items() if len(data['retweeters']) > 2}
    with open('corrtw.json', 'w') as f:
        json.dump(coretweets, f)

def generate_mention_graph(tweets):
    G = nx.DiGraph()
    for tweet in tweets:
        if 'entities' in tweet and 'user_mentions' in tweet['entities']:
            tweeting_user = tweet['user']['screen_name']
            for mention in tweet['entities']['user_mentions']:
                mentioned_user = mention['screen_name']
                G.add_edge(tweeting_user, mentioned_user)
    return G

def create_mention_json(tweets):
    mentions = {}
    for tweet in tweets:
        if 'entities' in tweet and 'user_mentions' in tweet['entities']:
            mentioning_user = tweet['user']['screen_name']
            tweet_id = tweet['id']
            for user_mention in tweet['entities']['user_mentions']:
                mentioned_user = user_mention['screen_name']
                if mentioned_user not in mentions:
                    mentions[mentioned_user] = {'receivedMentions': 1, 'mentions': [{'id': tweet_id, 'mentioned_by': mentioning_user}]}
                else:
                    mentions[mentioned_user]['receivedMentions'] += 1
                    mentions[mentioned_user]['mentions'].append({'id': tweet_id, 'mentioned_by': mentioning_user})
    with open('mencion.json', 'w') as f:
        json.dump(mentions, f)

def process_tweets(input_directory, start_date, end_date, hashtags):
    tweets = []
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.bz2'):
                with bz2.BZ2File(os.path.join(root, file), 'rb') as f:
                    for line in f:
                        tweet = json.loads(line)
                        tweets.append(tweet)
                        
    G_rt = generate_retweet_graph(tweets)
    nx.write_gexf(G_rt, 'retweet_graph.gexf')
    G_crt = generate_co_retweet_graph(tweets)
    nx.write_gexf(G_crt, 'co_retweet_graph.gexf')
    G_m = generate_mention_graph(tweets)
    nx.write_gexf(G_m, 'mention_graph.gexf')
    
    create_retweet_json(tweets)
    create_mention_json(tweets)
    create_coretweet_json(tweets)
        
start_time = timeit.default_timer()
def main(argv):
    input_directory = 'app'
    start_date = None
    end_date = None
    hashtags = None
    
    
    process_tweets(input_directory, start_date, end_date, hashtags)  
    try:
        opts, _ = getopt.getopt(argv, "d:fi:ff:h:grt:jrt:gm:jm:gcrt:jcrt:")
    except getopt.GetoptError:
        print("generador.py -d <path relativo> -fi <fecha inicial> -ff <fecha final> -h <nombre de archivo> -grt -jrt -gm -jm -gcrt -jcrt")
        sys.exit(2)

    options = {
    '-d': lambda arg: arg,
    '-fi': lambda arg: datetime.strptime(arg, '%d-%m-%y'),
    '-ff': lambda arg: datetime.strptime(arg, '%d-%m-%y'),
    '-h': lambda arg: arg,
    '-grt': lambda arg: True,
    '-jrt': lambda arg: True,
    '-gm': lambda arg: True,
    '-jm': lambda arg: True,
    '-gcrt': lambda arg: True,
    '-jcrt': lambda arg: True
}

    for opt, arg in opts:
        if opt in options:
            result = options[opt](arg)
            if opt in ['-d', '-fi', '-ff', '-h']:
                globals()[opt[1:]] = result
            else:
                globals()[f'generate_{opt[2:]}'] = result
                
if __name__ == "__main__":
    main(sys.argv[1:])

end_time = timeit.default_timer()
print(f"Total execution time: {end_time - start_time} seconds")
    


