class Graph:
    def __init__(self):
        print("Graph initialized")
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        """Add an undirected edge with a weight between two vertices."""
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        # Add the edge in both directions
        self.adjacency_list[vertex1].append((vertex2, weight))
        self.adjacency_list[vertex2].append((vertex1, weight))

    def find_components(self):
        """Find and return the connected components of the graph."""
        visited = set()
        components = []

        for vertex in self.adjacency_list:
            if vertex not in visited:
                component = []
                self._dfs_collect(vertex, visited, component)
                components.append(component)

        return components

    def _dfs_collect(self, vertex, visited, component):
        """Depth-First Search to collect all vertices in a component."""
        visited.add(vertex)
        component.append(vertex)
        for neighbor, _ in self.adjacency_list[vertex]:
            if neighbor not in visited:
                self._dfs_collect(neighbor, visited, component)

    def is_connected(self):
        """Check if the graph is connected and return components if not."""
        components = self.find_components()
        is_connected = len(components) == 1
        return is_connected, components

    def addable_edges(self, components):
        """Suggest edges to connect disconnected components."""
        if len(components) < 2:
            return []

        addable = []
        # Connect the first vertex of each component to the first vertex of the next component
        for i in range(len(components) - 1):
            # Suggest connecting the first vertex of the current component to the first vertex of the next
            addable.append((components[i][0], components[i + 1][0]))

        return addable
    
    def find_shortest_path(self, start: str, end: str):
        """Find the shortest path using the Bellman-Ford algorithm."""
        # Initialize distances and predecessors
        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        predecessors = {vertex: None for vertex in self.adjacency_list}
        distances[start] = 0

        # Relax edges
        for _ in range(len(self.adjacency_list) - 1):
            for vertex, edges in self.adjacency_list.items():
                for neighbor, weight in edges:
                    if distances[vertex] + weight < distances[neighbor]:
                        distances[neighbor] = distances[vertex] + weight
                        predecessors[neighbor] = vertex

        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()

        return path if distances[end] < float('inf') else None

    def read_from_file(self, filename):
        """Read graph data from a file."""
        print(f"Reading {filename}")
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(' ')
                # V 0000 Abbesses ;12 ;False 0 -> 
                # ['V', '0000', 'Abbesses', ';12', ';False', '0']
    
                i = 2  # Start after 'V', 'num_station'
                name_parts = []
                
                # Collect name parts until you hit a semicolon
                while i < len(parts) and parts[i][0] != ';':
                    name_parts.append(parts[i])
                    i += 1
                # after this while loop, name_parts[i] = ['Abbesses']

                # Join the name parts into a single string
                name = ' '.join(name_parts)
                # name = Abbesses
                

                # format pour les sommets :
                # V num_sommet nom_sommet numéro_ligne si_terminus branchement 
                # (0 stations en commun, 1 pour la direction 1,  2 pour la direction 2, ainsi de suite ...)
    
                # format pour les arêtes :
                # E num_sommet1 num_sommet2 temps_en_secondes

                if parts[0][0] == 'V':
                    num_sommet = parts[1].strip()
                    # num_sommet = 0001
                    self.add_vertex(num_sommet)
                elif parts[0][0] == 'E':
                    num_sommet1 = parts[1].strip()
                    num_sommet2 = parts[2].strip()
                    temps_en_secondes = int(parts[3].strip())
                    # parts = ['E', '0', '238', '41']
                    # num_sommet1, num_sommet2, temps_en_secondes = 0, 238, 41
                    self.add_edge(num_sommet1, num_sommet2, temps_en_secondes)

    def display(self):
        """Display the graph as an adjacency list."""
        if not self.adjacency_list:
            print("The graph is empty.")
            return

        for vertex, edges in self.adjacency_list.items():
            connections = ', '.join([f"{neighbor} (weight: {weight})" for neighbor, weight in edges])
            print(f"{vertex} --> {connections}")