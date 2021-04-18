const LOCATION = "Political Science";
document.getElementById('building').innerHTML = LOCATION;
const column1 = document.getElementById('column1');
const column2 = document.getElementById('column2');
const column3 = document.getElementById('column3');
const column4 = document.getElementById('column4');
const column5 = document.getElementById('column5');
const column6 = document.getElementById('column6');


const getSpaces = async () => {
    const response = await fetch('http://somchai09.trueddns.com:43322/getavailableparkingspace');
    const data = await response.json(); 
    console.log(data);

    //filter only data in location
    var filtered_data = [];
    for(i = 0; i< data.length;i++){
        if(data[i]['building']==LOCATION){
            filtered_data.push(data[i]);
        }
    }
    console.log(filtered_data);

    //add div for each floor
    const container = document.getElementById('container');
    for(i = 0; i < filtered_data.length;i++){
        //create new div
        var div = document.createElement("div");
        div.setAttribute("id","data");
        var div2 = document.createElement("div");
        div2.setAttribute("id","data");
        //middle div to align floor text
        var middle = document.createElement("div");
        middle.setAttribute("id","middle");
        //floor text container
        var div_floor = document.createElement("div");
        div_floor.setAttribute("id","floorContainer");
        //floor text
        var p = document.createElement('p');
        p.setAttribute("id","floor");
        div.appendChild(middle);
        middle.appendChild(div_floor)
        div_floor.appendChild(p);

        var div_space = document.createElement("div");
        div_space.setAttribute("id","spaceContainer");
        var p2 = document.createElement('p');
        p2.setAttribute("id","spaces");
        div2.appendChild(div_space);
        div_space.appendChild(p2);
        //set text
        p.innerHTML = filtered_data[i]['floor'];
        p2.innerHTML = filtered_data[i]['available_space'];
        //add to html
        if(i<6){
            column1.appendChild(div);
            column2.appendChild(div2);
            continue;
        }
        if(i<12){
            column3.appendChild(div);
            column4.appendChild(div2);
            continue;
        }
        if(i<18){
            column5.appendChild(div);
            column6.appendChild(div2);
            continue;
        }
       
        
    }

    
    

    
}
getSpaces();