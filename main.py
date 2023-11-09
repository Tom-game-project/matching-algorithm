# matching algorithm
# マッチングアルゴリズム
# 頂点を共有しない辺の集合をマッチングという
# マッチングは頂点同士をペアにすることを意味している
# max_matching関数はマッチングが最大になるようにしている

class node:
    def __init__(self,id_:int,data):
        self.id = id_
        self.data=data

class matchingGraph:
    def __init__(self,anodes:list[node],bnodes:list[node]):
        self.anodes = anodes
        self.bnodes = bnodes
        self.sides = []
    def add_side(self,anode:int,bnode:int):
        self.sides.append((anode,bnode))

    
    def get_all_side(self)->list[tuple[int,int]]:
        """
        全ての辺を取得し、そのリストを返却します
        """
        return self.sides

def max_matching():
    # 
    pass

def incr_road():
    pass

works = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
]

staff_ability = {
    "1": {
        "capable": ["B", "D"]
    },
    "2": {
        "capable": ["A", "C", "E"]
    },
    "3": {
        "capable": ["B"]
    },
    "4": {
        "capable": ["D", "E", "F"]
    },
    "5": {
        "capable": ["B", "D"]
    },
}

if __name__=="__main__":
    pass