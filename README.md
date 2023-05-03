# Finding Critical and Pseudocritical Edges using Boruvka's Algorithm

LeetCode: https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/

## Summary of the algorithm:

The algorithm's foundation involves calculating the Minimum Spanning Tree (MST) of each graph three times:
- MST with all edges
- MST by forcing the inclusion of the i^th edge
- MST by forcing the exclusion of the i^th edge

Critical edges are those that, when removed, result in an increased MST weight for the graph. Pseudocritical edges, on the other hand, do not impact the graph's MST weight when excluded. The outcomes of Cases 2 and 3 determine the classification of an edge based on the weight from Case 1:

- If the weight of Case 3 is greater than the weight of Case 1, the edge is considered a critical edge and added to the CriticalEdge set.
- If the weight of Case 2 equals the weight of Case 1, the edge is considered a pseudocritical edge and added to the PseudocriticalEdge set.

## Overview of the algorithm
Boruvka's algorithm is a greedy method for finding the Minimum Spanning Tree (MST) in connected graphs with distinct edge weights. The central concept involves connecting vertices using the shortest edges between each component or subset. Before executing Boruvka's algorithm, the code that identifies critical and pseudocritical edges also performs a "connected-components check" to ensure the graph's connectivity. This check guarantees that Boruvka's algorithm will not fail or get trapped in an infinite loop.

Initially, all vertices are separate components or forests, with each vertex acting as its own parent. A vertex's parent helps determine its subset membership, which is useful for edge contraction.

For every edge in the graph, we use a vertex's parent to perform a find operation and determine the subset to which it belongs. If the two vertices of an edge, u and v, belong to different subsets, we update their closest edge based on the weights connecting the subsets. By iterating through each vertex, we consider each edge, identify the cheapest edge connecting to another subset, and contract them into one subset. Each edge contraction reduces the number of subsets, initially equal to the number of vertices, by one and includes the edge in the MST.

We repeat these operations until only one subset remains, representing the minimum spanning tree. At this point, the loop will exit and return the MST's weight.
