import javax.swing
import com
from java.awt import Component,GridLayout
from javax.swing import JFrame

class dockexample1(com.hp.hpl.guess.ui.DockableAdapter):
	
	searchtext = JTextField("Enter your search term",20)
        depthtext =JTextField("Enter the node to be searched",20)
        leveltext = JTextField("Enter the level",20)
        node1text =JTextField("Enter the first node:",20)
        node2text =JTextField("Enter the second node:",20)
        betcluster=JButton("Connect")
        searchbutton =JButton("search")
        clustrbutton =JButton("Full Cluster")
        depthbutton =JButton("Level Search")
        minclustr =JButton("Individual Cluster")    
	
	textarea= JTextArea()
        textarea.size=(300,1)


	
	'''btn1 =JButton("Button1")
	btn2 =JButton("Button2")
	btn3 =JButton("Button3")
	btn4 =JButton("Button4")
	btn5 =JButton("Button5")'''

	def __init__(self):	

		# every time the button is pressed, center the display
          	#listener = addEventListener(searchbutton, ActionListener, 'actionPerformed', searchaction)
           	self.searchbutton.actionPerformed = self.searchaction
            	self.clustrbutton.actionPerformed= self.cluaction                   
            	self.depthbutton.actionPerformed= self.depthaction                          
            	self.betcluster.actionPerformed=self.connectaction  
            	self.minclustr.actionPerformed=self.mincluaction


	
		self.frame =JFrame('Welcome to Tree Search!', defaultCloseOperation=JFrame.EXIT_ON_CLOSE, size=(300, 300), locationRelativeTo=None)
            	 	
		
		self.mainPanel =JPanel(GridLayout(7,1))
		self.mainPanel.add(self.searchtext)
		self.frame.add(self.mainPanel)
				
		self.prow =JPanel(GridLayout(1,3))
		
		self.prow.add(self.searchbutton)
		self.prow.add(self.minclustr)
		self.prow.add(self.clustrbutton)
			
		self.frame.add(self.prow)
		self.mainPanel.add(self.prow)		
		self.prow =JPanel(GridLayout(1,2))
		self.prow.add(self.depthtext)
		self.prow.add(self.leveltext)
		self.frame.add(self.prow)
		self.mainPanel.add(self.prow)
		self.mainPanel.add(self.depthbutton)
		self.frame.add(self.mainPanel)

		self.prow=JPanel(GridLayout(1,2))
		self.prow.add(self.node1text)
		self.prow.add(self.node2text)
		self.frame.add(self.prow)
		self.mainPanel.add(self.prow)
		self.mainPanel.add(self.betcluster)
		self.frame.add(self.mainPanel)
		
		self.mainPanel.add(self.textarea)
		self.frame.add(self.mainPanel)
		
		self.frame.visible=true
		
		#add toolbar to the main window
            
            	ui.dock(self)




	          
      #INDIVIDUAL CLUSTERING
        def mincluaction(self,event):
		g.edges.color=blue
		g.nodes.color=cadetblue
		val = self.searchtext.getText()
        	txt=""
		
		       #self.labl.setText(st)
		for n in g.nodes:
			if n.label==val:
				nod=n.name
				n.color=red
				n1=n
				f=1
				while(f):
					for e in g.edges:
						if e.node1==n1 or e.node2==n1:
							if e.node1==n1:
								if e.node2.betweenness>n1.betweenness:
									n1=e.node2
									e.color=yellow
									if n1.totaldegree>3:
										f=0
										break
									else:
										break
							elif e.node2==n1:
								if e.node1.betweenness>n1.betweenness:
									n1=e.node1
									e.color=yellow
									if n1.totaldegree>3:
										f=0
										break
									else:
										break
								
	
				for e1 in g.edges:
					if e1.node1==n1 or e1.node2==n1:
						if e1.node1==n1:
							if e1.node2.betweenness<n1.betweenness:
								e1.color=yellow	
						else:
							if e1.node1.betweenness<n1.betweenness:
								e1.color=yellow
	
      #SEARCHING

        def searchaction(self,event):
            g.edges.color=blue
            g.nodes.color=cadetblue
            val = self.searchtext.getText()
            txt=""
            #self.labl.setText(st)
            for n in g.nodes:
                if n.label==val:
                        nod=n.name
                        n.color=red
                        for e in g.edges:
                                if e.node1.label==val or e.node2.label==val:
                                        e.color=red
                                        if e.node1.label==val:
                                                txt=txt+e.node2.label+"\n"
                                        else:
                                                txt=txt+e.node1.label+"\n"
            self.textarea.setText("You may also like:\n"+txt)                          
