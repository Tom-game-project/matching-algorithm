# matching algorithm
# マッチングアルゴリズム
# 頂点を共有しない辺の集合をマッチングという
# マッチングは頂点同士をペアにすることを意味している
# max_matching関数はマッチングが最大になるようにしている

from pprint import pprint

class node:
    """
    頂点
    """
    def __init__(self,id_:int,data):
        self.id = id_
        self.data=data

class matchingGraph:

    def __init__(self,anodes:list[node],bnodes:list[node]):
        self.anodes = anodes #0
        self.bnodes = bnodes #1
        self.sides = []
        self.matching_set=[]

    def add_side(self,anode:int,bnode:int):
        """
        辺を追加します
        """
        self.sides.append((anode,bnode))

    # 相手となりうるnodeのiter
    def get_other_side(self,node_id:int,belonging=0)->iter:
        return map(
            lambda b:b[belonging^1],# <-反転術式
            filter(lambda a:a[belonging]==node_id,self.sides)
        )
    
    
    def init_matching(self):
        """
        初期マッチング

        一連のnodeと辺の設定が終わったら
        マッチング（集合）を初期状態にする
        """
        for i in self.anodes:
            for j in self.get_other_side(i.id,belonging=0):
                
                if all(map(lambda a:a[1]!=j ,self.matching_set )):
                    self.matching_set.append((i.id,j))
                    break




    def incr_road():
        pass


def max_matching():
    # 
    pass

works = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F"
]

staff_ability = [
    {
        "name": "1",
        "capable": ["B", "D"]
    },
    {
        "name":"2",
        "capable": ["A", "C", "E"]
    },
    {
        "name":"3",
        "capable": ["B"]
    },
    {
        "name":"4",
        "capable": ["D", "E", "F"]
    },
    {
        "name":"5",
        "capable": ["B", "D"]
    },
]


if __name__=="__main__":
    # nodeの設定
    staff_nodes = [node(i,j) for i,j in enumerate(staff_ability)]
    works_nodes = [node(i,j) for i,j in enumerate(works)]

    # グラフの初期化
    mgraph = matchingGraph(
        staff_nodes,
        works_nodes
    )

    # 辺の追加
    for i in staff_nodes:
        for j in i.data["capable"]:
            print(i.id, " -> ",works.index(j))
            mgraph.add_side(i.id, works.index(j))
    
    mgraph.init_matching()
    pprint(
        mgraph.matching_set
    )
