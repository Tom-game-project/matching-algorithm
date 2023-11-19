import { matchingGraph } from "./script";


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
}
main()