/** 
 * 同じリポジトリ内にあるpythonと同じ実装をしたjavascriptバージョン
 * @fileOverview マッチングアルゴリズムを実装したjsファイルです
 * 
 * @author Tom0427
 * @version 1.0.0
 */



/**
 * 頂点ノードオブジェクト
 */
class node{
    /**
     * # 頂点(ノード)
     * 
     * @param {Number} id 
     * @param {Object} data 
     */
    constructor(id,data){
        this.id = id;
        this.data = data;
    }
}


class matchingGraph{
    /**
     * anodes 頂点集合左
     * bnodes 頂点集合右
     * @param {Array<node>} anodes 
     * @param {Array<node>} bnodes 
     */
    constractor(anodes,bnodes){
        /**
         * @type {Array<node>}
         */
        this.anodes = anodes; // 頂点集合左
        /**
         * @type {Array<node>}
         */
        this.bnodes = bnodes; // 頂点集合右

        /**
         * @type {Array<Array<Number>>}
         */
        this.sides = Array(); // 辺

        /**
         * @type {Array<Array<Number>>}
         */
        this.matching_set = []; // マッチング集合

        //以下は増加道を発見する際に使います
        /**
         * @typedef {Array<Number>} incrRoads
         * @type {Array<incrRoads>}
         */
        this.incr_roads = [];
        /**
         * @type {incrRoads}
         */
        this.incr_road = [];

        /**
         * @type {Array<Number>}
         */
        this.marked_anode = [];
        /**
         * @type {Array<Number>}
         */
        this.marked_bnode = [];
    }

    /**
     * ## addSide
     * ### 辺を追加する
     * @param {Number} anode 
     * @param {Number} bnode 
     */
    addSide(anode,bnode){
        if (this.sides===undefined){
            //this.sidesを安全に呼び出す
            this.sides=[];
        }

        this.sides.push([anode,bnode]);
    }

    /**
     * ## getOtherSide
     * ### 相手となりうるnodeのarrayを返却します
     * @param {Number} nodeId 
     * @param {Number} belonging 
     * @returns {Array<Number>}
     */
    getOtherSide(nodeId,belonging){
        return this.sides.filter(a=>a[belonging]==nodeId).map(a=>a[(belonging==1?0:1)])
    }

    /**
     * ## initMatching
     * ### 一連のnodeと辺の設定が終わったら
     * ### マッチング(集合)を初期状態にする
     */
    initMatching(){
        for (const i of this.anodes){
            for (const j of this.getOtherSide(i.id,belonging=0)){
                if (this.matching_set.map(a => a[1] !== j).every()){
                    this.matching_set.push([i.id,j]);
                    break;
                }
            }
        }
    }

    /**
     * ## findUnMatchingNode
     * ### 引数`matching`はマッチしたnodeのペアのリスト
     * ### マッチしていないノードをリストで返却する
     * 
     * @param {Array<Array<Number>>} matching 
     * @param {Number} belonging 
     * @returns {Array<Number>}
     */
    findUnMatchingNode(matching,belonging=0){
        matching_list = matching.map(i => i[belonging]);
        target_node = belonging == 0 ? this.anodes : this.bnodes;

        return target_node
            .filter(i => !matching_list.includes(i.id))
            .map(i => i.id);
    }

    /**
     * ## findMatchingNode
     * ### 引数`matching`はマッチしたnodeのペアのリスト
     * ### マッチしているノードをリストで返却する
     * 
     * @param {Array<Array<Number>>} matching 
     * @param {Number} belonging 
     * @returns {Array<Number>}
     */
    findMatchingNode(matching, belonging = 0) {
        matching_list = matching.map(i => i[belonging]);
        target_node = belonging == 0 ? this.anodes : this.bnodes;

        return target_node
            .filter(i => matching_list.includes(i.id))
            .map(i => i.id);
    }

    /**
     * ## getIncrRoads
     * ### 左側にある、まだマッチしていないnodeのidを引数にとります
     * ### 増加道かまたは変更可能なノード先を返却します
     * @param {Number} start_node_id
     * @returns {Array<Array<Number>>} 
     */
    getIncrRoads(start_node_id){
        this.incr_roads=[];
        this.incr_road=[];
        
        this.marked_anode=[];
        this.marked_bnode=[];

        this.marked_anode.push(start_node_id);
        this.getIncrRoadsProcess(start_node_id,0);

        return this.incr_roads
    }

