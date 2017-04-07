import Kmeans_rgb_modified

class Graph:
    def __init__(self,m,n,la,lb):
        self.size = m * n
        self.width = n
        self.length = m
        self.edg = {0:{}}
        self.adj = {0:[]}
        for i in range(self.size):
            # source to every node
            self.edg[0].setdefault(i+1, la[i])
            # source's adjcent node
            self.adj[0].append(i+1)
            
        for i in range(self.size):
            xc = i // self.width
            yc = (i + 1) % self.width
            self.edg.setdefault(i + 1,{})
            # set penalty
            penalty = 0.2
            # current node to sink
            self.edg[i + 1].setdefault(-1,lb[i])
            self.adj.setdefault(i + 1,[])
            self.adj[i + 1].append(-1)
            # current node to adjcent node
            if xc != 0:
                if yc == 0:
                    yct = self.width
                else:
                    yct = yc
                top = (xc - 1) * self.width + yct
                self.edg[i + 1].setdefault(top, penalty)
                self.adj[i + 1].append(top)
            if yc != 1:
                if yc == 0:
                    yct = self.width
                else:
                    yct = yc
                left = xc * self.width + yct - 1
                self.edg[i + 1].setdefault(left, penalty)
                self.adj[i + 1].append(left)
            if yc != 0:
                right = xc * self.width + yc + 1
                self.edg[i + 1].setdefault(right, penalty)
                self.adj[i + 1].append(right)
            if xc != self.length - 1:
                if yc == 0:
                    xct = xc + 1
                else:
                	xct = xc
                bot = (xct + 1) * self.width + yc
                self.edg[i + 1].setdefault(bot, penalty)
                self.adj[i + 1].append(bot)

    def find_adjcent(self,x):
        return self.adj[x]

    def update(self,path,min):
        




if __name__=='__main__':
    m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()
    g=Graph(m, n, likelihood_a, likelihood_b)
    print(g.find_adjcent(5))

 