import Kmeans_rgb_modified

class Graph:
    def __init__(self,m,n,la,lb):
        self.size = m * n
        self.width = n
        self.length = m
        self.edg = {0:{},-1:{}}
        self.adj = {0:[],-1:[]}
        self.res = {-1:{}}
        for i in range(self.size):
            # source to every node
            self.edg[0].setdefault(i+1, la[i])
            # source's adjcent node
            self.adj[0].append(i+1)
            self.edg[-1].setdefault(i+1, 0)
            
        for i in range(self.size):
            xc = i // self.width
            yc = (i + 1) % self.width
            self.edg.setdefault(i + 1, {})
            # set penalty
            penalty = 0.2
            # current node to sink
            self.edg[i + 1].setdefault(0, 0)
            self.edg[i + 1].setdefault(-1, lb[i])
            self.adj.setdefault(i + 1, [-1])
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
        l=len(path)
        for i in range(l):
            if(i + 1 < l):
                self.edg[path[i]][path[i + 1]] = self.edg[path[i]][path[i + 1]] - min
                self.edg[path[i + 1]][path[i]] = self.edg[path[i + 1]][path[i]] + min
                if self.edg[path[i + 1]][path[i]] > 0 and path[i] not in self.adj[path[i + 1]]:
                    self.adj[path[i + 1]].append(path[i])
                if self.edg[path[i]][path[i + 1]] == 0 and path[i + 1] in self.adj[path[i]]:
                    self.adj[path[i]].remove(path[i + 1])

    def find_edge_value(self,start,end):
        return self.edg[start][end]


if __name__=='__main__':
    m, n, likelihood_a, likelihood_b = Kmeans_rgb_modified.mainfunction()
    g=Graph(m, n, likelihood_a, likelihood_b)
    print(g.find_adjcent(5))
    #print(g.find_edge_value(0,5))
    #print(g.find_edge_value(5,165))
    #print(g.find_edge_value(165,-1))
    g.update([0,5,165,-1],0.2)
    #print(g.find_edge_value(0,5))
    #print(g.find_edge_value(5,165))
    #print(g.find_edge_value(165,-1))
    print(g.find_adjcent(5))


 
