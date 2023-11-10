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

def process_tweets(input_directory, start_date, end_date, hashtags):
    
    retweets = {}
    graph_corretweet = nx.DiGraph()
    graph_mention = nx.DiGraph()

    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.bz2'):
                with bz2.BZ2File(os.path.join(root, file), 'rb') as f:
                    for line in f:
                        tweet = json.loads(line)
                        print(tweet.keys()) 
                        if 'user' not in tweet:
                            continue
                        author = tweet['user']['screen_name']

                        # Process retweets for corretweet graph
                        if 'retweeted_status' in tweet:
                            original_tweet_id = tweet['retweeted_status']['id']
                            if original_tweet_id not in retweets:
                                retweets[original_tweet_id] = [author]
                            else:
                                for user in retweets[original_tweet_id]:
                                    graph_corretweet.add_edge(user, author)
                                retweets[original_tweet_id].append(author)

                        # Process mentions for mention graph
                        if 'entities' in tweet and 'user_mentions' in tweet['entities']:
                            for user_mention in tweet['entities']['user_mentions']:
                                mentioned_user = user_mention['screen_name']
                                graph_mention.add_edge(author, mentioned_user)
                                
                                
def generate_graphs(graphs, generate_graph, generate_json):
    for name, graph in graphs.items():
        if generate_graph[name]:
            nx.write_gexf(graph, f'{name}.gexf')
        if generate_json[name]:
            with open(f'{name}.json', 'w') as f:
                json.dump(nx.node_link_data(graph), f)


def main(argv):
    input_directory = 'app'
    start_date = None
    end_date = None
    hashtags = None
    generate_graph_rt = False
    generate_json_rt = False
    generate_graph_mention = False
    generate_json_mention = False
    generate_graph_corretweet = False
    generate_json_corretweet = False
    
    process_tweets(input_directory, start_date, end_date, hashtags)  
    try:
        opts, _ = getopt.getopt(argv, "d:fi:ff:h:grt:jrt:gm:jm:gcrt:jcrt:")
    except getopt.GetoptError:
        print("generador.py -d <path relativo> -fi <fecha inicial> -ff <fecha final> -h <nombre de archivo> -grt -jrt -gm -jm -gcrt -jcrt")
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
        elif opt == '-grt':
            generate_graph_rt = True
        elif opt == '-jrt':
            generate_json_rt = True
        elif opt == '-gm':
            generate_graph_mention = True
        elif opt == '-jm':
            generate_json_mention = True
        elif opt == '-gcrt':
            generate_graph_corretweet = True
        elif opt == '-jcrt':
            generate_json_corretweet = True
            
        
        generate_graph = {
        'rt': generate_graph_rt,
        'mention': generate_graph_mention,
        'corretweet': generate_graph_corretweet
        }
        generate_json = {
            'rt': generate_json_rt,
            'mention': generate_json_mention,
            'corretweet': generate_json_corretweet
        }
        graphs = {
            'rt': graph_rt,
            'mention': graph_mention,
            'corretweet': graph_corretweet
        }
        generate_graphs(graphs, generate_graph, generate_json)
    

if __name__ == "__main__":
    main(sys.argv[1:])
    


