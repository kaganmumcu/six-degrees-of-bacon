import pandas as pd
import networkx as nx
from itertools import combinations
import argparse # To get actor name from command line

def load_and_prepare_data():
    """Loads, filters, and merges the IMDb datasets."""
    print("--- Step 1: Loading and Preparing Data ---")
    try:
        # Load actors
        actors_df = pd.read_csv('name.basics.tsv.gz', sep='\t', usecols=['nconst', 'primaryName'])
        
        # Load movies
        movies_df = pd.read_csv('title.basics.tsv.gz', sep='\t', usecols=['tconst', 'titleType', 'primaryTitle'], low_memory=False)
        movies_df = movies_df[movies_df['titleType'] == 'movie']

        # Load principals
        principals_df = pd.read_csv('title.principals.tsv.gz', sep='\t', usecols=['tconst', 'nconst', 'category'])
        principals_df = principals_df[principals_df['category'].isin(['actor', 'actress'])]

        # Merge data
        merged_df = principals_df.merge(actors_df, on='nconst').merge(movies_df, on='tconst')
        
        # Clean up
        final_df = merged_df[['primaryTitle', 'primaryName']]
        final_df.rename(columns={'primaryTitle': 'movie', 'primaryName': 'actor'}, inplace=True)
        final_df.dropna(inplace=True)
        
        print(f"Data prepared. Found {len(final_df):,} movie-actor pairs.")
        return final_df

    except FileNotFoundError as e:
        print(f"\nERROR: {e}.")
        print("Please make sure the IMDb .tsv.gz files are in the same directory.")
        return None

def build_graph(df):
    """Builds a graph from the movie-actor DataFrame."""
    print("\n--- Step 2: Building the Actor Graph ---")
    G = nx.Graph()
    movie_to_actors = df.groupby('movie')['actor'].apply(list)
    
    print("Creating connections... This may take a while.")
    for movie, actors in movie_to_actors.items():
        if len(actors) > 1:
            for actor1, actor2 in combinations(actors, 2):
                G.add_edge(actor1, actor2)
    
    print(f"Graph built. Nodes: {G.number_of_nodes():,}, Edges: {G.number_of_edges():,}")
    return G, movie_to_actors

def find_bacon_path(G, movie_to_actors, start_actor, end_actor="Kevin Bacon"):
    """Finds and prints the shortest path between two actors."""
    print(f"\n--- Step 3: Finding Path from '{start_actor}' to '{end_actor}' ---")
    
    if not G.has_node(start_actor):
        print(f"ERROR: Actor '{start_actor}' not found in the dataset.")
        return
    if not G.has_node(end_actor):
        print(f"ERROR: Target actor '{end_actor}' not found in the dataset.")
        return

    # Create a helper lookup table for movie connections (on-the-fly)
    actor_pair_to_movie = {}
    for movie, actors in movie_to_actors.items():
        if len(actors) > 1:
            for actor1, actor2 in combinations(actors, 2):
                pair = frozenset([actor1, actor2])
                if pair not in actor_pair_to_movie:
                    actor_pair_to_movie[pair] = movie

    try:
        path = nx.shortest_path(G, source=start_actor, target=end_actor)
        bacon_number = len(path) - 1
        
        print(f"\nSuccess! The '{end_actor}' number for '{start_actor}' is: {bacon_number}")
        print("----------------------------------------------------")
        
        if bacon_number > 0:
            for i in range(len(path) - 1):
                actor1, actor2 = path[i], path[i+1]
                movie = actor_pair_to_movie[frozenset([actor1, actor2])]
                print(f"{i+1}. {actor1} was in '{movie}' with {actor2}")
        
        print("----------------------------------------------------")

    except nx.NetworkXNoPath:
        print(f"Sorry, no connection was found between '{start_actor}' and '{end_actor}'.")

def main():
    parser = argparse.ArgumentParser(description="Find the 'Six Degrees of Kevin Bacon' for any actor.")
    parser.add_argument("actor_name", type=str, help="The name of the actor to start from.")
    parser.add_argument("--target", type=str, default="Kevin Bacon", help="The target actor (default: Kevin Bacon).")
    
    args = parser.parse_args()
    
    master_df = load_and_prepare_data()
    
    if master_df is not None:
        graph, movie_lookup = build_graph(master_df)
        find_bacon_path(graph, movie_lookup, args.actor_name, args.target)

if __name__ == "__main__":
    main()