#level clustering
        def depthaction(self,event):
		lis=[]
      		g.edges.color=blue
		g.nodes.color=cadetblue
		dep=self.depthtext.getText()
		c=int(self.leveltext.getText())
		cot=0
		lev=0
		for n in g.nodes:
			if n.label==dep:
				
				n.color=red
				for e in g.edges:
					if e.node1==n or e.node2==n:
                                                e.color=red						
						if(e.node1==n and e.node2.betweenness<n.betweenness):
							lis.append(e.node2)
							cot=cot+1
						elif(e.node2==n and e.node1.betweenness<n.betweenness):
							lis.append(e.node1)	
							cot=cot+1
				break
							
					
		cot1=0	
		i=0
		print c
		while(lev <c):
				
		
			
			while(i<len(lis)):	
				for e in g.edges:
					if e.node1==lis[i] or e.node2==lis[i]:
                	                        						
						if((e.node1==lis[i]) and (e.node2.betweenness<e.node1.betweenness)):
							lis.append(e.node2)
							if(lev%3==0):							
								e.color=green
							elif lev%3==1:
								e.color=yellow
							elif lev%3==2:
								e.color=red
							cot1=cot1+1
		
						elif ((e.node2==lis[i]) and (e.node1.betweenness<e.node2.betweenness)):
							lis.append(e.node1)
							if(lev%3==0):							
								e.color=green
							elif lev%3==1:
								e.color=yellow
							elif lev%3==2:
								e.color=red
							cot1=cot1+1
					
				i=i+1
				cot=cot-1
				if cot<=0:
					lev=lev+1
					cot=cot1
					cot1=0
					break


 #TOTALCLUSTER
        def cluaction(self,event):
	    g.edges.color=blue
	    g.nodes.color=cadetblue
	    for e in g.edges:
		if e.node1.betweenness>0.2*(max(g.nodes.betweenness)) and e.node2.betweenness>0.2*(max(g.nodes.betweenness)):
			if e.node2.totaldegree>0.25*(max(g.nodes.totaldegree)) or e.node1.totaldegree>0.25*(max(g.nodes.totaldegree)):
				e.visible=false

      #CONNECTION BETWEEN TWO CLUSTERS
        def connectaction(self,event):
		txt=""
                g.edges.color=blue
                g.nodes.color=cadetblue                                 
                n1=self.node1text.getText()
                n2=self.node2text.getText()
                for n in g.nodes:
                        if n.label==n1:
                                n.color=red
                                nod1=n
                for n in g.nodes:
                        if n.label==n2:
                                n.color=red
                                nod2=n
                f=1
                while(f):
                        for e in g.edges:
                                if nod1.betweenness<=nod2.betweenness:
                                        if e.node1==nod1 or e.node2==nod1:
                                                if e.node1==nod1 and e.node2.betweenness>e.node1.betweenness:
                                                        e.color=red
                                                        nod1=e.node2
                                                        if nod1==nod2:
                                                                f=0
								txt=txt+"\n"+e.node2.label
                                                        break
                                                elif e.node2==nod1 and e.node1.betweenness>e.node2.betweenness:
                                                        e.color=red
                                                        nod1=e.node1
                                                        if nod1==nod2:
                                                                f=0
								txt=txt+"\n"+e.node1.label
                                                        break
                                elif nod1.betweenness>nod2.betweenness:         
                                        if e.node1==nod2 or e.node2==nod2:
                                                if e.node1==nod2 and e.node2.betweenness>e.node1.betweenness:
                                                        e.color=red
                                                        nod2=e.node2
                                                        if nod1==nod2:
                                                                f=0
								txt=txt+"\n"+e.node2.label
                                                        break
                                                elif e.node2==nod2 and e.node1.betweenness>e.node2.betweenness:
                                                        e.color=red
                                                        nod2=e.node1
                                                        if nod1==nod2:
                                                                f=0
								txt=txt+"\n"+e.node1.label
                                                        break
                                
		self.textarea.setText("You may also like:\n"+txt)  

	def getTitle(self):
            # define the title in the window
            return("dockexample1")      
