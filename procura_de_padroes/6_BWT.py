############################################
#        Burrows-Wheeler Transform
#
###########################################

class BWT:
    
    def __init__(self, seq = "",buildsufarray = False):
        self.bwt = self.build_bwt(seq, buildsufarray) 
    
    def set_bwt(self, bw):
        self.bwt = bw


    def build_bwt(self, text, buildsufarray = False):
        ls = []
        # generates ciclic rotations
        ls = [ ]
        for i in range(len(text)):
            ls.append(text[i:]+text[:i])
        ls.sort()                                                           # lexicographic order
        res = " "
        for i in range(len(text)): 
            res += ls[i][len(text)-1]                                       # recover the last column
        return res                                                          # the result is a string

        if buildsufarray:
            self.sa = []
            for i in range(len(ls)):
                stpos = ls[i].index("$")
                self.sa.append(len(text)-stpos-1)
        return res    
    
    def inverse_bwt(self):
        firstcol = self.get_first_col()
        res = ""                                                             # final result
        c = "$"                                                              # last character in the sequence
        occ = 1                                                              # first character occurrence
        for i in range(len(self.bwt)):
            pos = find_ith_occ(self.bwt,c,occ)                               # retrieve element from first column in that position
            c = firstcol[pos]                                                # update c
            occ = 1                                                          # update occurrence
            k = pos-1                                                        # or pos -=1                        
            while firstcol[k] == c and k >=0:
                occ += 1
                k -= 1                                                       # decrease in index number
            res += c
        return res        
 
    def get_first_col (self):
        '''Recovers the first column by transformim bwt (str) into a sorted list'''
        firstcol = []
        for c in self.bwt:
            firstcol.append(c)                                                # convert bwt into a list
        firstcol.sort()                                                       # sort the list 
        return firstcol
        
    def last_to_first(self):
      '''Creates a table to convert the position of the same symbol from the last to the first column'''
        res = []
        firstcol = self.get_first_col()                                       # get the first column
        for i in range(len(firstcol)):                                        # check occurrences
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c)+1
            res.append(find_ith_occ(firstcol, c, ocs))
        return res

    def bw_matching(self, patt):
        lf = self.last_to_first()
        res = []                                                              # list of the positions where pattern occurrs in the 1st column
        top = 0                                                               # first position
        bottom = len(self.bwt)-1                                              # last position
        flag = True
        while flag and top <= bottom:
            if patt != "":                                                    # if pattern is not empty continue, else stop
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom+1)]                              
                if symbol in lmat:                                            # if the symbol exists between top and bottom
                    topIndex = lmat.index(symbol) + top                       # first occurrence of the symbol
                    bottomIndex = bottom - lmat[::-1].index(symbol)           # last occurence of the symbol
                    top = lf[topIndex]                                        # recalculate top
                    bottom = lf[bottomIndex]                                  # recalculate bottom
                else: flag = False                                            
            else: 
                for i in range(top, bottom+1): res.append(i)                  # append elements between top and bottom to the res list
                flag = False            
        return res        
 
    def bw_matching_pos(self, patt):
        res = []
        matches = self.bw_matching(patt)
        for m in matches:
            res.append(self.sa[m])
        res.sort()
        return res
 

def find_ith_occ(l, elem, index):
    j, k = 0, 0
    while k < index and j < len(l):
        if l[j] == elem:
            k += 1
            if k == index: return j
        j+=1
    return -1 

      
def test():
    seq = "TAGACAGAGA$"
    bw = BWT(seq)
    print (bw.bwt)
    print (bw.last_to_first())
    print (bw.bw_matching("AGA"))


def test2():
    bw = BWT("")
    bw.set_bwt("ACG$GTAAAAC")
    print (bw.inverse_bwt())

def test3():
    seq = "TAGACAGAGA$"
    bw = BWT(seq, True)
    print("Suffix array:", bw.sa)
    #print(bw.bw_matching_pos("AGA"))

test()
#test2()
#test3()

