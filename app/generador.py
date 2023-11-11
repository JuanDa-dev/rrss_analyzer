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
start_time = timeit.default_timer()
def generate_retweet_graph(tweets):
    G = nx.DiGraph()
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            G.add_edge(retweeted_user, retweeting_user)
    return G
import json

def generate_retweet_json(tweets):
    retweets_dict = {}
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            tweet_id = tweet['id']
            
            if retweeted_user not in retweets_dict:
                retweets_dict[retweeted_user] = {'receivedRetweets': 0, 'tweets': []}
            
            retweets_dict[retweeted_user]['receivedRetweets'] += 1
            retweets_dict[retweeted_user]['tweets'].append({'tweetId': tweet_id, 'retweetedBy': retweeting_user})
    
    return json.dumps(retweets_dict, indent=4)


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

def generate_co_retweets_json(tweets):
    co_retweets_dict = defaultdict(list)
    
    for tweet in tweets:
        if 'retweeted_status' in tweet:
            retweeted_user = tweet['retweeted_status']['user']['screen_name']
            retweeting_user = tweet['user']['screen_name']
            
            co_retweets_dict[retweeted_user].append(retweeting_user)
    
    return json.dumps(co_retweets_dict, indent=4)

def generate_mention_graph(tweets):
    G = nx.DiGraph()
    for tweet in tweets:
        if 'entities' in tweet and 'user_mentions' in tweet['entities']:
            tweeting_user = tweet['user']['screen_name']
            for mention in tweet['entities']['user_mentions']:
                mentioned_user = mention['screen_name']
                G.add_edge(tweeting_user, mentioned_user)
    return G

def generate_mentions_json(tweets):
    mentions_dict = {}
    
    for tweet in tweets:
        if 'entities' in tweet and 'user_mentions' in tweet['entities']:
            for mention in tweet['entities']['user_mentions']:
                mentioned_user = mention['screen_name']
                tweet_id = tweet['id']
                
                if mentioned_user not in mentions_dict:
                    mentions_dict[mentioned_user] = {'receivedMentions': 0, 'tweets': []}
                
                mentions_dict[mentioned_user]['receivedMentions'] += 1
                mentions_dict[mentioned_user]['tweets'].append({'tweetId': tweet_id, 'mentionedBy': tweet['user']['screen_name']})
    
    return json.dumps(mentions_dict, indent=4)

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
    retweet_data = generate_retweet_json(tweets)
    with open('retweet_data.json', 'w') as f:
        json.dump(retweet_data, f)
    
    G_crt = generate_co_retweet_graph(tweets)
    nx.write_gexf(G_crt, 'co_retweet_graph.gexf')
    corretweet_data = generate_co_retweets_json(tweets)
    with open('co_retweet_data.json', 'w') as f:
        json.dump(corretweet_data, f)
    
    G_m = generate_mention_graph(tweets)
    nx.write_gexf(G_m, 'mention_graph.gexf')
    mentions_data = generate_mentions_json(tweets)
    with open('mentions_data.json', 'w') as f:
        json.dump(mentions_data, f)

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
    