    /**
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        
        再帰的に処理を行う部分

     * @param {Number} nodeId 
     * @param {Number} belonging 
     */
    getIncrRoadsProcess(nodeId,belonging){
        //structureCloneはdeepClone
        let road = structuredClone(this.incr_road);

        let marked_a_local = structuredClone(this.marked_anode);
        let marked_b_local = structuredClone(this.marked_bnode);

        let nextId = structuredClone(nodeId);

        if (belonging%2==0){     //左側にいるとき
            //内側から
            let opposite = this.getOtherSide(nextId,0);
            
            // 今までに通ったことのあるノードを除く
            opposite=opposite.filter(
                i=>
                    ![...Array(road.length)]
                    .map((j,k)=>k)
                    .filter(k=>k%2==0)
                    .map(k=>road[k]).includes(i)
            )
            //マッチングしているノードは除く
            opposite=opposite.filter(i=>
                    !this.matching_set.some(j=>j[0]==nodeId&&j[1]==i)//includes [...]の変わり
            )
            opposite=opposite.filter(i=>!this.marked_bnode.includes(i))
            
            if (opposite.length!==0){
                //まだ進める場合
                for (const i of opposite){
                    this.marked_bnode = this.marked_bnode.concat(opposite);
                    this.incr_road.push(i);
                    this.getIncrRoadsProcess(i,1);  //再帰部分

                    this.incr_road = structuredClone(road);
                    this.marked_anode = structuredClone(marked_a_local);
                }
            }else{
                //もし進める道がない場合
            }
        }else{                 //右側にいるとき
            //ここに挿入
            let opposite = this.getOtherSide(nextId,1)
            opposite = opposite.filter(
                i=>
                    //今までに通ったことのあるノードを除く
                    !([...Array(road.length)]
                    .map((j,k)=>k)
                    .filter(k=>k%2==1)//奇数番のみ
                    .map(k=>road[k]).includes(i))
            )
            opposite=opposite.filter(
                //
                i=>
                    //マッチングしているノード
                    this.matching_set.some(j=>j[0]==i&&j[1]==nextId)
            )
            opposite=opposite.filter(
                i=>!this.marked_anode.includes(i)
            )
            if (opposite.length!==0){
                //まだ進める場合
                for (const i of opposite){
                    this.marked_anode = this.marked_anode.concat(opposite);
                    this.incr_road.push(i);
                    this.getIncrRoadsProcess(i,0);    //再帰部分

                    this.incr_road = structuredClone(road);
                    this.marked_bnode = structuredClone(marked_b_local);
                }
            }else{
                //もし進める道がない場合
                this.incr_roads.push(this.incr_road);
            }
        }
    }

    /**
     * ## incrSidesIter 
     * 引数には増加道のみを含むリスト
     * 戻り値は
     * (左ノード,右ノード)
     * のデータ形式を含んだリスト
     * 
     * @param {Number} start_node_id 
     * @param {Array<Number>} incr_list 
     * @returns {Array<Array<Nuber>>}
     */
    incrSidesIter(start_node_id,incr_list){
        let incr_road_map = [start_node_id].concat(incr_list); 
        return [...Array(incr_road_map.length-1)].map((i,j) => j%2===0?[incr_road_map[j],incr_road_map[j+1]]:[incr_road_map[j+1],incr_road_map[j]])
    }

    /**
     * 古いマッチングから新しいマッチングに更新します
     * 
     * @param {Array} matching 
     * @param {Array} remove_matching_set 
     * @param {Array} add_matching_set
     * 
     * @returns {Array<Array<Number>>} 
     */
    newMatchingSetCreator(matching,remove_matching_set,add_matching_set){
        return matching
        .filter(
            i=>!remove_matching_set
                .some(j=>j[0]===i[0]&&j[1]===i[1])
            )
        .concat(add_matching_set)
    }

    maxMatching(){
        this.initMatching();

        let unmatch_list = this.findMatchingNode(this.matching_set,0);

        let matching = this.matching_set;
        incriment = this.getIncrRoads().filter(i=>i.length>2);//増加道のみを受け入れる
        //todo!
    }
}


/**
 * # main function
 * 
 * 実験用
 */
function main(){

    ////サンプルデータの用意
    const works = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F"
    ]
    const staff_ability = [
        {
            name: "1",
            capable: ["B", "D"]
        },
        {
            name: "2",
            capable: ["A", "C", "E"]
        },
        {
            name: "3",
            capable: ["B"]
        },
        {
            name: "4",
            capable: ["D", "E", "F"]
        },
        {
            name: "5",
            capable: ["B", "D"]
        },
    ]

    ////nodeの設定
    const staff_nodes = [...Array(staff_ability.length)].map((i,j)=>new node(j,staff_ability[j]));
    const works_nodes = [...Array(works.length)].map((i,j)=>new node(j,works[j]));

    let mgraph = new matchingGraph(
        staff_nodes,
        works_nodes
    );//インスタンス化

    //辺の追加

    for (const i of staff_nodes){
        for (const j of i.data.capable){
            // jは役職の名前　例:A,B (..etc)
            mgraph.addSide(
                i.id,
                works.indexOf(j)
            );
        }
    }

    mgraph.matching_set = [
        [0, 1],
        [1, 4],
        [3, 3],
    ]

    console.log("------------include------------");
    for (const i of mgraph.matching_set){
        console.log(i);
    }

    console.log("------------incrroads------------")
    for (const i of mgraph.getIncrRoads(4)){
        let incr_road = mgraph.incrSidesIter(4,i);

        //宣言だけ先にしておく

        
        let remove_matching_set = [...Array(incr_road.length)]
        .map((j,k)=>k)
        .filter(k=>k%2===1)
        .map(k=>incr_road[k]);
        
        let add_matching_set    = [...Array(incr_road.length)]
        .map((j,k)=>k)
        .filter(k=>k%2===0)
        .map(k=>incr_road[k]);

        console.log("rm");

        console.log(
            "-",
            remove_matching_set
        );
            
        console.log(
            "+",
            add_matching_set
        );

        console.log("New Matching");
        console.log(
            "->",
            mgraph.newMatchingSetCreator(
                mgraph.matching_set,
                remove_matching_set,
                add_matching_set
            )
        )

    }
}main()