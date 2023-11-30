import init,{MatchingGraph} from "./matching/pkg/matching.js";

//人間関係グラフ
// create an array with nodes
//test data
import staff00 from "./data/00/staff.json" assert { type: "json" };
import works00 from "./data/00/works.json" assert {type:"json"};
import staff01 from "./data/01/staff.json" assert { type: "json" };
import works01 from "./data/01/works.json" assert {type:"json"};
import staff02 from "./data/02/staff.json" assert { type: "json" };
import works02 from "./data/02/works.json" assert {type:"json"};
import staff03 from "./data/03/staff.json" assert { type: "json" };
import works03 from "./data/03/works.json" assert {type:"json"};

/**
 * # createTable
 * 表作成
 */
function createTable(matchingList){
    let table = document.getElementById("shiftTable");
    let thead = document.createElement("thead");
    let thead_tr = document.createElement("tr");
    for (const thead_tr_th_text of ["tasks","staff"]){
        let thead_tr_th = document.createElement("th");
        thead_tr_th.textContent=thead_tr_th_text;
        thead_tr.appendChild(thead_tr_th);
    }
    thead.appendChild(thead_tr);
    let tbody = document.createElement("tbody");
    for (const matching of matchingList){
        let tbody_tr = document.createElement("tr");
        let task = document.createElement("th")
        let member = document.createElement("td");
        task.textContent = matching[0];
        member.textContent = matching[1];
        tbody_tr.appendChild(task);
        tbody_tr.appendChild(member);
        tbody.appendChild(tbody_tr);
    }
    table.appendChild(thead);
    table.appendChild(tbody);
}

/**
 * # matching2List
 * 
 * createTableに
 * @param {Array<Array<Number>>} max_matching 
 * @param {Object} staff 
 * @param {Object} works 
 * @returns {Array<Array<Number>>}
 */
function matching2List(max_matching,staff,works){
    let rlist = [];
    for (const matching of max_matching){
        rlist.push(
            [works[matching[1]],staff[matching[0]].name]
        );
    }
    return rlist;
}

init().then(
    ()=>{
        /**
         * # initGraph
         * グラフを初期化
         * @param {Object} staff 
         * @param {Object} works 
         * @returns {MatchingGraph}
         */
        function initGraph(staff,works){
            const staff_nodes = [...Array(staff.length).keys()].map((i)=>i);
            const works_nodes = [...Array(works.length).keys()].map((i)=>i);
            let mgraph = new MatchingGraph(staff_nodes,works_nodes);//インスタンス化
            //辺の追加
            
            let index = 0;
            for (const i of staff){
                for (const j of i.capable){
                    // jは役職の名前　例:A,B (..etc)
                    mgraph.addSide(
                        index,
                        works.indexOf(j)
                    );
                }
                index++;
            }
            return mgraph;
        }
        
        /**
         * # initNetwork
         * @param {*} staff 
         * @param {*} works 
         * @returns {Array}
         */
        function initNetwork(staff,works){
            //二部グラフを可視化する
            let max_match = JSON.parse(mgraph.maxMatching());
            console.log(max_match);
            let max_length = max_match.length;
            
            //頂点の設定
            let nodeList = [...Array(staff.length).keys()]
                .map(function (i){
                    return {
                        id : i,
                        label : staff[i].name,
                        x : 100,
                        y : i*240,
                        shape: "box",
                        color: "#f9a8ff"
                    }
                }).concat([...Array(works.length).keys()]
                    .map(function(i){
                    return {
                        id : i+staff.length,
                        label : works[i],
                        x : 500,
                        y : i*240
                    }
                })
                );
            
            //辺の設定
            let k = 0;
            let edgeList = [];
            for (let i=0; i< staff.length;i++){
                for (const j of staff[i].capable){
                    let edge={
                        id:k,
                        from:i,
                        to:staff.length+works.indexOf(j)
                    };
                    edgeList.push(edge);
                    k+=1;
                }
            }
            
            let nodes = new vis.DataSet(nodeList);
            
            // create an array with edges
            let edges = new vis.DataSet(edgeList);
            
            // create a network
            let container = document.getElementById("mynetwork");
            let data = {
            nodes: nodes,
            edges: edges,
            };
            let options = {
                physics: {
                    enabled: false,
                },
            };
            
            return [edges,nodes,new vis.Network(container, data, options)];
        }
        
        /**
         * #  changeEdgesColor
         * @param {Array<Array<Number>>} matching 
         */
        function changeEdgesColor(staff,works,matching){
            let k=0;
            for (let i=0; i< staff.length;i++){
                for (const j of staff[i].capable){
                    let edge={
                        id:k,
                        from:i,
                        to:staff.length+works.indexOf(j)
                    };
                    if (matching.some(k=>k[0]==i&&k[1]==works.indexOf(j))){//最大マッチングのリストに含まれているかどうか
                        //マッチングに含まれている
                        edge["color"]={ color: "#ff0000"} ;
                        edge["width"]="20";
                    }else{
                        //マッチングに含まれていない
                        edge["color"]={ color: "#c2c2c2"} ;
                        edge["width"]="3";
                    }
                    edges.update(edge)
                    k+=1;
                }
            }
        }
        
        let mgraph;
        let edges,nodes,network;
        
        //--------00
        mgraph = initGraph(
            staff02,
            works02
        );
        [edges,nodes,network] = initNetwork(
            staff02,
            works02
        );

        let max_matching = JSON.parse(mgraph.maxMatching())
        changeEdgesColor(
            staff02,
            works02,
            max_matching
        )
        
        
        let nextBtn = document.getElementById("nextbtn");
        let backBtn = document.getElementById("backbtn");
        
        
        nextBtn.addEventListener("click",()=>{onClickNextBtn(1)});
        backBtn.addEventListener("click",()=>{onClickNextBtn(-1)});
        
        function mod(n,m){
            //剰余の出し方をpythonと同じにする
            return  ((n % m) + m) % m;
        }
        
        //--------------event--------------
        let counter = 0
        let ctrElem = document.getElementById("ctr");
        ctrElem.textContent = counter;
        function onClickNextBtn(head){
            counter++;
        }


        let a = matching2List(
            max_matching,
            staff02,
            works02
        );
        createTable(a);
    }
)