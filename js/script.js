/** 
 * @fileOverview マッチングアルゴリズムを実装したファイルです
 * 
 * @author Tom0427
 * @version 1.0.0
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
        this.sides = []; // 辺

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
        this.sides.push([anode,bnode])
    }

    /**
     * ## getOtherSide
     * ### 相手となりうるnodeのarrayを返却します
     * @param {Number} nodeId 
     * @param {Number} belonging 
     * @returns {Array<Number>}
     */
    getOtherSide(nodeId,belonging=0){
        return this.sides
            .filter(a=>a[belonging]==nodeId)
            .map(a=>a[belonging^1])
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
     * @param {NUmber} belonging 
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
     * @param {NUmber} belonging 
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
        this.getIncrRoadsProcess(start_node_id,belonging);

        return this.incr_roads;
    }

    /**
        node引数はマッチしていないものでanodesに属するものを選ぶ必要がある
        返り値は増加道を表現したリスト
        
        再帰的に処理を行う部分

     * @param {Number} nodeId 
     * @param {Number} belonging 
     */
    getIncrRoadsProcess(nodeId,belonging=0){
        //structureCloneはdeepClone
        road = structuredClone(this.incr_road);

        marked_a_local = structuredClone(this.marked_anode);
        marked_b_local = structuredClone(this.marked_bnode);

        nextId = structuredClone(nodeId)

        if (belonging%2==0){
            //内側から
            let opposite = this.getOtherSide(nextId,1)
            .filter(
                i=>{
                    //今までに通ったことのあるノードを除く
                    !([...Array(road.length)]
                    .map((i,j)=>j)
                    .filter(i=>i%2==0)//偶数番のみ
                    .map(i=>road[i]).includes(i));
                }
            ).filter(
                //
                i=>{
                    //マッチングしているノードは除く
                    !this.matching_set.includes((nextId,i))
                }
            ).filter(
                i=>{
                    //this.marked_bnodeに含まれているnodeは除く
                    !this.marked_bnode.includes(i)
                }
            )
            if (opposite){
                //まだ進める場合
                for (const i of opposite){
                    this.marked_bnode = this.marked_bnode.concat(opposite);
                    this.incr_road(i);
                    this.getIncrRoadsProcess(i,1);

                    this.incr_road = structuredClone(road);
                    this.marked_anode = structuredClone(marked_a_local);
                }
            }else{
                //もし進める道がない場合
            }
        }else{
            //ここに挿入
            let opposite = this.getOtherSide(nextId,1)
            .filter(
                i=>{
                    //今までに通ったことのあるノードを除く
                    !([...Array(road.length)]
                    .map((i,j)=>j)
                    .filter(i=>i%2==1)//奇数番のみ
                    .map(i=>road[i]).includes(i));
                }
            ).filter(
                //
                i=>{
                    //マッチングしているノードは除く
                    !this.matching_set.includes((i,nextId))
                }
            ).filter(
                i=>{
                    //this.marked_bnodeに含まれているnodeは除く
                    !this.marked_anode.includes(i)
                }
            )
            if (opposite){
                //まだ進める場合
                for (const i of opposite){
                    this.marked_bnode = this.marked_bnode.concat(opposite);
                    this.incr_road(i);
                    this.getIncrRoadsProcess(i,1);

                    this.incr_road = structuredClone(road);
                    this.marked_anode = structuredClone(marked_a_local);
                }
            }else{
                //もし進める道がない場合
            }
        }
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

    ////


}main()