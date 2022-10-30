import collections

'''
Referenced - 
https://iss.oden.utexas.edu/?p=projects/galois/analytics/mst
https://stanford.edu/~rezab/classes/cme323/S15/projects/parallel_union_find_report.pdf

'''

class Graph:
    def __init__(self, n):
        self.graph = []
        self.parent = []
        self.cheapest = []
        self.weight = 0
        self.numberOfVertices = n
    
    def addEdge(self, edge):
        '''
        Adds an edge into the graph.
        '''
        _, _, w = edge
        self.graph.append(edge)
        self.weight += w
    
    def connected_components(self, neighbors):
        '''
        Returns the number of connected nodes inside the edges. 
        Source: https://stackoverflow.com/questions/10301000/how-to-find-connected-components 
        '''

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
        '''
        Returns the number of connected nodes inside the edges. 
        Source: https://stackoverflow.com/questions/10301000/how-to-find-connected-components 
        '''
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
    
    def find(self, u):
        '''

        The find operation will return the root of the node being requested. 
        The root for each node is stored inside the parents array.

        Reference - 
            Parallelized Union Find Set, with an Application in Finding 
            Connected Components in a Graph

            Source: https://stanford.edu/~rezab/classes/cme323/S15/projects/parallel_union_find_report.pdf

        '''
        if self.parent[u] == u:
            return u
        return self.find(self.parent[u])

    def union(self, rank, u, v):
        '''
        When there is a request to union the sets containing node x and node y, the
        algorithm first find the roots of x and y. If the root of x is different from the root of
        y, one of their parent will be set to the other.

        Reference - 
            Parallelized Union Find Set, with an Application in Finding 
            Connected Components in a Graph

            Source: https://stanford.edu/~rezab/classes/cme323/S15/projects/parallel_union_find_report.pdf
        '''
        rootU = self.find(u)
        rootV = self.find(v)

        if rootU != rootV:
            rankU = rank[rootU]
            rankV = rank[rootV]

            if rankU > rankV:
                self.parent[rootV] = rootU
            elif rankU < rankV:
                self.parent[rootU] = rootV
            else:
                self.parent[rootU] = rootV
                rank[rootV] = rank[rootV] + 1
        else:
            return -1
    
    def less(self, u, v):
        '''
        Compares two nodes and returns true/false is u > v.
        '''
        return u > v

    def boruvka(self, pick, skip):

        numberOfVertices = self.numberOfVertices
        self.cheapest = [-1] * numberOfVertices
        rank = [0] * numberOfVertices

        mst = Graph(numberOfVertices)

        # Each vertex is it's own parent. 
        for i in range(0, numberOfVertices):
            self.parent.append(i)
        
        # Force the addition of an edge into the mst. 
        if pick:
            mst.addEdge(pick)
            u,v,w = pick
            self.union(rank, u, v)
            numberOfVertices -= 1
        
        # Before running Boruvka, we've checked that the graph is connected, therefore,
        # this while loop will never fail. 
        while numberOfVertices > 1:
            
            # Select the minimum-weight edge incident on v
            for edge in self.graph:
                
                # Ignore the skipped edge and move onto the next.
                if skip and edge == skip:
                    continue
                
                # Compute subsets in which u and v belong. 
                u,v,w = edge
                rep1 = self.find(u)
                rep2 = self.find(v)

                if rep1 != rep2:
                    
                    # The cheapest edge going out from a tree T is the cheapest edge between T and "the outside world"
                    # By the cut-edge property, it must be in the MST.
                    # Source: https://www2.seas.gwu.edu/~simhaweb/champalg/mst/mst.html
                    # https://courses.engr.illinois.edu/cs374/fa2015/slides/18-mst.pdf 
                    
                    # For each tree in the connected components, find the closest edge
                    if self.cheapest[rep1] == -1 or self.less(self.cheapest[rep1][2], w):
                        self.cheapest[rep1] = edge

                    if self.cheapest[rep2] == -1 or self.less(self.cheapest[rep2][2], w):
                        self.cheapest[rep2] = edge

                else:
                    # u and v belong to the same component
                    continue

            # Perform edge contraction on the cheapest vertices without self-loops
            for i in range(0, self.numberOfVertices):

                edge = self.cheapest[i]

                if edge and edge != -1:
                    u,v,w = edge

                    # Eliminate all but the lowest-weight edge among each set of multiple edges.
                    # Note - This find operation is doubled here. It is performed once again in the union operation.
                    # It can be safely removed from here, but LeetCode does not accept it (produces a time limit 
                    # exceed error).
                    if self.find(u) != self.find(v):
                        mst.addEdge(edge)
                        self.union(rank, u, v)

                        # Since we contracted on the two edges, we can safely reduce the number of 
                        # vertices left to process.
                        numberOfVertices -= 1
            
            # Because each edge has it's own set of cheaply-distant edges, we must reset the cheap array for each 
            # iteration.
            self.cheapest = [-1] * self.numberOfVertices

        # return weight of selected as MST edges
        return mst.weight

