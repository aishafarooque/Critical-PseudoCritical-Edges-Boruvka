class Graph():
    def __init__(self, n) -> None:
        self.__len__ = 0
        self.graph = [[-1 for _ in range(n)] for _ in range(n)]
        
        self.vertices = set()
        self.totalWeight = 0
    
    def add(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight
        
        self.vertices.add(u)
        self.vertices.add(v)

        self.totalWeight += weight
        self.__len__ += 1

    def getEdge(self, u, v):
        # print (f'Getting edge for {u} and {v}')

        try:
            return self.graph[u][v]
        except:
            return -1

    def getEdges(self, u):
        '''
        Returns weights for all edges from u.
        If u is not connected to the ith vertex, then it returns -1.
        '''

        edges = []

        for i in range(0, len(self.graph)):
            edges.append(self.getEdge(u,i))
        
        # print (f'Getting {u} edges: {edges}')
        return edges
    
    def deleteEdge(self, u, v):
        try:
            edge = self.graph[u][v]
            if edge:
                print (f'Deleting graph[{u}][{v}]={self.graph[u][v]}')
                self.graph[u][v] = -1
                self.graph[v][u] = -1
                return edge
        except:
            return None
    
    def getNumberOfVertices(self):
        return len(self.vertices)

    def printWithVertexInformation(self):
        '''
        Prints the graph. Outputs: 
            Vertex #0: 1: 1, 3: 2, 4: 3
            Vertex #1: 0: 1, 2: 1, 4: 6
            Vertex #2: 1: 1, 3: 2
            Vertex #3: 0: 2, 2: 2, 4: 3
            Vertex #4: 0: 3, 1: 6, 3: 3
        '''
        for i in range(0, len(self.graph)):
            res = ''
            for j in range(0, len(self.graph[i])):
                if self.graph[i][j] != -1:
                    res += f'{j}: {self.graph[i][j]}, '
            print (f'Vertex #{i}: {res}'[:-2])
        print ()
    
    def printGraphAsTable(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.graph]))

    def __len__(self):
        return self.__len__

class ConnectedComponents():
    def __init__(self, numberOfEdges) -> None:
        self.n = numberOfEdges
        self.nodes = []
        for i in range(0, numberOfEdges):
            self.nodes.append({ i })

    def find(self, u):
        for i in range(0, n):
            if u in self.nodes[i]:
                return i
        return -1
    
    def connect(self, u, v):
        '''
        Merges u and v together. For example:

        Input: [{0}, {1}, {2}, {3}, {4}, {5}]
        Remaining nodes after merging are: [{0, 1}, {2}, {3}, {4}]
        Remaining nodes after merging are: [{0, 1, 2}, {3}, {4}]
        Remaining nodes after merging are: [{0, 1, 2, 3}, {4}]
        Remaining nodes after merging are: [{0, 1, 2, 3, 4}]
        '''
        
        indexU = self.find(u)
        indexV = self.find(v)

        if indexU == -1 or indexV == -1 or indexU == indexV: 
            print (f'Ineligible conditions, u = {u}, v = {v}')
            return
        
        self.nodes[indexU].update(self.nodes[indexV])
        self.nodes.pop(indexV)
        
        print (f'Merged {u} and {v}')
        print (f'Remaining nodes after merging are: {self.nodes}')
    
    def getMinimumWeightedEdges(self, graph, debug=False):
        minimumEdge = None
        for node in self.nodes:
            for vertex in node:
                edges = graph.getEdges(vertex) 
                # (print (f'node = {node}, vertex = {vertex}, edges = {edges}') if debug else None)
                for i in range(0, len(edges)-1):
                    if edges[i] != -1:
                        source, target, weight = vertex, i, edges[i]
                        if target not in node:
                            # Select the minimum-weight edge incident on v
                            if minimumEdge == None or minimumEdge[2] > weight:
                                minimumEdge = (source, target, weight)
                                # print (f'node = {node}, vertex = {vertex}, edges = {edges}')
                                # print (f'Minimum edge weight is graph[{minimumEdge[0]}][{minimumEdge[1]}]={minimumEdge[2]}')
        print (f'Final minimum edge is {minimumEdge}\n')
        return minimumEdge

    def print(self):
        print(self.nodes)

def boruvka(graph, debug=False):
    """
    Computes MST using Boruvska's algorithm.
    Assumes all edges are distinct. 

    Parameters
    ----------
    n : int
        number of vertices 
    edges : list[list]
        weighted undirected connected graph
    """

    numberOfEdges = graph.getNumberOfVertices()

    # Initialize a forest F to (V, E') where E' = {}.
    connectedComponents = ConnectedComponents(numberOfEdges)

    # Stores the resulting minimum spanning tree
    minimumSpanningTree = Graph(numberOfEdges)

    # Iterate until there are independently connected components
    while len(connectedComponents.nodes) > 1:

        try:
            # Select the minimum-weight edge
            minimumEdgeWeightSource, minimumEdgeWeightTarget, minimumEdgeWeight = \
                connectedComponents.getMinimumWeightedEdges(graph, debug)
            
            # Edge Contraction: an edge is chosen from the graph and a new node is formed with the union 
            # of the connectivity of the incident nodes of the chosen edge.
            # References: https://iss.oden.utexas.edu/?p=projects/galois/analytics/mst
            connectedComponents.connect(minimumEdgeWeightSource, minimumEdgeWeightTarget)

            # Eliminate all but the lowest-weight edge among each set of multiple edges
            minimumSpanningTree.add(minimumEdgeWeightSource, minimumEdgeWeightTarget, minimumEdgeWeight)
        except:
            return -1
    
    # Return the weight of the MST 
    return minimumSpanningTree.totalWeight

def driver(n, edges):
    debug = False
    debugIndex = 1

    graph = Graph(n)
    
    # Build the graph
    for i in range(0, len(edges)):
        source, target, weight = edges[i]
        graph.add(source, target, weight)
        # print (f'source: {source}, target: {target}')

    criticalEdge = set()
    pseudoCriticalEdge = set()
    mstAllEdges = boruvka(graph, debug)
    assert(mstAllEdges == 7)

    for i in range(0, len(edges)):
        edge = edges[i]
        source, target, weight = edge
        graph.deleteEdge(source, target)

        mstWithoutOneEdge = boruvka(graph, debug=(True if i == debugIndex else False))
        print (f'MST Weight is = {mstWithoutOneEdge} for i = {i} \n')
        # graph.print() 

        assert((mstWithoutOneEdge == 8 if i == 0 else True))
        assert((mstWithoutOneEdge == 7 if i == 1 else True))

        if mstWithoutOneEdge > mstAllEdges or mstWithoutOneEdge == -1:
            criticalEdge.add(i)
        elif mstWithoutOneEdge == mstAllEdges:
            pseudoCriticalEdge.add(i)
        
        graph.add(source, target, weight)

    return {'critical': criticalEdge, 'pseudoCritical': pseudoCriticalEdge}

if __name__ == "__main__":
    edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
    n = 5
    mst = driver(n, edges)
    print (mst)
