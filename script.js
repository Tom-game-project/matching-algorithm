
import {node,matchingGraph} from "./js/matching.js";//マッチングライブラリ

//人間関係グラフ
// create an array with nodes
import staff from "./data/staff.json" assert { type: "json" };
import works from "./data/works.json" assert {type:"json"};

const staff_nodes = [...Array(staff.length)].map((i,j)=>new node(j,staff[j]));
const works_nodes = [...Array(works.length)].map((i,j)=>new node(j,works[j]));

let mgraph = new matchingGraph(staff_nodes,works_nodes);//インスタンス化

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

let max_match = mgraph.maxMatching();
console.log(
    "マックスマッチング",
    max_match
);

let all_match = [];
for (const i of mgraph.maxMatching2()){
    console.log("マッチング",i);
    all_match.push(i);
}

//頂点の設定
let nodeList = [...Array(staff.length).keys()]
    .map(function (i){
        return {
            id : i,
            label : staff[i].name,
            x : 100,
            y : i*120,
            shape: "box",
            color: "#f9a8ff"
        }
    }).concat([...Array(works.length).keys()]
        .map(function(i){
        return {
            id : i+staff.length,
            label : works[i],
            x : 1000,
            y : i*120
        }
    })
    );

//辺の設定
let edgeList = [];
for (let i=0; i< staff.length;i++){
    for (const j of staff[i].capable){
        let edge={
            from:i,
            to:staff.length+works.indexOf(j)
        };
        if (max_match.some(k=>k[0]==i&&k[1]==works.indexOf(j))){//最大マッチングのリストに含まれているかどうか
            edge["color"]={ color: "#ff0000"} ;
        }else{
            edge["color"]={ color: "#0000ff"} ;
        }
        edgeList.push(edge);
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
let network = new vis.Network(container, data, options);