class Solution():
    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        g = Graph(n)
        critical = []
        pseudocritical = []

        for edge in edges:
            g.addEdge(edge)

        i = 0
        overall = g.boruvka(None, None)

        for e in range(0, len(edges)):
            edge = edges[e]
            
            # Since we're dealing with the same graph three times (mst on all edges, mst on one picked edge, and mst
            # on a skipped edge), we must reset it's parent every time to save time on creating a new graph. 
            g.parent = []
            pick = g.boruvka(edge, None)

            if e != 0:
                tempG = edges[:e] + edges[e+1:]
            else:
                tempG = edges[e+1:]

            if g.checkGraphConnectivity(tempG, n) != 1:
                critical.append(i)
                i += 1
                continue
            g.parent = []
            skip = g.boruvka(None, edge)

            if skip > overall:
                critical.append(i)

            elif pick == overall:
                pseudocritical.append(i)

            # print (i, pick, skip) 
            i += 1

        return ([critical, pseudocritical])

if __name__ == "__main__":
    tests = [
        [
            [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2],
                [0, 4, 3], [3, 4, 3], [1, 4, 6]],
            5,
            [[0, 1], [2, 3, 4, 5]]
        ],
        [
            [[0, 1, 1], [1, 2, 1], [0, 2, 1], [2, 3, 4],
                [3, 4, 2], [3, 5, 2], [4, 5, 2]],
            6,
            [[3], [0, 1, 2, 4, 5, 6]]
        ],
        [
            [[0, 1, 1], [0, 2, 2], [0, 3, 3]],
            4,
            [[0, 1, 2], []]
        ],
        [
            [[0, 1, 5], [0, 2, 13], [0, 3, 10], [1, 4, 5], [4, 5, 6], [0, 6, 9], [4, 7, 5], [5, 8, 6], [0, 9, 8], [1, 10, 4], [0, 11, 11], [7, 12, 9], [1, 7, 2], [0, 4, 4], [7, 8, 6], [3, 4, 9], [
                1, 11, 4], [2, 11, 4], [5, 9, 3], [3, 11, 7], [4, 8, 5], [7, 11, 5], [9, 10, 7], [1, 2, 4], [2, 6, 12], [6, 7, 7], [8, 9, 6], [3, 9, 11], [1, 3, 3], [4, 12, 9], [2, 3, 11]],
            13,
            [[9, 12, 13, 18, 20, 25, 28], [0, 3, 4, 6, 7, 11, 16, 17, 23, 26, 29]]
        ],
        [
            [[0, 1, 13], [0, 2, 6], [2, 3, 13], [3, 4, 4], [0, 5, 11], [4, 6, 14], [4, 7, 8], [2, 8, 6], [4, 9, 6], [7, 10, 4], [5, 11, 3], [6, 12, 7], [12, 13, 9], [7, 13, 2], [5, 13, 10], [0, 6, 4], [2, 7, 3], [0, 7, 8], [1, 12, 9], [10, 12, 11], [1, 2, 7], [1, 3, 10], [3, 10, 6], [6, 10, 4], [4, 8, 5], [1, 13, 4], [11, 13, 8], [2, 12, 10], [5, 8, 1], [3, 7, 6], [7, 12, 12], [1, 7, 9], [5, 9, 1], [2, 13, 10], [10, 11, 4], [3, 5, 10], [6, 11, 14], [5, 12, 3], [0, 8, 13], [8, 9, 1], [3, 6, 8], [0, 3, 4], [2, 9, 6], [0, 11, 4], [2, 5, 14], [
                4, 11, 2], [7, 11, 11], [1, 11, 6], [2, 10, 12], [0, 13, 4], [3, 9, 9], [4, 12, 3], [6, 7, 10], [6, 8, 13], [9, 11, 3], [1, 6, 2], [2, 4, 12], [0, 10, 3], [3, 12, 1], [3, 8, 12], [1, 8, 6], [8, 13, 2], [10, 13, 12], [9, 13, 11], [2, 11, 14], [5, 10, 9], [5, 6, 10], [2, 6, 9], [4, 10, 7], [3, 13, 10], [4, 13, 3], [3, 11, 9], [7, 9, 14], [6, 9, 5], [1, 5, 12], [4, 5, 3], [11, 12, 3], [0, 4, 8], [5, 7, 8], [9, 12, 13], [8, 12, 12], [1, 10, 6], [1, 9, 9], [7, 8, 9], [9, 10, 13], [8, 11, 3], [6, 13, 7], [0, 12, 10], [1, 4, 8], [8, 10, 2]],
            14,
            [[13, 16, 45, 55, 57, 58, 61, 89], [10, 15, 23,
                                                25, 28, 32, 37, 39, 51, 54, 70, 75, 76, 85]]
        ],
        [
            [[0, 1, 31], [1, 2, 35], [2, 3, 7], [3, 4, 36], [3, 5, 30], [0, 6, 8], [4, 7, 20], [4, 8, 13], [8, 9, 18], [1, 10, 33], [10, 11, 23], [4, 12, 41], [0, 13, 26], [10, 14, 17], [8, 15, 2], [6, 16, 2], [12, 17, 33], [2, 18, 41], [4, 19, 20], [11, 20, 14], [2, 21, 33], [16, 22, 17], [11, 23, 21], [21, 24, 17], [3, 25, 36], [15, 26, 20], [14, 27, 12], [10, 28, 12], [9, 29, 36], [5, 30, 16], [3, 31, 23], [24, 32, 19], [9, 33, 27], [31, 34, 15], [8, 35, 23], [26, 36, 14], [29, 37, 22], [26, 38, 33], [10, 39, 38], [10, 40, 12], [10, 15, 3], [12, 27, 29], [8, 12, 37], [12, 20, 22], [6, 19, 1], [24, 37, 5], [4, 31, 39], [14, 37, 12], [17, 29, 6], [10, 22, 27], [24, 40, 5], [27, 35, 33], [1, 11, 18], [3, 30, 2], [17, 27, 22], [17, 36, 29], [19, 33, 6], [22, 30, 25], [9, 18, 22], [0, 34, 2], [8, 33, 29], [3, 18, 13], [16, 33, 1], [2, 20, 1], [6, 9, 32], [38, 39, 29], [17, 30, 29], [11, 34, 7], [33, 34, 33], [18, 27, 19], [11, 22, 14], [20, 27, 16], [
                6, 27, 8], [12, 13, 25], [6, 15, 5], [22, 32, 23], [2, 33, 4], [18, 25, 18], [12, 19, 35], [24, 33, 39], [2, 16, 27], [8, 14, 7], [7, 34, 1], [19, 20, 32], [7, 31, 4], [8, 39, 12], [7, 8, 29], [22, 39, 4], [16, 23, 17], [6, 28, 35], [21, 38, 21], [12, 35, 34], [17, 21, 18], [2, 35, 38], [9, 10, 18], [15, 31, 20], [5, 19, 5], [12, 24, 32], [9, 23, 24], [15, 24, 31], [5, 21, 38], [27, 39, 2], [21, 23, 35], [27, 33, 21], [36, 39, 38], [4, 5, 3], [8, 18, 16], [21, 27, 41], [3, 10, 33], [13, 39, 35], [24, 30, 11], [5, 25, 12], [14, 31, 41], [3, 24, 17], [1, 7, 34], [18, 40, 39], [19, 35, 9], [27, 30, 13], [5, 35, 9], [23, 35, 16], [36, 40, 17], [30, 33, 36], [19, 22, 41], [3, 16, 4], [5, 36, 15], [17, 37, 16], [26, 39, 38], [18, 32, 29], [13, 21, 34], [20, 36, 17], [22, 28, 16], [22, 24, 30], [25, 34, 12], [22, 40, 5], [7, 21, 15], [24, 35, 14], [27, 38, 16], [12, 36, 12], [12, 33, 18], [5, 37, 38], [15, 25, 14], [25, 30, 37], [9, 27, 27]],
            41,
            [[5, 14, 15, 27, 31, 35, 40, 44, 45, 48, 50, 52, 53, 59, 61, 62, 63, 67, 72, 73, 74, 76, 81, 82,
                84, 87, 96, 101, 105, 119, 123, 124, 125, 133, 134, 136, 137], [8, 94, 111, 116, 118, 132]]
        ],
    ]

    for i in range(0, len(tests)):
        test = tests[i]
        edges, n, res = test
        solution = Solution()
        cost = solution.findCriticalAndPseudoCriticalEdges(n, edges)

        if cost != res:
            print (f'Failed {i}')
            print (cost, '\n')
            break
        else:
            print ('Passed')
