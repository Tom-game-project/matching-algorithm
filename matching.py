# matching algorithm
# マッチングアルゴリズム
# 頂点を共有しない辺の集合をマッチングという
# マッチングは頂点同士をペアにすることを意味している
# max_matching関数はマッチングが最大になるようにしている

from typing import Generator
import copy #再帰に処理時の配列保存よう

import os
import json
from pprint import pprint

import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        """
        対岸のノード
        """
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
        self.matching_set=[]
        for i in self.anodes:
            for j in self.get_other_side(i.id,belonging=0):
                if all(map(lambda a:a[1]!=j ,self.matching_set )):
                    self.matching_set.append((i.id,j))
                    break

    def find_unmatching_node(self, matching: list[tuple[int, int]], belonging=0) -> list[int]:
        """
        引数`matching`はマッチしたnodeのペアのリスト
        マッチしていないノードをiterで返却する
        """
        matching_list = [i[belonging] for i in matching]
        target_nodes = self.anodes if belonging == 0 else self.bnodes
        return [
            i.id
            for i in target_nodes
            if i.id not in matching_list
        ]

    def find_matching_node(self, matching: list[(int, int)], belonging=0) -> int:
        """
        引数`matching`はマッチしたnodeのペアのリスト
        マッチしているノードをiterで返却する
        """
        matching_list = [i[belonging] for i in matching]
        target_nodes = self.anodes if belonging == 0 else self.bnodes
        return (
            i.id
            for i in target_nodes
                if i.id in matching_list
        )

    def get_incr_roads(self,start_node_id:int)->list[list[int]]:
        """
        左側にある、まだマッチしていないnodeのidを引数にとります
        増加道かまたは変更可能なノード先を返却します

        """
        # 変数の初期化
        self.incr_roads: list[list[int]] = []
        self.incr_road: list[int] = []

        self.marked_anode: list[int] = []  # 左側の頂点集合で使用されたもの
        self.marked_bnode: list[int] = []  # 右側の頂点集合で使用されたもの
        logging.debug("スタートノード")
        logging.debug(start_node_id)
        self.marked_anode.append(start_node_id)# node_id と合わせる
        self.__get_incr_roads__process(start_node_id,belonging=0,flag=True)

        return self.incr_roads

    def get_incr_roads2(self,start_node_id:int)->list[list[int]]:
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
        self.__get_incr_roads__process(start_node_id,belonging=0,flag=False) # flag false

        return self.incr_roads


    def __get_incr_roads__process(self,node_id: int, belonging=0,flag=False):
        """
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        """
        road:list[int] = copy.deepcopy(self.incr_road)
        
        marked_a_local = copy.deepcopy(self.marked_anode)
        marked_b_local = copy.deepcopy(self.marked_bnode)

        next_id=node_id
        logging.debug("id")
        logging.debug(next_id)
        if belonging %2 == 0:    #左側にいるとき
            opposite=self.get_other_side(next_id, belonging=0)  # 進む先のノードの候補
            opposite = list(opposite)
            opposite=filter(
                lambda i: i not in road[0::2],
                opposite
            )# すでに通った左側ノードを除く
            opposite = filter(
                lambda j: (next_id, j) not in self.matching_set,
                opposite
            )
            opposite = [k
                for k in opposite 
                if k not in self.marked_bnode
            ]
            opposite = [k for k in opposite]
            logging.debug("左側から見た右ノード")
            logging.debug(opposite)
            
            if opposite:# 進める道がある場合
                for i in opposite:
                    self.marked_bnode = self.marked_bnode+opposite
                    self.incr_road.append(i)
                    self.__get_incr_roads__process(i,belonging=1,flag=True) # 再帰部分
                    
                    self.incr_road = copy.deepcopy(road) # ここのdeepcopy必要かどうか怪しい
                    self.marked_anode = copy.deepcopy(marked_a_local) # ここのdeepcopy必要かどうか怪しい
            elif flag:
                self.incr_roads.append(self.incr_road)
            else:
                logging.debug(
                    self.incr_road
                )
        else:                   #右側にいるとき
            opposite=self.get_other_side(
                            next_id, belonging=1)  # 進む先のノードの候補 
            opposite=filter(
                        lambda i: i not in road[1::2],  # すでに通った右側ノードを除く
                    opposite)
            opposite= filter(
                    lambda j: (j, next_id) in self.matching_set,
                opposite)
            opposite = [k
                for k in opposite
                if k not in self.marked_anode
                ] # マッチングに含まれて**いる**もの
            opposite = [k for k in opposite]
            logging.debug("右から見た左ノード")
            logging.debug(opposite)
            
            if opposite:# 進める道がある場合
                for i in opposite:
                    self.marked_anode = self.marked_anode+opposite
                    self.incr_road.append(i)
                    self.__get_incr_roads__process(i,belonging=0,flag=True) # 再帰部分
                    
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
    
    def new_matching_set_creator(
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
    
    def max_matching(self)->list[tuple[int,int]]:
        """
        任意の最大マッチングリストを返却する
        同じ条件に対して出力は常に同じになるが最大マッチングが一つになるとは限らない
        """
        self.init_matching() # マッチングを初期化する
        while True: # 終了の保証が出来ない
            unmatching_list = self.find_unmatching_node(self.matching_set,belonging=0) # 左側ノードの全てのアンマッチノードを返却する
            if len(unmatching_list)==0:
                return self.matching_set
            
            increment = [i 
                    for i in self.get_incr_roads(unmatching_list[0])
                        if len(i) > 2
                ] # 増加道のみを受け入れる
            
            print("incr",increment)
            if len(increment)==0:
                return self.matching_set
            else:
                incr_rord=self.incr_sides_iter(unmatching_list[0],increment[0])
                remove_matching_set=incr_rord[1::2]
                add_matching_set=incr_rord[0::2]
                self.matching_set = self.new_matching_set_creator(
                    self.matching_set,
                    remove_matching_set,
                    add_matching_set
                )

    def max_matching2(self):
        """
        第二案
        最大かどうかに関わらずとりあえず全てのマッチングに関して増加道が無くなるまで計算する
        """

        self.init_matching()
        unmatching_list = self.find_unmatching_node(self.matching_set,belonging=0)
        for i in unmatching_list:
            logging.debug("アンマッチ",i)
            increment = [
                j for j in self.get_incr_roads(i)
                if len(j)>1
            ]
            logging.debug(f"増加道 {increment}")
            for inc in increment:
                incr_road = self.incr_sides_iter(i,inc)
                remove_matching_set = incr_road[1::2]
                add_matching_set = incr_road[0::2]
                changedmatching = self.new_matching_set_creator(
                    self.matching_set,
                    remove_matching_set,
                    add_matching_set
                )
                yield changedmatching


    def find_all_max_matching(self):# 工事中工事中工事中工事中工事中工事中工事中工事中工事中工事中工事中工事中
        """
        全ての最大マッチングを返却する
        同じ条件に対して出力の順番は常に同じである
        """
        # 考慮すべき事項
        # 増加道を見つけたからと言って最大マッチングを見つけたとは限らない
        # 最大マッチングを見つけるまで増加道を見つけなければならない
        # あるアンマッチノードをすべて探しても最大マッチングに到達しないのであれば
        # そのノードを含んだ増加道を見つけることはできないので終了

        maxmatchlen = len(self.max_matching())# 最大マッチングのリストの長さ

        self.init_matching() # マッチングを初期化する
        while True: # 終了の保証が出来ない
            unmatching_list = self.find_unmatching_node(self.matching_set,belonging=0) # 左側ノードの全てのアンマッチノードを返却する
            if len(unmatching_list)==0:
                return self.matching_set
            else:
                incriment = [i 
                    for i in self.get_incr_roads(unmatching_list[0])
                        if len(i) > 2
                ] # 増加道のみを受け入れる
            
            if len(incriment)==0:
                return self.matching_set
            else:
                incr_rord=self.incr_sides_iter(unmatching_list[0],incriment[0])
                remove_matching_set=incr_rord[1::2]
                add_matching_set=incr_rord[0::2]
                self.matching_set = self.new_matching_set_creator(
                    self.matching_set,
                    remove_matching_set,
                    add_matching_set
                )


    def test_max_matching(self):
        """
        最大マッチングを見つける関数作成のためのテスト
        """

        # ここでself.matching_setが初期化される
        self.init_matching()

        # 左側ノードの全てのアンマッチノードを探す
        unmatch_list=self.find_unmatching_node(self.matching_set,belonging=0)
        print("左側でマッチしていないノード",unmatch_list)
        
        # 増加道を探す
        matching = self.matching_set
        print("増加道を探す",matching)

        incriment = [i 
            for i in self.get_incr_roads(2)
                if len(i) > 2
        ] # 増加道のみを受け入れる
        print("見つかった増加道",incriment)

        print("Base Matching".center(30,"="))
        for i in self.matching_set:
            print(i)

        print("Incr Road".center(30,"="))
        for i in unmatch_list:
            # 以下実験ではnodeid 4をスタートにして実験
            incriment = [j
                for j in self.get_incr_roads(i)
                    if len(j) > 2
            ] # 増加道のみを受け入れる
            for j in incriment:
                # iは増加道
                incr_rord=self.incr_sides_iter(i,j)
                
                print("rm")
                print(
                    "-",
                    remove_matching_set:=incr_rord[1::2]
                )
                print("add")
                print(
                    "+",
                    add_matching_set:=incr_rord[0::2]
                )

                print("New Matching")
                print(
                    "->",
                    self.new_matching_set_creator(
                        self.matching_set,
                        remove_matching_set,
                        add_matching_set
                    ), "\n"
                )


def __test0_function():
    """
    test0 function 
    テスト用関数
    """
    mgraph.matching_set = [(0, 1), (1, 4), (3,3)]
    
    print("Base Matching".center(30,"="))
    for i in mgraph.matching_set:
        print(i)
    print("incr road".center(30,"="))
    # 以下実験ではnodeid 4をスタートにして実験
    for i in mgraph.get_incr_roads(4):
        # iは増加道
        incr_rord=mgraph.incr_sides_iter(4,i)
        
        print("rm")
        print(
            "-",
            remove_matching_set:=incr_rord[1::2]
        )
        print("add")
        print(
            "+",
            add_matching_set:=incr_rord[0::2]
        )

        print("New Matching")
        print(
            "->",
            mgraph.new_matching_set_creator(
                mgraph.matching_set,
                remove_matching_set,
                add_matching_set
            ), "\n"
        )



backnum="0"
# テスト用データ
with open(os.path.join("data",f"works{backnum}.json"),encoding="utf-8")as f:
    works = json.load(f)
    #pprint(works)
with open(os.path.join("data",f"staff{backnum}.json"),encoding="utf-8")as f:
    staff_ability = json.load(f)
    #pprint(staff_ability)

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
    
    logging.debug(mgraph.sides)
    logging.debug("最大マッチング")
    logging.debug(
        mgraph.max_matching()
    )
    
    #for i in mgraph.max_matching2():print("マッチング",i)
    
    
    # print(
    #     mgraph.find_all_max_matching()
    # )

    end = time.perf_counter()

    print("パフォーマンス",(end-start)*1000,"ms")