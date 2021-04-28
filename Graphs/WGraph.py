#####################################################################################
#                        WGraph - Weighted Graph       
#
# Weighted Graph structure example: {node1 : [(node2, wheight1-2), (node3, weight1-3)]}
# Each edge has a numerical weight assotiated with it. 
# Incomplete class.
######################################################################################

class WGraph:
    
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
        for v in self.graph.keys():                                     # for each key in the dict
            for d in self.graph[v]:                                     # for each corresponding tuple (Node,Weight)
                edges.append((v,d[0]))                                  # v is an origin and d a destination, d[0] is the node
        return edges

    ## weights
    
    def get_weight(self, v, d):
      '''Given a node v (int), and its destination node
      Returns the corresponding weight (int)'''
      w = 0
      for t in self.graph[v]:                                           
          if t[0] == d:
              w = t[1]
      return w


    ## size 

    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():                                  
            self.graph[v] = []
        
    def add_edge(self, o, d, w):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph, as well as the corresponding weight w ''' 
        if o not in self.graph.keys():
            self.add_vertex(o)
            
        if d not in self.graph.keys():
            self.add_vertex(d)
        
        d_nodes = self.get_successors(o)                                  # list of nodes that are contained in the list of o tuples
 
        if d not in d_nodes:                                              # if d is not in the list of the tuples of o
            self.graph[o].append((d,w))                                   # append d and the corresponding weight w

    ## successors, predecessors, adjacent nodes
        
    def get_successors(self, v):
        '''Given a node v (int), returns its destination nodes (list)'''
        nodes = []                                                        # list of nodes that are contained in the list of v's tuples
        for t in self.graph[v]:                                           # t is a tuple of the list of v
            if t[0] not in nodes: 
                nodes.append(t[0])
        return nodes

    def get_predecessors(self, d):
        '''Returns the list of predecessors of node d.
        Go through keys. If d is in the respective list the key will be append to res'''
        res = []
        for k,T in self.graph.items():                                   # for key : [tuple,tuple1]
            for t in T:                                                  # for each tuple in the list
                if d in t[0]:                                            # if d is one of the first elements of the list
                    res.append(k)                                        # append the corresponding key
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

       return len(self.get_successors(v))
   
            
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
    

def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: return True
    return res


def test1():
    gr = WGraph( {1:[(2,3)], 2:[(3,5)], 3:[(2,4),(4,2)], 4:[(2,6)]} )
    gr.print_graph()
    print('Nodes:')
    print (gr.get_nodes())
    print('Edges:')
    print (gr.get_edges())
        

def test2():
    gr2 = WGraph()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    # add_edge receives 3 params: vertex, destination node, weight
    gr2.add_edge(1,2,3)
    gr2.add_edge(2,3,5)
    gr2.add_edge(3,2,4)
    gr2.add_edge(3,4,2)
    gr2.add_edge(4,2,6)
    print('\nSecond test:\n')
    gr2.print_graph()

if __name__ == "__main__":
    test1()
    test2()
  
