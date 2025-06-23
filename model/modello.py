import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._bestScore = 0
        self._bestPath = []

    def getYears(self):
        return DAO.get_all_years()

    def getShape(self,anno):
        return DAO.get_all_shape(anno)

    def buildGraph(self,anno, forma):
        self._graph.clear()
        nodi = DAO.get_all_nodes(anno,forma)
        for n in nodi:
            self._idMap[n.id] = n

        self._graph.add_nodes_from(nodi)

        archi = DAO.get_all_edges(anno,forma, self._idMap)
        self._graph.add_edges_from(archi)

        connesse = list(nx.weakly_connected_components(self._graph))
        maxCon = max(connesse, key= len)

        return connesse, maxCon

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestpath(self):
        self._bestPath = []
        self._bestScore = 0
        self._occorrenze = dict.fromkeys((1,13),0)

        for n in self._graph.nodes():
            successivi = self.calcolaAmmissibili(n)
            parziale = [n]
            self._occorrenze[n.datetime.month] += 1
            self.ricorsione(parziale,successivi)
            self._occorrenze[n.datetime.month] -= 1
            parziale.pop()

        return self._bestPath,self._bestScore

    def ricorsione(self,parziale,successivi):
        if len(successivi) == 0 and self.getScore(parziale) > self._bestScore:
            self._bestScore = self.getScore(parziale)
            self._bestPath = copy.deepcopy(parziale)

        else:
            for n in successivi:
                parziale.append(n)
                succ = self.calcolaAmmissibili(n)
                self._occorrenze[n.datetime.month] += 1
                self.ricorsione(parziale,succ)
                self._occorrenze[parziale[-1].datetime.month] -= 1
                parziale.pop()


    def calcolaAmmissibili(self, n):
        successivi = self._graph.successors(n)
        ammissibili = []
        for n1 in successivi:
            if n1.duration > n.duration and self._occorrenze[n1.datetime.month] < 3:
                ammissibili.append(n1)
        return ammissibili



    def getScore(self,parziale):
        score = 100*len(parziale)
        for i in range(1,len(parziale)):
            if parziale[i].datetime.month == parziale[i-1].datetime.month:
                score += 200

        return score











