console.log(1);
fetch("scripts/json_files/result.json")
    .then(response=>response.json())
    .then(data=>{
        var div = document.getElementById("results");
        var x=div.innerHTML;
        x = x + "<p>Most Expensive : "+ data["most_exp"] +"</p>"+ "<p>Price : "+ data["price"] +" $</p>"+ "<p>Cheapest Investment : "+ data["cheap_invest"] +"</p>"+ "<p>Price : "+ data["cheap_price"] +" $</p>"+ "<p>Suggested : "+ data["suggested"] +"</p>"+ "<p>Price : "+ data["sugg_price"]+" $</p>" ;
        div.innerHTML=x;
    });

fetch("scripts/json_files/result_stock_info.json")
.then(response=>response.json())
.then(data=>{
        console.log(data);
        var div = document.getElementById("stock_info");
        console.log(2);
        var x=div.innerHTML;
        console.log(data.length);
        console.log("entering loop!!");
        var count=0;
        var a=-1;
        x=x+"<table><tr><td>Name</td><td>Price</td><td>Gain</td><td>Time</td></tr>";
        for(let i in data)
        {
            var val="";
            if(count%4==0)
            {
                x=x+"<tr>"
                a++;
                console.log(data["name"+a]);
                val="<th>"+data["name"+a]+"</th>";
            }
            else if(count%4==1)
            {
                console.log(data["price"+a]);
                val="<td>"+data["price"+a]+" $</td>";
            }
            else if(count%4==2)
            {
                console.log(data["gain"+a]);
                val="<td>"+data["gain"+a]+" %</td>";
            }
            else
            {
                console.log(data["time"+a]);
                val="<th>"+data["time"+a]+"</th>";
            }

            x=x+val;
            if(count%4==3)
            {
                x=x+"</tr>";
            }
            //x = x + "<p>Name : "+ data["name0"] +"</p>"+ "<p>Price : "+ data["price0"] +" $</p>"+"<p>Gain : "+ data["gain0"] +" %</p>"+"<p>Time : "+ data["time0"] +"</p>" ;
            //console.log(x);
            count++;
        }
    x=x+"</table>";
    console.log(data["price0"]);
    console.log(3);
    div.innerHTML=x;
    });

