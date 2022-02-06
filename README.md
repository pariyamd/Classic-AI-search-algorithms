# classic-AI-search-algorithms

## Search algorithms
### IDS (Iterative deepening depth-first search)
To implement this algorithm, we used the ids function to execute dfs with limited depth. The initial depth and maximum depth can be determined from the Graph class fields. Also, the recursive dfs algorithm is implemented. (The implemented dfs search is a tree search).
### A* 
To implement this algorithm, we need to determine an acceptable heuristic function that optimistically guesses the cost to the destination. The function works by comparing the queue of each case with each of the target cases and the minimum between these numbers is returned as the heuristic value of a node.
Suppose the initial state has maximum displacements relative to one of the targets, ie row x col - 1 misplacements. It is clear that in order to achieve that goal, we have to move each person at least once with Jafar, and this number of transfers is certainly less than the cost of reaching that goal, so at least these transfers are less than the actual cost. Therefore, the heuristic is acceptable.
There are other acceptable heuristic functions, such as measuring each person's Manhattan distance to the correct location in the target and adding this distance to each person, but finding the corresponding place for each person in the final case is costly.
After the heuristic function is selected, we consider a parameter called _g_ showing the path's cost in each node, then we dequeue a node with the lowest f = g + h or the cost to extend and run the target test each time.


### Two-way search algorithm
To run this algorithm, which is described in the product_goal method, we first generate nodes for each of the target scenarios, and then we place the hypothetical nodes as the parent of these nodes. Subsequently, we run two bfs algorithms asynchronously, starting from the hypothetical nodes.
The target test is performed when the node is expanded, and when a node from one of the bfs runs is found in another's frontier set, that node and its corresponding node in another frontier are returned to print the path to the target using their parents.

## Comparison


|  | Iterative deepening search | A* search| Bidirectional search|
| ------ | ------ | ------ | ------ |
| Time complexity | <img src="https://render.githubusercontent.com/render/math?math=O(b^d)">|<img src="https://render.githubusercontent.com/render/math?math=O(log h*(n))">|<img src="https://render.githubusercontent.com/render/math?math=O(b^{d/2})">|
| Space complexity |  <img src="https://render.githubusercontent.com/render/math?math=O(bd)">|<img src="https://render.githubusercontent.com/render/math?math=O(b^d)">|<img src="https://render.githubusercontent.com/render/math?math=O(b^{d/2})">|

