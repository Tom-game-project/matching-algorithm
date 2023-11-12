


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
        this.anodes = anodes; // 頂点集合左
        this.bnodes = bnodes; // 頂点集合右

        this.sides = []; // 辺

        this.matching_set = []; // マッチング集合

        //以下は増加道を発見する際に使います
        this.incr_roads = [];
        this.incr_road = [];

        this.marked_anode = [];
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

    findUnMatchingNode(){
        
    }
}