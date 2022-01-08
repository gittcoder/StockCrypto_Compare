(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
var connection = new WebSocket('ws://localhost:5557');
connection.onopen = function () 
{
  connection.send("abcd");
  console.log("Message Sent!!!")
  document.querySelector("#get_stock").addEventListener("click", () => 
  {
    console.log("Function CALLED!!!");
    stock=document.querySelector('input').value;
    cry=document.querySelector("#sel_crypto").value;
    timeline=document.querySelector("#sel_date").value;
    console.log("stock");
    console.log(stock);
    console.log("stock");
    console.log(cry);
    console.log("stock");
    console.log(timeline);
    message="stock "+stock + " " +timeline;
    if(stock!="" && cry=="Select Crypto")
    {
        if(timeline!="Select Timeline")
        {
            message="stock "+stock+ " " +timeline;
            connection.send(message);
            console.log("Stock Message Sent!!!");
            window.open("loading.html");
        }
        else
        {
          connection.send("abcd");
          alert("Please Select Valid Timeline!!!");
        }
    }
    else if(stock=="" && cry!="Select Crypto")
    {
        if(timeline!="Select Timeline")
        {
            message="crypto "+cry+ " " +timeline;
            connection.send(message);
            console.log("Crypto Message Sent!!!");
            window.open("loading.html");
        }
        else
        {
            connection.send("abcd");
            alert("Please Select Valid Timeline!!!");
        }
    }
    else if(stock=="" && cry=="Select Crypto")
    {
      connection.send("abcd");
      alert("Required Fields are Not filled (Either Stock OR Crypto )!!!");
    }
    else
    {
        connection.send("abcd");
        alert("You are only allowed to enter Either Crypto Or Stock , NOT BOTH !!!");
    }

  });
};





},{}]},{},[1]);
