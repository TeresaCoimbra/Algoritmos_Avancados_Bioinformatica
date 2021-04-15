###################################################################################################################
#                          Suffix Tree
#
# Used for pre-processing the sequence (instead of the pattern) and to search for repeats of patterns in sequences. 
# A type of trie built from the set of suffixes found in the target sequence.
# 
#
###################################################################################################################
class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) }                                         # root node: a node corresponds to a tuple
        self.num = 0
    
    def print_tree(self):
        for k in self.nodes.keys():
            if self.nodes[k][0] < 0:
                print (k, "->", self.nodes[k][1]) 
            else:
                print (k, ":", self.nodes[k][0])
                
    def add_node(self, origin, symbol, leafnum = -1):
        '''
        Adds a new node by receiving an origin, a symbol and the leaf number, if it is a leaf.
        The number of the new node will be num+1. 
        
        Parameters
        ----------
        origin  : int      
        symbol  : str
        leafnum : int 
        '''
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p, sufnum):
        '''
        Adds a sufix to the tree. 
        
        Parameters
        ----------
        p      : str      
        sufnum : int
        '''
        pos = 0
        node = 0
        while pos < len(p):                                           
            if p[pos] not in self.nodes[node][1].keys():                   # check if the symbol is not on the tree ([1] because the dict is the 2nd element of the tuple)
                if pos == len(p)-1:                                        # if it's the last position: it's a leaf
                    self.add_node(node, p[pos],sufnum)                     # add the position of the suffix
                else:                                                      # if it's not a leaf
                    self.add_node(node, p[pos])                            # the sufnum is the default = -1
            node = self.nodes[node][1][p[pos]]
            pos += 1
    
    def suffix_tree_from_seq(self, text):
        '''
        Adds the symbol $ to the sequence and calls self.add_suffix for each suffix of the sequence. 
        
        Parameter
        ----------
        text : str 
        
        '''
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)
    
    def find_pattern(self, pattern):
        '''
        Search for the pattern in the tree. 
        If the pattern is found, the leaves bellow the node are return by calling self.get_leafes_below().
        Else, the search fails, returning None. 
     
        Parameter
        ----------
        pattern : str 
        
        Returns
        ----------
        List of the position where the pattern occurs or None if no matches where found.
        '''
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
                pos += 1
            else: return None
        return self.get_leafes_below(node)
    

    def get_leafes_below(self, node):
        '''
        Colects the leaves under a given node.
        
        Parameter
        ----------
        node : int
        
        Returns
        ----------
        res : list
            List of the leaves bellow a node.
        
        '''
        res = []                                                           # res will be the list of leaves bellow the node
        if self.nodes[node][0] >=0:                                        # if it's a leaf
            res.append(self.nodes[node][0])                                
        else:                                                              # if it's not a leaf
            for k in self.nodes[node][1].keys():                           # for each key (symbol)
                newnode = self.nodes[node][1][k]                          
                leaves = self.get_leafes_below(newnode)
                res.extend(leaves)                                         # adds the elements of 'leaves' to res
        return res
##############################################################################################################################3
# ex1 

    def nodes_bellow(self, node):
        '''
        Given a node, returns the list of the identifiers of the nodes bellow. 
        
        Parameter
        ----------
        node : int
        
        Returns
        ----------
        res : list
            List of the identifiers bellow a node.

        '''
        res = [node]
        for n in res:
            if self.nodes[n][0] <0:                                         # if it's not a leaf
                for v in self.nodes[n][1].values():                         # for each key in the dictionary inside the tuple
                    res.append(v)                                           # new node is the corresponding value   
        return sorted(res[1::])                                             # remove the first, because it corresponds to the node itself
      
                                
 #############################################################33333
    def matches_prefix (self, prefix):
        '''
        Verifies all of the patterns that start with a certain prefix, that are contained
        within the sequence that originated the suffix tree. 

        Parameters
        ----------
        prefix : str

        Returns
        -------
        res: list
            List of all the patterns that beggin with prefix that are contained
            within the sequence that originated the tree. 

        '''
        res1 = []
        lpos = self.find_pattern(prefix)                                      # find_pattern returns a list with the leaves where the pattern was found
        # starting at the positions where the pattern was found go through the tree 
        finish_nodes = []                                                     # finish_nodes will have the nodes where the interesting leaves where found
        for node in self.nodes.keys():
            if self.nodes[node][0] in lpos: 
                finish_nodes.append(node)
      
        
        bellow = self.nodes_bellow(lpos[0])                                   # nodes bellow
        
        if bellow[0] == 1:
            bellow.insert(0,0)                                                # insert the starting position
            
      
        p = ''                                                                # pattern found
        
        # pattern will go from start node to finishing nodes, going through all of the nodes bellow
      
        for n in bellow: 
            if (n not in finish_nodes):
                for k in self.nodes[n][1].keys():                             # for each value 
                    if k != '$': 
                        p += k  
                    res1.append(p)
            else:
                break
        
        # process the result
        res = []
        for seq in res1:
            if len(seq) >= len(prefix) and (seq not in res):                  # remove sequences shorter than prefix and avoid repetitions
                res.append(seq)                                        
        return res
 ###################################################################
    
def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))
    print('Leaves:', st.get_leafes_below(0))
    print('nodes:' , st.nodes_bellow(0))
    print(st.get_leafes_below(7))
    print(st.nodes_bellow(7))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    #print(st.repeats(2,2))

test()
print()
#test2()
        
            
    
    
