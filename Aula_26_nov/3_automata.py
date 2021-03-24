
class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1                                      # Q - number of states
        print('self.numstates = ', self.numstates)
        self.alphabet = alphabet                                               # Alphabet     
        self.transitionTable = {}                                              # Transition table
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                prefixo = pattern[:q]+a                                        
                self.transitionTable[(q,a)] = overlap(prefixo,pattern)         
                
       
    def printAutomata(self):
        print ("States: " , self.numstates)
        print ("Alphabet: " , self.alphabet)
        print ("Transition table:")
        for k in self.transitionTable.keys():
            print (k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable.get((current,symbol))
        #return self.transitionTable[(current,symbol)]
        
    def applySeq(self, seq):
        ''' 
        Parameters
        ----------
        seq : str
            
        Returns
        -------
        res : list
            List that contains the 'next states' after cheking the current state and symbol in the transition table. 
        '''
        q = 0                                                                  # the 1st state is 0
        res = [q] 
        for s in range(len(seq)):                                              # for each symbol in the sequence
            q = self.nextState(q, seq[s])                                      # the next state will be the corresponding value 
            res.append(q) 
        return res
        
    def occurencesPattern(self, text):
        ''' 
        Parameters
        ----------
        text : str
            
        Returns
        -------
        res : list
            List that contains the occurrences of the pattern found within the text. 
        '''
        q = 0 
        res = []
        states = self.applySeq(text)
        c = 0                                                                  # counts the occurence of a pattern found
        for i in states:
            if i == (self.numstates-1):                                        # if the last state was achieved...
                c += 1
                res.append(c)                                                  #...the index of its occurence is a result
            elif i != (self.numstates-1) and (c!=0):
                c+=1
        return res

def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov,0,-1):
        if s1[-i:] == s2[:i]: return i                                         # returns the index where the overlap occurs
    return 0

               
def test():
    auto = Automata("AC", "ACA")
    auto.printAutomata()
    print (auto.applySeq("CACAACAA"))
    print (auto.occurencesPattern("CACAACAA"))

test()

#States:  4
#Alphabet:  AC
#Transition table:
#0 , A  ->  1
#0 , C  ->  0
#1 , A  ->  1
#1 , C  ->  2
#2 , A  ->  3
#2 , C  ->  0
#3 , A  ->  1
#3 , C  ->  2
#[0, 0, 1, 2, 3, 1, 2, 3, 1]
#[1, 4]


