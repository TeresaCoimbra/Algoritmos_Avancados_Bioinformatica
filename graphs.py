###########################################################################################
##                                       MyGraph
## Here a graph is represented as an adjacency list using a dictionary.
## The keys are vertices.
## The  values of the dictionary represent the list of adjacent vertices of the key node.
###########################################################################################
class MyGraph:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origin, destination) '''
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v,d))                                     # v is an origin and d a destination
        return edges
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():                                  
            self.graph[v] = []
        
    def add_edge(self, o, d):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        if d not in self.graph[o]:                                       # if d not in the list of o
            self.graph[o].append(d)                                      # append d

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        return list(self.graph[v])                                       # needed to avoid list being overwritten of result of the function is used
             
    def get_predecessors(self, v):
        '''Returns the list of predecessors of node v.
        Go through keys. If v is in the respective list the key will be append to res'''
        res = []
        for k,val in self.graph.items():
            if v in val:
                res.append(k)
        return res
                
    
    def get_adjacents(self, v):
        '''Returns the list of adjacent nodes to the input node v.'''
        # nodes are adjacent if they are successors or predecessors of v
        suc = self.get_successors(v)
        res_adj = self.get_predecessors(v)
        for i in suc:
            if i not in res_adj: res_adj.append(i)
        return res_adj
    
    def get_adjacents_2(self, v):
        '''Returns the list of adjacent nodes to the input node v, using sets instead of lists.'''
        # nodes are adjacent if they are successors or predecessors of v
        suc = set(self.get_successors(v))
        res_adj = set(self.get_predecessors(v))
        res = suc.union(res_adj)
        return list(res)
        
    ## degrees    
    
    def out_degree(self, v):
       '''Calculates the out degree of a node.
       
        Parameters
        ----------
        v : int
            Input node.

        Returns
        -------
        Out degree of the node v : int
             The number of out connections or successors of the node.
            
       '''

       # return len(self.get_successors(v)))
       return len(self.graph[v])
   
            
    def in_degree(self, v):
        '''Calculates the in degree of a node. 
       
        Parameters
        ----------
        v : int
            Input node.

        Returns
        -------
        In degree of the node v :int
             The number of predecessors of the node.
        '''
        return len(self.get_predecessors(v))
   
    def degree(self, v):
        '''Calculates the degree of a node. 
       
        Parameters
        ----------
        v : int
            Input node.

        Returns
        -------
        Degree of the node v : int
            The same connection is not counted twice. 
            By using get_adjacents this is avoided since there are no repetitions of nodes. 
        '''
        return len(self.get_adjacents(v))
        
    
    ## BFS and DFS searches    
    # These are different in their last steps. 
    # l has all the nodes that weren't seen
    # res - all that has been visited
    def reachable_bfs(self, v):
        l = [v]                                                               # to visit
        res = []                                                              # visited
        while len(l) > 0:                                                     # ends when there are no more nodes to visit
            node = l.pop(0)                                                   # get the first element
            if node != v: res.append(node)                                    # append node to the list
            for elem in self.graph[node]:                        
                if elem not in res and elem not in l and elem != node:        # if they are not in l and != from node
                    l.append(elem) 
        # queue because I add to the end of the list and remove from the beggining
        return res
        
    def reachable_dfs(self, v):
        # similar to the previous but implementing stacks instead of queues
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res    
    
    def distance(self, s, d):
        '''
        Receives two nodes s (int) and d (int).
        Returns distance between input nodes.'''
        if s == d: return 0
        l = [(s,0)]                             # l is a list of tuples, with node and distance
        visited = [s]                           # Will be the result. Keeps the visited nodes. The first node visited is s.
        while len(l) > 0:                       # while there are nodes to visit
            node, dist = l.pop(0)               # first element of l --> pop the tuple (node,dist) 
            for elem in self.graph[node]:       # if the element is a successor
                if elem == d: return dist+1     #  and the successor is the element we want to search - the element is at a dist from the origin which is dist from node +1
                elif elem not in visited:       # if the element was not visited
                    l.append((elem,dist+1))     # element needs to be visited
                    visited.append(elem)
        return None
    
    def shortest_path(self, s, d):
        '''Returns the whole shortest path between s and d'''
        if s == d: return [s,d]
        l = [(s,[])]
        visited = [s]
        while len(l) > 0:
            node, pred = l.pop(0)
            for elem in self.graph[node]:       # for element in the list 
                if elem == d:                   # join to the previous path the currently observed node 
                    return pred + [node,elem]
                elif elem not in visited:
                    l.append((elem, pred+[node,elem]))
                    visited.append(elem)
        return None


    def reachable_with_dist(self, s):
        '''
        Stores tuple with element and distance, combining the two previous functions. 
        List of all visited nodes and distance. 
        It ill go through all the nodes and save the distance. 
        '''
        res = []
        l = [(s,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != s: res.append((node,dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,elem): 
                    l.append((elem,dist+1))
        return res

## cycles


    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True    # when the element is found, it has a cycle
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res                           # if it goes through all the tree - there are no cycles

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print('Nodes:')
    print (gr.get_nodes())
    print('Edges:')
    print (gr.get_edges())
    # greates a directed graph 
    

def test2():
    gr2 = MyGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print('*******************')
    gr.print_graph()
    print('Successors')
    print ('Successors of 2:', gr.get_successors(2))
    print('Predecessors')
    print ('Predecessors of 2:', gr.get_predecessors(2))
    print ('Adjacents', gr.get_adjacents(2))
    print ('In degree of node 2:', gr.in_degree(2))
    print('Out degree of node 2:',gr.out_degree(2))
    # print ('Degree:',gr.degree(2))

def test4():
    print('****************************************')
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print ('Distance between 1 and 4:', gr.distance(1,4))
    print ('Distance between 4 and 3:', gr.distance(4,3))

    print ('Shortest path between 1 and 4',gr.shortest_path(1,4))
#     print (gr.shortest_path(4,3))

#     print (gr.reachable_with_dist(1))
#     print (gr.reachable_with_dist(3))

#     gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    
#     print (gr2.distance(2,1))
#     print (gr2.distance(1,5))
    
#     print (gr2.shortest_path(1,5))
#     print (gr2.shortest_path(2,1))

#     print (gr2.reachable_with_dist(1))
#     print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    print (gr2. node_has_cycle(1))
    print (gr2.has_cycle())


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    #test5()
