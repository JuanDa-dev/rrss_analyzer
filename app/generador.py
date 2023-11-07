import os
import networkx as nx 
import glob 
import json 
import shutil,bz2,getopt,sys
from collections import defaultdict
import bz2
from datetime import datetime
import graphlib


def process_tweet(tweet, hashtags, authors, mentions, retweets, co_retweets):
    # Procesa el tweet según tus necesidades
    print(tweet)
    # Registra las menciones y retweets
    for mention in tweet['mentions']:
        mentions[mention] = mentions.get(mention, [])
        mentions[mention].append(tweet['id'])
    if 'retweet' in tweet:
        retweeted_id = tweet['retweet']
        retweets[retweeted_id] = retweets.get(retweeted_id, [])
        retweets[retweeted_id].append(tweet['author'])
        co_retweets[(tweet['author'], retweeted_id)] = co_retweets.get((tweet['author'], retweeted_id), 0) + 1

def main(argv):
    input_directory = 'app'
    start_date = None
    end_date = None
    hashtags_file = None
    output_directory = 'app'
    generate_graph_rt = False
    generate_json_rt = False
    generate_graph_mention = False
    generate_json_mention = False
    generate_graph_corretweet = False
    generate_json_corretweet = False

    try:
        opts, _ = getopt.getopt(argv, "d:fi:ff:h:", ["grt", "jrt", "gm", "jm", "gcrt", "jcrt"])
    except getopt.GetoptError:
        print("generador.py -d <path relativo> -fi <fecha inicial> -ff <fecha final> -h <nombre de archivo> [--grt] [--jrt] [--gm] [--jm] [--gcrt] [--jcrt]")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            input_directory = arg
        elif opt == '-fi':
            start_date = datetime.strptime(arg, '%d-%m-%y')
        elif opt == '-ff':
            end_date = datetime.strptime(arg, '%d-%m-%y')
        elif opt == '-h':
            hashtags_file = arg
        elif opt == '--grt':
            generate_graph_rt = True
        elif opt == '--jrt':
            generate_json_rt = True
        elif opt == '--gm':
            generate_graph_mention = True
        elif opt == '--jm':
            generate_json_mention = True
        elif opt == '--gcrt':
            generate_graph_corretweet = True
        elif opt == '--jcrt':
            generate_json_corretweet = True

    if hashtags_file:
        with open(hashtags_file, 'r') as file:
            hashtags = [line.strip() for line in file]
    else:
        hashtags = []

    authors = {}
    mentions = {}
    retweets = {}
    co_retweets = {}

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.bz2'):
                with bz2.BZ2File(os.path.join(root, file), 'rb') as f:
                    for line in f:
                        tweet = json.loads(line)
                        tweet_date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

                        if (not start_date or tweet_date >= start_date) and (not end_date or tweet_date <= end_date):
                            if not hashtags or any(hashtag.lower() in tweet['text'].lower() for hashtag in hashtags):
                                process_tweet(tweet, hashtags, authors, mentions, retweets, co_retweets)

    if generate_graph_rt:
        # Genera el grafo de retweets (rt.gexf)
        # Create a new directed graph object
        G = nx.DiGraph()

        # Add nodes for each user
        for user in retweets:
            G.add_node(user)

        # Add edges for each retweet
        for user, retweeted_users in retweets.items():
            for retweeted_user in retweeted_users:
                G.add_edge(user, retweeted_user)

        # Save the graph in GEXF format
        nx.write_gexf(G, "rt.gexf")
                
    if generate_json_rt:
        # Genera el JSON de retweets (rt.json)
        with open("rt.json", "w", encoding='utf-8') as f:
            json.dump(retweets, f, ensure_ascii=False, indent=4)
        
    if generate_graph_mention:
        # Genera el grafo de menciones (mención.gexf)
        G = nx.DiGraph()

        # Add nodes for each user
        for user in mentions:
            G.add_node(user)

        # Add edges for each retweet
        for user, retweeted_users in retweets.items():
            for retweeted_user in retweeted_users:
                G.add_edge(user, retweeted_user)

        # Save the graph in GEXF format
        nx.write_gexf(G, "mención.gexf")
    if generate_json_mention:
        # Genera el JSON de menciones (mención.json)
        with open("mención.json", "w", encoding='utf-8') as f:
            json.dump(mentions, f, ensure_ascii=False, indent=4)
    if generate_graph_corretweet:
        # Genera el grafo de co-retweets (corrtw.gexf)
        G = nx.DiGraph()

        # Add nodes for each user
        for user in retweets:
            G.add_node(user)

        # Add edges for each retweet
        for user, retweeted_users in retweets.items():
            for retweeted_user in retweeted_users:
                G.add_edge(user, retweeted_user)

        # Save the graph in GEXF format
        nx.write_gexf(G, "corrt.gexf")
    if generate_json_corretweet:
        # Genera el JSON de co-retweets (corrtw.json)
        with open("corrt.json", "w", encoding='utf-8') as f:
            json.dump(co_retweets, f, ensure_ascii=False, indent=4)    

if __name__ == "__main__":
    main(sys.argv[1:])



