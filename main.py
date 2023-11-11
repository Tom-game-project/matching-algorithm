# matching algorithm
# マッチングアルゴリズム
# 頂点を共有しない辺の集合をマッチングという
# マッチングは頂点同士をペアにすることを意味している
# max_matching関数はマッチングが最大になるようにしている

from pprint import pprint
from typing import Generator
import copy

import time

class node:
    """
    頂点(ノード)
    """
    def __init__(self,id_:int,data):
        self.id = id_
        self.data=data


class matchingGraph:

    def __init__(self,anodes:list[node],bnodes:list[node]):
        self.anodes:list[node] = anodes # 0 頂点集合左
        self.bnodes:list[node] = bnodes # 1 頂点集合右

        self.sides:list[tuple[int,int]] = [] # 辺

        self.matching_set:list[tuple[int,int]]=[] # マッチング集合

        # 以下は増加道を発見する際に使います
        self.incr_roads:list[list[int]]=[]
        self.incr_road:list[int]=[]

        self.marked_anode:list[int] = [] # 左側の頂点集合で使用されたもの
        self.marked_bnode:list[int] = [] # 右側の頂点集合で使用されたもの

    def add_side(self,anode:int,bnode:int):
        """
        辺を追加します
        """
        self.sides.append((anode,bnode))

    # 相手となりうるnodeのiterを返却します
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

    def find_unmatching_node(self, matcing: list[tuple[int, int]], belonging=0) -> list[int]:
        """
        引数`matching`はマッチしたnodeのペアのリスト
        マッチしていないノードをiterで返却する
        """
        matching_list = [i[belonging] for i in matcing]
        target_nodes = self.anodes if belonging == 0 else self.bnodes
        return [
            i.id
            for i in target_nodes
            if i.id not in matching_list
        ]

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

    def get_incr_roads(self,start_node_id:int):
        """
        左側にある、まだマッチしていないnodeのidを引数にとります
        増加道かまたは変更可能なノード先を返却します

        """
        # 変数の初期化
        self.incr_roads: list[list[int]] = []
        self.incr_road: list[int] = []

        self.marked_anode: list[int] = []  # 左側の頂点集合で使用されたもの
        self.marked_bnode: list[int] = []  # 右側の頂点集合で使用されたもの

        self.marked_anode.append(start_node_id)# node_id と合わせる
        self.__get_incr_roads__process(start_node_id,belonging=0)

        return self.incr_roads

    def __get_incr_roads__process(self,node_id: int, belonging=0):
        """
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        """
        road:list[int] = copy.deepcopy(self.incr_road)
        
        marked_a_local = copy.deepcopy(self.marked_anode)
        marked_b_local = copy.deepcopy(self.marked_bnode)

        next_id=node_id

        if belonging %2 == 0:
            # 進む先のノードの候補
            opposite = self.get_other_side(next_id, belonging=0)
            opposite = [i 
                for i in opposite 
                    if i not in road[0::2]
                    # まだ通っていない道かどうか
                ]
            opposite = [i 
                for i in opposite 
                    if (next_id,i) not in self.matching_set
                    # マッチングに含まれて**いない**もの
                ]
            opposite = [i
                for i in opposite
                    if i not in self.marked_bnode
            ]
            if opposite:# 進める道がある場合
                for i in opposite:
                    self.marked_bnode = self.marked_bnode+opposite
                    self.incr_road.append(i)
                    self.__get_incr_roads__process(i,belonging=1)
                    
                    self.incr_road = copy.deepcopy(road) # ここのdeepcopy必要かどうか怪しい
                    self.marked_anode = copy.deepcopy(marked_a_local) # ここのdeepcopy必要かどうか怪しい
            else:  # もし進める道がない
                pass
        else:
            # 進む先のノードの候補
            opposite = self.get_other_side(next_id,belonging=1)
            opposite = [i
                for i in opposite
                    if i not in road[1::2]
                    # まだ通っていない道かどうか
            ]
            opposite = [i
                for i in opposite
                    if (i,next_id) in self.matching_set
                    # マッチングに含まれて**いる**もの
            ]
            opposite = [i
                for i in opposite
                    if i not in self.marked_anode
            ]

            if opposite:# 進める道がある場合
                for i in opposite:
                    self.marked_anode = self.marked_anode+opposite
                    self.incr_road.append(i)
                    self.__get_incr_roads__process(i,belonging=0)
                    
                    self.incr_road = copy.deepcopy(road) # ここのdeepcopy必要かどうか怪しい
                    self.marked_bnode = copy.deepcopy(marked_b_local) # ここのdeepcopy必要かどうか怪しい
            else:  # 進める道がない場合
                self.incr_roads.append(self.incr_road)

    def incr_sides_iter(self,start_node_id:int,incr_list:list[int])->list[tuple[int,int]]:
        """
        引数には増加道のみを含むリスト
        戻り値は
        (左ノード,右ノード)
        のデータ形式を含んだリスト
        """
        incr_road_map = [start_node_id]+incr_list
        return [
            (j, incr_road_map[i+1]) 
            if i % 2 == 0 else 
            (incr_road_map[i+1],j) 
            for i, j in enumerate(incr_road_map[:-1])
        ]
    
    def new_matching_set_creater(
            self,
            matching           :list[tuple[int,int]],   # 変更前のマッチング集合
            remove_matching_set:list[tuple[int,int]],   # rm
            add_matching_set   :list[tuple[int,int]]    # add
        )                     ->list[tuple[int,int]]:   # 変更後のマッチング集合
        """
        正しく引数を入力すると
        新しいマッチングを返します
        """
        return [i
            for i in matching
                # 取り除いて
                if i not in remove_matching_set
            ] + add_matching_set # 新しく追加する



    def max_matching(self):
        """
        最大マッチングを探す

        """
        # ここでself.matching_setが初期化される
        self.init_matching()

        # 左側ノードの全てのアンマッチノードを探す
        unmatch_list=self.find_unmatching_node(self.matching_set,belonging=0)

        # 増加道を探す
        matching = self.matching_set
        incriment = [i 
            for i in self.get_incr_roads()
                if len(i) > 2
        ] # 増加道のみを受け入れる
        





# テスト用データ

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

    start=time.perf_counter()
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

    mgraph.matching_set = [(0, 1), (1, 4), (3,3)]
    
    print("マッチング".center(30,"="))
    for i in mgraph.matching_set:
        print(i)
    print("増加道".center(30,"="))
    # 以下実験ではnodeid 4をスタートにして実験
    for i in mgraph.get_incr_roads(4):
        # iは増加道
        incr_rord=mgraph.incr_sides_iter(4,i)
        
        print("削除する古いマッチング")
        print(
            "-",
            remove_matching_set:=incr_rord[1::2]
        )
        print("追加する新しいマッチング")
        print(
            "+",
            add_matching_set:=incr_rord[0::2]
        )

        print("変更後のマッチング")
        print(
            "->",
            mgraph.new_matching_set_creater(
                mgraph.matching_set,
                remove_matching_set,
                add_matching_set
            ), "\n"
        )
    
    end = time.perf_counter()

    print("パフォーマンス",(end-start)*1000,"ms")