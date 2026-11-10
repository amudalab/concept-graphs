class Edge(object):
    """
        A class defined for the edges in the word graph. Here edges include
        edge weight, and the number of times it is updated, from node, tonode and any other information needed. The methods
        facilitate the processing specific to text graph
    """

    def __init__(self):
        self.weight = float('inf')
        self.numupdate = 0
        #self.fromnode = " "
        #self.tonode = " "

    def updatenumber(self):
        self.numupdate += 1

    def updatewt(self,wt):
        curwt = self.weight + wt
        self.weight = curwt
		
    def getwt(self,maxi):
        curwt = ((self.weight)*(maxi-self.numupdate))/((self.numupdate*1.0)*maxi)
        return curwt
        
