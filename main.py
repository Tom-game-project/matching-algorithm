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
        self.anodes:list[node] = anodes #0
        self.bnodes:list[node] = bnodes #1
        self.sides:list[tuple[int,int]] = []
        self.matching_set:list[tuple[int,int]]=[]#

        self.incr_roads:list[list[int]]=[]
        self.incr_road:list[int]=[]

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

    def get_incr_roads(self,node_id: int, belonging=0):
        """
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        """
        road:list[int] = copy.deepcopy(self.incr_road)
        step=0
        next_id=node_id
        
        if belonging%2==0:
            a = self.get_other_side(next_id,belonging=0)
            a = [i 
                for i in a 
                    if i not in road[0::2]
                    # まだ通っていない道かどうか
                ]
            a = [i 
                for i in a 
                    if (next_id,i) not in self.matching_set
                    # マッチングに含まれて**いない**もの
                ]
            
            if a:# 進める道がある場合
                for i in a:
                    self.incr_road.append(i)
                    self.get_incr_roads(i,belonging=1)
                    self.incr_road=road
            else:  # もし進める道がない
                pass
        else:
            b = self.get_other_side(next_id,belonging=1)
            b = [i
                for i in b
                    if i not in road[1::2]
            ]
            b = [i
                for i in b
                    if (i,next_id) in self.matching_set
                    # マッチングに含まれて**いる**もの
            ]

            if b:# 進める道がある場合
                for i in b:
                    self.incr_road.append(i)
                    self.get_incr_roads(i,belonging=0)
                    self.incr_road=road
            else:  # 進める道がない場合
                self.incr_roads.append(self.incr_road)
        step+=1


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
    mgraph.get_incr_roads(4, belonging=0)
    pprint(
        mgraph.incr_roads
    )