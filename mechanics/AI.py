class PathFindingAI:
    """AI for finding optimal paths and rail connections."""

    def __init__(self, nodes):
        self.nodes = nodes

    def find_optimal_path(self, start_node, end_node):
        """Find the optimal path between two nodes using A* algorithm."""
        # Implementation of A* algorithm
        open_set = {start_node.id}
        closed_set = set()

        # g_score is the cost from start to current node
        g_score = {node.id: float('inf') for node in self.nodes}
        g_score[start_node.id] = 0

        # f_score is g_score + heuristic (estimated cost to goal)
        f_score = {node.id: float('inf') for node in self.nodes}
        f_score[start_node.id] = self._heuristic(start_node, end_node)

        # came_from tracks the optimal path
        came_from = {}

        while open_set:
            # Find node with lowest f_score
            current_id = min(open_set, key=lambda id: f_score[id])
            current = next(node for node in self.nodes if node.id == current_id)

            if current_id == end_node.id:
                # We found the path
                return self._reconstruct_path(came_from, current_id)

            open_set.remove(current_id)
            closed_set.add(current_id)

            # Check all connected nodes
            for neighbor_id in current.connections:
                if neighbor_id in closed_set:
                    continue

                neighbor = next(node for node in self.nodes if node.id == neighbor_id)

                # Calculate tentative g_score
                tentative_g_score = g_score[current_id] + self._distance(current, neighbor)

                if neighbor_id not in open_set:
                    open_set.add(neighbor_id)
                elif tentative_g_score >= g_score[neighbor_id]:
                    continue

                # This path is better, record it
                came_from[neighbor_id] = current_id
                g_score[neighbor_id] = tentative_g_score
                f_score[neighbor_id] = g_score[neighbor_id] + self._heuristic(neighbor, end_node)

        # No path found
        return []

    def _heuristic(self, node1, node2):
        """Heuristic function for A* (Euclidean distance)."""
        x1, y1 = node1.position
        x2, y2 = node2.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def _distance(self, node1, node2):
        """Calculate actual distance between two nodes."""
        x1, y1 = node1.position
        x2, y2 = node2.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def _reconstruct_path(self, came_from, current_id):
        """Reconstruct the path from start to end."""
        total_path = [current_id]
        while current_id in came_from:
            current_id = came_from[current_id]
            total_path.append(current_id)
        return total_path[::-1]  # Reverse to get from start to end

    def find_minimum_spanning_tree(self):
        """Find the minimum spanning tree of all nodes using Kruskal's algorithm."""
        # Create all possible edges
        edges = []
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes[i + 1:], i + 1):
                distance = self._distance(node1, node2)
                edges.append((node1.id, node2.id, distance))

        # Sort edges by weight
        edges.sort(key=lambda x: x[2])

        # Kruskal's algorithm
        mst = []
        parent = {node.id: node.id for node in self.nodes}
        rank = {node.id: 0 for node in self.nodes}

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)

            if root_x == root_y:
                return

            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            else:
                parent[root_y] = root_x
                if rank[root_x] == rank[root_y]:
                    rank[root_x] += 1

        for u, v, weight in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, weight))

        return mst

    def is_solution_optimal(self, rails):
        """Check if the provided rails form a minimum spanning tree."""
        # Create a set of all nodes that are connected in the solution
        connected_nodes = set()
        for rail in rails:
            connected_nodes.add(rail['node1'])
            connected_nodes.add(rail['node2'])

        # Check if all nodes are connected
        if len(connected_nodes) != len(self.nodes):
            return False

        # Get the MST
        mst = self.find_minimum_spanning_tree()

        # Calculate the total cost of the MST
        mst_cost = sum(weight for _, _, weight in mst)

        # Calculate the total cost of the provided solution
        solution_cost = sum(rail['cost'] for rail in rails)

        # Allow a small margin of error (5%)
        return solution_cost <= mst_cost * 1.05