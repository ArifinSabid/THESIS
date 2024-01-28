import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def calculate_early_times(G):
    for node in nx.topological_sort(G):
        if not list(G.predecessors(node)):
            G.nodes[node]['ES'] = 0
            G.nodes[node]['EF'] = G.nodes[node]['duration']
        else:
            max_early_finish = max([G.nodes[predecessor]['EF'] for predecessor in G.predecessors(node)], default=0)
            G.nodes[node]['ES'] = max_early_finish
            G.nodes[node]['EF'] = max_early_finish + G.nodes[node]['duration']

def calculate_late_times(G):
    for node in list(nx.topological_sort(G))[::-1]:
        G.nodes[node]['LF'] = min([G.nodes[successor]['LS'] for successor in G.successors(node)],
                                   default=G.nodes[node]['EF'])
        G.nodes[node]['LS'] = G.nodes[node]['LF'] - G.nodes[node]['duration']

def identify_critical_path(G):
    return [node for node in G.nodes if G.nodes[node]['delta'] == 0]

def visualize_graph(G, critical_path):
    pos = nx.circular_layout(G)
    node_colors = ['red' if node in critical_path else 'lightblue' for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=1800, node_color=node_colors)
    edge_labels = {(u, v): f"LF: {G.nodes[v]['LF']}, Duration: {G.nodes[v]['duration']} days" for u, v in G.edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

def main():
    data = {
        'Task': [],
        'Duration': [],
        'Dependencies': [],
    }
    while True:
        task = input("Enter task name (or press Enter to finish): ")
        if not task:
            break
        duration = int(input("Enter task duration (in days): "))
        dependencies = input("Enter task dependencies (comma-separated, or press Enter for none): ")
        dependencies = dependencies.split(",") if dependencies else []
        data['Task'].append(task)
        data['Duration'].append(duration)
        data['Dependencies'].append(dependencies)
    
    df = pd.DataFrame(data)
    G = nx.DiGraph()
    for index, row in df.iterrows():
        G.add_node(row['Task'], duration=row['Duration'])
        if row['Dependencies']:
            for dep_task in row['Dependencies']:
                G.add_edge(dep_task, row['Task'])
    
    calculate_early_times(G)
    calculate_late_times(G)
    for node in G.nodes:
        G.nodes[node]['delta'] = G.nodes[node]['LF'] - G.nodes[node]['EF']
    critical_path = identify_critical_path(G)
    visualize_graph(G, critical_path)

if __name__ == '__main__':
    main()
