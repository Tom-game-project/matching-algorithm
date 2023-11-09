# matching algorithm
# マッチングアルゴリズム
# 頂点を共有しない辺の集合をマッチングという
# マッチングは頂点同士をペアにすることを意味している
# max_matching関数はマッチングが最大になるようにしている

from pprint import pprint
from typing import Generator
import copy

class node:
    """
    頂点(ノード)
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

        self.incr_road_list=[]

    def add_side(self,anode:int,bnode:int):
        """
        辺を追加します
        """
        self.sides.append((anode,bnode))

    # 相手となりうるnodeのiter
    def get_other_side(self,node_id :int ,belonging=0) -> Generator[int,None,None]:
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

    def find_unmatching_node(self, matcing: list[tuple[int, int]], belonging=0) -> int:
        """
        引数`matching`はマッチしたnodeのペアのリスト
        マッチしていないノードをiterで返却する
        """
        matching_list = [i[belonging] for i in matcing]
        target_nodes = self.anodes if belonging == 0 else self.bnodes
        return (
            i.id
            for i in target_nodes
            if i.id not in matching_list
        )

    def find_matching_node(self, matcing: list[(int, int)], belonging=0) -> int:
        """
        引数`matching`はマッチしたnodeのペアのリスト
        マッチしているノードをiterで返却する
        """
        matching_list = [i[belonging] for i in matcing]
        target_nodes = self.anodes if belonging == 0 else self.bnodes
        return (
            i.id
            for i in target_nodes
                if i.id in matching_list
        )

    def incr_road(self,road:list[int],node_id: int, belonging=0):
        """
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        """
        if belonging%2==0:
            a = self.get_other_side(node_id,belonging=belonging)
            if a:
                for i in a:
                    self.incr_road_list.append(
                        road+self.incr_road(road+[i],i,belonging=1)
                    )
            else:
                return road
        else:
            b = self.get_other_side(node_id,belonging=belonging)
            for i in b:
                pass


    def max_matching():
        # 
        pass


#テスト用データ

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
            mgraph.add_side(i.id, works.index(j))

    # マッチング初期化
    mgraph.init_matching()
    print(
        "マッチング集合",
        matching := mgraph.matching_set
    )

    for i in mgraph.sides:
        print(i[0],"<->" if i in matching else " ->",i[1])

    # マッチングしていないnodeのリスト
    print(
        "マッチングしていないnode",
        list(mgraph.find_unmatching_node(matching, belonging=0))
    )

    mgraph.matching_set = [(0, 1), (1, 4), (3, 3)]
    pprint(
        mgraph.incr_road(4, belonging=0)
    )