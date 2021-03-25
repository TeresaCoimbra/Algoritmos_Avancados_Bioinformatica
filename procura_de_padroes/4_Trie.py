#######################################################################################
#                                    Trie
#
# Tries are n-ary trees where each symbol will be associated with an edge of the tree.
# Each pattern will correspond to a leaf in the the tree. 
# Here the trie is a dictionary containing several nodes. 
# Each node is a key, and the corresponding value is another dictionary with
# symbols as keys and index of destination node as value.
# A node with a label and an empty dictionary as value represents a leaf.
#######################################################################################


class Trie:
    
    def __init__(self):
        self.nodes = { 0:{} }                                                # the trie is a dictionary
        self.num = 0                                                         # current size of the tree: number of nodes
    
    def print_trie(self):
        for k in self.nodes.keys():
            print (k, "->" , self.nodes[k]) 
    
    def add_node(self, origin, symbol):
        '''
        Adds a new node by receiving an origin (the node is added, linked to an existing one) and a symbol.
        The number of the new node will be num+1. 
        
        Parameters
        ----------
        origin : int      
        symbol : str
        '''
        self.num += 1                                                        # increment 1 to num
        self.nodes[origin][symbol] = self.num                                # connect the origin (a node) to a new node
        self.nodes[self.num] = {}                                            # create the new node with an empty dict
    
    def add_pattern(self, p):
        ''' 
        Adds the pattern to the trie. 
        To add a new pattern, we go through the sequence and trie.
        
        Parameters
        ----------
        p : str
        '''
        pos = 0                                                              # to go through the pattern
        node = 0                                                             # to go through the dictionary
        while pos < len(p):                                                 
            if p[pos] not in self.nodes[node].keys():                        # if the character isn't in the keys
                self.add_node(node, p[pos])                                  # a node is added
            node = self.nodes[node][p[pos]]                                  # update of the node value with the value that corresponds to the symbol p[pos]
            pos +=1                                                          # advance in the pattern
    
    def trie_from_patterns(self, pats):
        ''' 
        Adds a set of patterns to the trie.
        
        Parameters
        ----------
        pats : list
        '''
        for padrao in pats:
            self.add_pattern(padrao)
    
    def prefix_trie_match(self, text):
        ''' 
        Search for patterns as prefixes of the sequence 'text'.
        
        Parameters
        ----------
        text : str
         
        Returns
        ----------
        pattern : str   if it was found.
        None            if it no pattern was found.
        '''
        pos = 0                                                               # starting at index 0 in the text
        match = ""                                                            # possible match 
        node = 0                                                              # starting at node 0
        while pos < len(text):
            if text[pos] in self.nodes[node].keys():                          # if the symbol is already represented there can be a pattern 
                node = self.nodes[node][text[pos]]                            # update of the node value to continue searching
                match += text[pos]                                            # include the symbol found in the match
                if self.nodes[node] == {}: return match                       # if it is an empty dict, a leaf was found, meaning: pattern was found
                else: pos += 1                                                # no leaf found, continue the search
            else: return None
        return None
        
    def trie_matches(self, text):
        ''' 
        If a pattern is represented in the trie is a prefix of the sequence (self.prefix_trie_match)
        this method will search for occurrences over the whole text. 
        
        Parameters
        ----------
        text : str
         
        Returns
        ----------
        res : list
            List of occurrences of the pattern in the text. Each occurrence is a tuple(index, pattern)
            
        '''
        res = []
        for i in range(len(text)):
            m = self.prefix_trie_match(text[i:])
            if m is not None:                                                 # if a prefix was found
                res.append((i,m))                                             # append a tuple with the position and the sequence
        return res
        
          
def test():
    patterns = ["GAT", "CCT", "GAG"]
    t = Trie()
    t.trie_from_patterns(patterns)
    t.print_trie()

   
def test2():
    patterns = ["AGAGAT", "AGC", "AGTCC", "CAGAT", "CCTA", "GAGAT", "GAT", "TC"]
    t = Trie()
    t.trie_from_patterns(patterns)
    print (t.prefix_trie_match("GAGATCCTA"))
    print (t.trie_matches("GAGATCCTA"))
    
test()
print()
test2()
