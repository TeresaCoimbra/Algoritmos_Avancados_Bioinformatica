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
            for k in self.nodes[node][1].keys():                           # check all the branches
                newnode = self.nodes[node][1][k]
                leaves = self.get_leafes_below(newnode)
                res.extend(leaves)                                         # adds the elements of 'leaves' to res
        return res

    
    
def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))

def test2():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    print (st.find_pattern("TA"))
    #print(st.repeats(2,2))

test()
print()
test2()
        
            
    
    
