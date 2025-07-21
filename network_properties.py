# this code is calculating the network properties

import networkx as nx
import concurrent.futures
import collections
from networkx.algorithms.community import greedy_modularity_communities

def process_edges(chunk):
    edges = []
    for line in chunk:
        parts = line.strip().split()
        edges.append((parts[0], parts[1]))
       # edges.append((parts[0], parts[1], float(parts[2])))   # for weighted 
    return edges

def read_file(file_path, chunk_size=1000):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        lines = f.readlines()
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_edges, chunks)
    for edges in results:
        G.add_edges_from(edges)
    return G

def compute_betweenness(Gcc):
    bc = collections.OrderedDict(sorted(nx.betweenness_centrality(Gcc).items(), key=lambda x: x[0]))
    with open(path +grp+ "/betweenness.dat", 'w') as fbcc:
        for bcc in bc:
            fbcc.write(f"{bcc}\t{bc[bcc]}\n")
    return bc #[round(bc[node], 6) for node in bc]

def compute_clustering(Gcc):
    cc = collections.OrderedDict(sorted(nx.clustering(Gcc).items(), key=lambda x: x[0]))
    with open(path + grp+"/clustering.dat", 'w') as fccc:
        for ccc in cc:
            fccc.write(f"{ccc}\t{cc[ccc]}\n")
    return cc #[round(cc[node], 6) for node in cc]


def compute_degree(Gcc):
    deg = collections.OrderedDict(sorted(Gcc.degree(), key=lambda x: x[0]))
    with open(path +grp+ "/degree.dat", 'w') as fdegc:
        for degree in deg:
            fdegc.write(f"{degree}\t{deg[degree]}\n")
    return deg #[deg[node] for node in deg]


def compute_modularity(Gcc):
    mod = list(greedy_modularity_communities(Gcc))
    modules = [(node, i) for i, community in enumerate(mod) for node in community]
    print(modules[:10])
    sorted_modules = collections.OrderedDict(sorted(modules, key=lambda x: x[0]))
    #print(sorted_modules[:10])
    with open(path +grp+ "/modules.dat", 'w') as fmod:
        for mm in sorted_modules:
            fmod.write(f"{mm[0]}\t{mm[1]}\n")
    return sorted_modules #[sorted_modules[node] for node in sorted_modules]


def main(edge_file, output_file):
    graph = read_file(edge_file)
    Gc = sorted(nx.connected_components(graph), key=len, reverse=True) # largenst connected component
    Gcc = graph.subgraph(Gc[0])
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = {
            "betweenness": executor.submit(compute_betweenness, Gcc),
            "clustering": executor.submit(compute_clustering, Gcc),
            "degree": executor.submit(compute_degree, Gcc),
            "modularity": executor.submit(compute_modularity, Gcc)
        }

        bc_val = futures["betweenness"].result()
        cc_val = futures["clustering"].result()
        deg_val = futures["degree"].result()
        module_val = futures["modularity"].result()

    with open(output_file, "w") as f:
        f.write("Node\tDegree\tBetweenness\tClustering\tModularity\n")
        for node in sorted(Gcc.nodes()):          
            f.write(f"{node}\t{deg_val.get(node, 0)}\t{bc_val.get(node, 0)}\t{cc_val.get(node, 0)}\t{module_val.get(node, -1)}\n")
        #for edge in sorted(Gcc.edges()):     #for writing the edge list
            #f.write(f"{node[0]}\t{node[1]}\n")

path = "/"
groups = ['High_altitude', 'Low_altitude', 'TCtrl', 'TMin', 'TMax']
for grp in groups:
    edge_file = path+grp+"/gene_correlation_filtered.csv"
    output_file = path+grp+"/network_properties.csv"         #use adj_list.csv if writing edge list
    main(edge_file, output_file)
