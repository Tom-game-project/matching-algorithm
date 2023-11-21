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
let max_length = max_match.length;

let all_match = [];
for (const i of mgraph.maxMatching2()){
    //console.log("マッチング",i);
    if (i.length===max_length){
        all_match.push(i);
    }
}

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
        if (max_match.some(k=>k[0]==i&&k[1]==works.indexOf(j))){//最大マッチングのリストに含まれているかどうか
            edge["color"]={ color: "#ff0000"} ;
            edge["width"]="20";
        }else{
            edge["color"]={ color: "#c2c2c2"} ;
            edge["width"]="3";
        }
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
let network = new vis.Network(container, data, options);

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
    counter+=head;
    
    let matching = all_match[mod(counter,all_match.length)];
    //ひな形

    ctrElem.textContent=mod(counter,all_match.length);
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
