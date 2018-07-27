var host='http://127.0.0.1:5000/';
var moverUrl = host + 'top_movers';
// console.log(moverUrl);

$.getJSON(
     moverUrl,
    //host +'data',
    function(json){
        data = json;
        // console.log(data);
        var priceUrl = host +'stock_info/'+ data[0];
        document.getElementById("stockSymbol").innerHTML = data[0];

        $.getJSON(
                priceUrl,
                function(res){
                    
                    chartBars = res.ChartBars;
                    document.getElementById("transactinCount").innerHTML = chartBars[0].Volume;
                    document.getElementById("stockPrice").innerHTML = chartBars[0].VWAP;


                    var x = [];
                    var close = [];
                    var high = [];
                    var low = [];
                    var open = [];

                    chartBars.forEach(function(fragment){
                        // console.log(fragment);
                        x.push(fragment.StartTime);
                        close.push(fragment.Close);
                        high.push(fragment.High);
                        low.push(fragment.Low);
                        open.push(fragment.Open);
                    });
                    
                    var trace1 = {
  
                        x: x, 
                        
                        close: close, 
                        
                        decreasing: {line: {color: '#7F7F7F'}}, 
                        
                        high: high, 
                        
                        increasing: {line: {color: '#17BECF'}}, 
                        
                        line: {color: 'rgba(31,119,180,1)'}, 
                        
                        low: low, 
                        
                        open: open, 
                        
                        type: 'candlestick', 
                        xaxis: 'x', 
                        yaxis: 'y'
                      };
                      
                      var data = [trace1];
                      
                      var layout = {
                        dragmode: 'zoom', 
                        margin: {
                          r: 10, 
                          t: 25, 
                          b: 40, 
                          l: 60
                        }, 
                        showlegend: false, 
                        xaxis: {
                          autorange: true, 
                          domain: [0, 1], 
                        //   range: ['2017-01-03 12:00', '2017-02-15 12:00'], 
                        //   rangeslider: {range: ['2017-01-03 12:00', '2017-02-15 12:00']}, 
                          title: 'Date', 
                        //   type: 'date'
                        }, 
                        yaxis: {
                          autorange: true, 
                          domain: [0, 1], 
                        //   range: [114.609999778, 137.410004222], 
                          type: 'linear'
                        }
                      };
                      Plotly.plot('priceChart', data, layout);



                }

            );


        for (i=0; i < 10; i++) {
            var reqUrl = host +'data/'+ data[i];
            // console.log(reqUrl);
            //var priceUrl = reqUrl;
            
            var tweetUrl = reqUrl;
            var tbody = document.getElementById("moverBody");

            // create Table
            $.getJSON (
                reqUrl,
                function (res) {
                    
                    res = res;
                    console.log(res);

                    // var table = document.getElementById("moverTable");
                    var tr = document.createElement("tr");
                    var tdCode = document.createElement("td");
                    var tdName = document.createElement("td");
                    var tdPrice = document.createElement("td");
                    var tdBadge = document.createElement("td");

                    var name = document.createTextNode(res[0].stock);
                    var price = document.createTextNode(res[0].price);
                    var growth = (res[0].price - res[0].price_15min)/res[0].price_15min;
                    growth = Math.floor(growth * 100 * Math.pow(10,2))/Math.pow(10,2);
                    var badge;

                    if (growth > 1) {
                        badge = '<span class="label label-success">+' + growth + '%</span>';
                    } else if (growth > - 1) {
                        badge = '<span class="label label-warning">+' + growth + '%</span>';
                    } else {
                        badge = '<span class="label label-danger">+' + growth + '%</span>';
                    }
                    
                    tdCode.innerHTML = res[0].stock;
                    tdName.appendChild(name);
                    tdPrice.appendChild(price);
                    tdBadge.innerHTML = badge;
                    
                    tr.appendChild(document.createElement("td"));
                    tr.appendChild(tdCode);
                    tr.appendChild(tdName);
                    tr.appendChild(tdPrice);
                    tr.appendChild(tdBadge);
                    tbody.appendChild(tr);

                }
            );
            
        }


    }
);
