'''
This file contains the Graph class and the Solution class to find critical and pseudocritical edges. 
The driver function for these classes is inside main.py. 
The code is written in Python and can be run using Python and Python3 as languages on Leetcode.

https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/

Due to a known bug on Leetcode, this code may not be accepted on the first run. However, here's proof of 
submission: https://leetcode.com/submissions/detail/833716528/
'''

class Graph:
    def __init__(self, n):
        self.graph = []
        self.parent = []
        self.closest = []
        self.weight = 0
        self.numberOfVertices = n

    def addEdge(self, edge):
        '''Adds an edge into the graph.'''
        _, _, w = edge
        self.graph.append(edge)
        self.weight += w

    def countComponents(self, n, edges):
        ''' Checks for connectivity inside a graph. Since Boruvka only works on connected graphs,
        if the number of connected components != 1, then the MST cannot be formed and
        we can add edge into the critical list. '''

        adj = dict()
        visited = [False] * n
        connectedComponents = 0

        for edge in edges:
            u, v, w = edge
            if u in adj:
                adj[u].append(v)
            else:
                adj[u] = [v]

            if v in adj:
                adj[v].append(u)
            else:
                adj[v] = [u]

        # If there are less vertices in the adjacency list than n, then a graph is not 
        # possible, return -1. 
        if len(adj) < n:
            return -1

        for i in range(0, n):
            if visited[i] == False:
                connectedComponents += 1
                self.dfs(adj, visited, i)

        return connectedComponents

    def dfs(self, adj, visited, i):
        if visited[i]:
            return
        visited[i] = True

        for j in range(0, len(adj[i])):
            self.dfs(adj, visited, adj[i][j])

    def find(self, u):
        '''The find operation will return the parent of the node being requested.'''
        if self.parent[u] == u:
            return u
        return self.find(self.parent[u])

    def union(self, u, v):
        '''If u and v belong to different subsets, then, we will unify them by
        setting u as the parent of v. '''
        rootU = self.find(u)
        rootV = self.find(v)

        if rootU != rootV:
            self.parent[rootU] = rootV
        else:
            return -1

    def isPreferredOver(self, parentSet, w):
        '''Compares the weight between current cheapest edge and the next edge.
        We're essentially computing if the cheapest edge is preferred over the current edge.
        '''
        if not parentSet or parentSet[2] > w:
            return True
        return False

    def boruvka(self, pick, skip):
        ''' The pseudocode for this algorithm is from Dr. Gopal's book. An explanation 
        is inside the report submitted with this code.'''
        
        # This is the number of independent forest at the beginning of the algorithm.
        # As edges are contracted, the number of vertices left to process are reduced.
        numberOfVertices = self.numberOfVertices

        # By default, none of the vertices are close/cheapest to each other
        defaultClosestCost = None

        # This MST will be used to store the minimum weighted edge 
        # and return the overall weight at the end. 
        mst = Graph(numberOfVertices)

        # Force the addition of an edge into the mst.
        if pick:
            mst.addEdge(pick)
            u, v, w = pick
            self.union(u, v)
            numberOfVertices -= 1

        # Before running Boruvka, we've checked that the graph is connected, therefore,
        # this while loop will never fail.
        while numberOfVertices > 1:

            # We will store closest edge (minimum weighted edges) inside the
            # closest array instead of building a new MST to save on time. 
            # Because each edge has it's own set of cheaply-distant edges, we must 
            # reset the cheap array for each iteration.
            self.closest = [defaultClosestCost for x in range(0, self.numberOfVertices)]

            # Select the minimum-weight edge incident on v
            for edge in self.graph:

                # Ignore the skipped edge and move onto the next.
                if skip and edge == skip:
                    continue
                
                # let the current edge be the cheapest edge for the component of u
                u, v, w = edge
                # Compute subsets in which u and v belong.
                rep1 = self.find(u)
                rep2 = self.find(v)

                if rep1 != rep2:

                    # The cheapest edge going out from a tree T is the cheapest edge between T and "the outside world"
                    # By the cut-edge property, it must be in the MST.

                    # For each tree in the connected components, find the closest edge.

                    wu = self.closest[rep1]
                    # Check if the current cheapest edge exists or is cheap than the current edge
                    if not wu or self.isPreferredOver(wu, w):
                        # The current edge is cheaper than the previous cheap edge, update cheapest
                        self.closest[rep1] = edge
                    
                    wv = self.closest[rep2]
                    if not wv or self.isPreferredOver(wv, w):
                        self.closest[rep2] = edge

                else:
                    # u and v belong to the same component
                    continue

            # Perform edge contraction on the cheapest vertices without self-loops
            for i in range(0, self.numberOfVertices):

                edge = self.closest[i]

                # If all components have cheapest edge set to "None" then no more trees
                # can be merged, so we check for that first. 
                if edge and edge != skip:
                    u, v, w = edge

                    # Eliminate all but the lowest-weight edge among each set of multiple edges.
                    if self.union(u, v) != -1:
                        # Since we contracted on the two edges, we can safely reduce the number of
                        # vertices left to process.
                        numberOfVertices -= 1
                        mst.addEdge(edge)

        # return weight of selected as MST edges
        return mst.weight


class Solution():
    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        g = Graph(n)

        critical = []
        pseudocritical = []

        # Build the graph
        for edge in edges:
            g.addEdge(edge)

        edgeIndex = 0

        # The MST of the graph including all edges will be used as a threshold to determine
        # if edges are critical or pseudocritical. 
        
        # Each vertex is it's own parent.
        g.parent = [i for i in range(0, n)]
        overall = g.boruvka(None, None)

        for e in range(0, len(edges)):
            edge = edges[e]

            # Since we're dealing with the same graph three times (mst on all edges, mst on one picked edge, and mst
            # on a skipped edge), we must reset it's parent every time to save time on creating a new graph.
            g.parent = [i for i in range(0, n)]
            pick = g.boruvka(edge, None)

            # Create a temporary graph with all edges except the current one. 
            if e != 0:
                tempG = edges[:e] + edges[e+1:]
            else:
                tempG = edges[e+1:]

            # An MST cannot be formed by skipping the current edge, therefore, this edge 
            # is critical. 
            if g.countComponents(n, tempG) != 1:
                critical.append(edgeIndex)
                edgeIndex += 1
                continue

            g.parent = [i for i in range(0, n)]
            skip = g.boruvka(None, edge)

            # Skipping this edge causes the overall weight to increase, therefore,
            # it is critical.
            if skip > overall:
                critical.append(edgeIndex)
            
            # Forcing the inclusion of this weight has no effect on the MST, therefore,
            # it is pseudocritical. 
            elif pick == overall:
                pseudocritical.append(edgeIndex)

            edgeIndex += 1

        return ([critical, pseudocritical])
