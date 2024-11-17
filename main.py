import Graph as g

import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(graph):
    G = nx.Graph()
    
    # Add edges to the NetworkX graph
    for vertex, edges in graph.adjacency_list.items():
        for neighbor, weight in edges:
            G.add_edge(vertex, neighbor, weight=weight)

    # Create a layout for the nodes
    pos = nx.spring_layout(G, k=0.5)  # Adjust k for spacing

    # Draw the nodes with custom settings
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_color='black')

    # Draw the edges with custom settings
    edge_widths = [0.5 if weight < 5 else 1.5 for _, _, weight in G.edges(data='weight')]
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='gray')

    # Add edge labels
    edge_labels = { (u, v): f"{d['weight']}" for u, v, d in G.edges(data=True) }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Add title and show the plot
    plt.title("Metro Graph Visualization")
    plt.axis('off')  # Turn off the axis
    plt.show()

def main():
    graph = g.Graph()
    metro_file = "src/metro.txt"
    graph.read_from_file(metro_file)

    is_connected, components = graph.is_connected()
    
    if not is_connected:
        print("The graph isn't connected.")

        addable = graph.addable_edges(components)

        for vertex1, vertex2 in addable:
            # default values 60s
            graph.add_edge(vertex1, vertex2, 60)

        # Check connectivity again after adding edges
        is_connected, _ = graph.is_connected()
        if is_connected:
            print("The graph is now connected.")
        else:
            print("The graph is still not connected after adding edges.")

    visualize_graph(graph)

if __name__ == "__main__":
    main()