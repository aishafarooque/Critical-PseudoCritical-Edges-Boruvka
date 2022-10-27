# Boruvka's algorithm to find Minimum Spanning
# Tree of a given connected, undirected and weighted graph

#Class to represent a graph
import collections

class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.adjacencyList = [[-1 for _ in range(n)] for _ in range(n)]
        self.graph = []  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
    
    def getEdge(self, u, v):
        try:
            return self.adjacencyList[u][v]
        except:
            return -1
            
    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        # print (f'Finding {i} in {parent}')
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        # Attach smaller rank tree under root of high rank tree
        # (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        #If ranks are same, then make one as root and increment
        # its rank by one
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def connected_components(self, neighbors):
        seen = set()
        def component(node):
            nodes = set([node])
            while nodes:
                node = nodes.pop()
                seen.add(node)
                nodes |= neighbors[node] - seen
                yield node
        for node in neighbors:
            if node not in seen:
                yield component(node)

    
    def checkGraphConnectivity(self, edges, n):

        graph = collections.defaultdict(set)

        for v1, v2, _ in edges:
            graph[v1].add(v2)
            graph[v2].add(v1)
        
        if len(graph) < n:
            return -1 

        components = []
        for component in self.connected_components(graph):
            c = set(component)
            components.append([e for e in edges
                                    if c.intersection(e)])

        return (len(components))

    # The main function to construct MST using Kruskal's algorithm
    def boruvkaMST(self, pick, skip):
        parent = []
        rank = []

        # An array to store index of the cheapest edge of
        # subset. It store [u,v,w] for each component
        cheapest = []

        # Initially there are V different trees.
        # Finally there will be one tree that will be MST
        numTrees = self.V
        MSTweight = 0

        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            cheapest = [-1] * self.V

        # Keep combining components (or sets) until all
        # components are not combined into single MST
        while numTrees > 1:

            # Traverse through all edges and update
            # cheapest of every component
            for i in range(len(self.graph)):

                numberOfUnknowns = 0

                # Find components (or sets) of two corners
                # of current edge
                u, v, w = self.graph[i]
                set1 = self.find(parent, u)
                set2 = self.find(parent, v)

                # if (2,3) == skip:
                    # print (f'pick: {pick}, skip: {skip}, parent: {parent}')
                    # print (f'u: {u}, v: {v}, set1: {set1}, set2: {set2}, cheapest: {cheapest}\n')
                    # previousEdge = self.graph[i-1]
                    # nextEdge = self.graph[i+1]
                    # if self.getEdge(previousEdge[0], nextEdge[0]) == -1:
                    #     return -1

                if pick and self.graph[i] == pick:
                    cheapest[set1] = [u, v, w]
                    cheapest[set2] = [u, v, w]
                
                if skip and self.graph[i] == skip:
                      continue  

                # If two corners of current edge belong to
                # same set, ignore current edge. Else check if
                # current edge is closer to previous
                # cheapest edges of set1 and set2
                if set1 != set2:

                    if cheapest[set1] == -1 or cheapest[set1][2] > w:
                        # print ('set 1 ', set1)  
                        cheapest[set1] = [u, v, w]

                    if cheapest[set2] == -1 or cheapest[set2][2] > w:
                        # print ('set 2 ', set2)
                        cheapest[set2] = [u, v, w] 

            if pick:
                u, v, w = pick
                set1 = self.find(parent, u)
                set2 = self.find(parent, v)
                self.union(parent, rank, set1, set2)
                MSTweight += w
                numTrees -= 1

            # Consider the above picked cheapest edges and add them
            # to MST
            for node in range(self.V):

                #Check if cheapest for current set exists
                if cheapest[node] != -1:
                    u, v, w = cheapest[node]
                    set1 = self.find(parent, u)
                    set2 = self.find(parent, v)

                    if set1 != set2:
                        MSTweight += w
                        self.union(parent, rank, set1, set2)
                        # print("Edge %d-%d with weight %d included in MST" % (u, v, w))
                        numTrees = numTrees - 1
            
            #reset cheapest array
            cheapest = [-1] * self.V

        # print("Weight of MST is %d" % MSTweight)
        return MSTweight

if __name__ == "__main__":
    edges = [[0,1,13],[0,2,6],[2,3,13],[3,4,4],[0,5,11],[4,6,14],[4,7,8],[2,8,6],[4,9,6],[7,10,4],[5,11,3],[6,12,7],[12,13,9],[7,13,2],[5,13,10],[0,6,4],[2,7,3],[0,7,8],[1,12,9],[10,12,11],[1,2,7],[1,3,10],[3,10,6],[6,10,4],[4,8,5],[1,13,4],[11,13,8],[2,12,10],[5,8,1],[3,7,6],[7,12,12],[1,7,9],[5,9,1],[2,13,10],[10,11,4],[3,5,10],[6,11,14],[5,12,3],[0,8,13],[8,9,1],[3,6,8],[0,3,4],[2,9,6],[0,11,4],[2,5,14],[4,11,2],[7,11,11],[1,11,6],[2,10,12],[0,13,4],[3,9,9],[4,12,3],[6,7,10],[6,8,13],[9,11,3],[1,6,2],[2,4,12],[0,10,3],[3,12,1],[3,8,12],[1,8,6],[8,13,2],[10,13,12],[9,13,11],[2,11,14],[5,10,9],[5,6,10],[2,6,9],[4,10,7],[3,13,10],[4,13,3],[3,11,9],[7,9,14],[6,9,5],[1,5,12],[4,5,3],[11,12,3],[0,4,8],[5,7,8],[9,12,13],[8,12,12],[1,10,6],[1,9,9],[7,8,9],[9,10,13],[8,11,3],[6,13,7],[0,12,10],[1,4,8],[8,10,2]]
    n = 14
    # edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]
    # n = 5
    
    g = Graph(n)
    critical = []
    pseudocritical = []

    for source, target, weight in edges:
        g.addEdge(source, target, weight)

    i = 0
    overall = g.boruvkaMST(None, None)

    # print (overall)

    for e in range(0, len(edges)):
        edge = edges[e]
        pick = g.boruvkaMST(edge, None)

        if e != 0:
            tempG = edges[:e] + edges[e+1:]
        else:
            tempG = edges[e+1:]

        if g.checkGraphConnectivity(tempG, n) != 1:
            critical.append(i)
            i += 1
            continue

        skip = g.boruvkaMST(None, edge)

        if skip > overall:
            critical.append(i)

        elif pick == overall:
            pseudocritical.append(i)
        
        if i == 15:
            print (i, pick, skip)
        
        i += 1

    print ([critical,pseudocritical])
