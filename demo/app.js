var express = require('express');
// var path = require('path');
// var favicon = require('static-favicon');
// var logger = require('morgan');
// var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
const cors = require('cors');

const PORT = 8765;

// var routes = require('./routes/index');
// var users = require('./routes/users');

var app = express();

// view engine setup
// app.set('views', path.join(__dirname, 'views'));
// app.set('view engine', 'jade');

// app.use(favicon());
// app.use(logger('dev'));
app.use(bodyParser.json());
// app.use(bodyParser.urlencoded());
// app.use(cookieParser());
app.use(cors());
// app.use(express.static(path.join(__dirname, 'public')));

//app.use('/', routes);
app.get('/observatory/api/', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    //res.json({"x":"38.050855", "y":"23.819017"})
    console.log("4242");
    res.json([{
        x:"23.818984", y:"38.050653", name:"TheCarsShop", info:"TooHigh"
     },
     {
        x:'24', y:'38', name:"BestCars", info:"SuperSports"
     }
     ]);
    // res.status(200).send({"message":"geiaaa"})
    //res.send({x:38.050855, y:23.819017/*, name: "Takis", value: "42"*/ })
    // res.send('hel42lo world');

});
app.get('/observatory/api/prices', function(req, res){
    console.log("parameters:",req.query)
    res.send({start:0, count:3, total:3, prices:[
        {price:42,date:"1973-10-10", productName:"Ford Focus",productId:42,
          productTags:["Zoula","Zoula"],shopId:"9834",shopName:"Kitsos",
          shopTags:["HighService","EasyService"],shopAddress:"Papaswthriou"},
        {price:43,date:"2016-04-01", productName:"Opel Astra",productId:43,
          productTags:["tag1","tag2"],shopId:"0",shopName:"FastCars",
          shopTags:["HighService","EasyService"],shopAddress:"Kekropos"},
        {price:44,date:"2017-01-02",productName:"Citroen C1", productId:44,
          productTags:["tag2","tag5"],shopId:"2",shopName:"CarRental",
          shopTags:["EasyService"],shopAdress:"Kolokotroni 65"}
    ]})
})
app.post('/observatory/api/prices', function(req, res){
    // console.log("parameters:",req.query)
    res.send({message:"ok!"})
})
app.get('/observatory/api/shops/shop3',function(req, res){
    console.log("edw einai o shop3")
    res.send(
        {
            id:"324",name:"GoodCars",address:"Melissiwn",lng:23.818984,
            lat:38.050653,tags:[],withdrawn:1
        }
    )
})
app.get('/observatory/api/shops/9834',function(req, res){
    console.log("Edw einai to shop1")
    res.send(
        {
            id:"9834",name:"Ford Focus",address:"Moyrganas",lng:24,
            lat:38,tags:[],withdrawn:1
        }
    )
})
app.get('/observatory/api/shops/2',function(req, res){
    console.log("Edw einai to shop2")
    res.send(
        {
            id:"2",name:"IounioRental",address:"Miranas",lng:23,
            lat:36.9,tags:[],withdrawn:1
        }
    )
})
app.get('/observatory/api/shops/0',function(req, res){
    console.log("Edw einai to shop2")
    res.send(
        {
            id:"0",name:"Opel Astra",address:"Kalograizas",lng:23.435,
            lat:37.3254,tags:["Air condition"],withdrawn:1
        }
    )
})
app.post('/observatory/api/upload', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    console.log("token=",req.header("x-observatory-auth"))
    res.status(200).send({"message": "Data recieved"})
});
app.post('/observatory/api/login', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.status(200).send({
        "success":"true",
        "message":"Authentication successful!",   "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTM0OTMzNTY2LCJleHAiOjE1MzUwMTk5NjZ9.3xOdoxpK8hb42ykjMIl6rwLafB63Y-EQNOO9fFamp68"
     })
});
app.post('/observatory/api/logout', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    res.status(200).send({
        "message":"OK"
    })
    console.log("logout token=",req.header("x-observatory-auth"))
});
app.post('/observatory/api/signup', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.send({
        "X-OBSERVATORY-AUTH":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTM0OTMzNTY2LCJleHAiOjE1MzUwMTk5NjZ9.3xOdoxpK8hb42ykjMIl6rwLafB63Y-EQNOO9fFamp68"
     })
});
let uploadProductResultId=42;
let uploadShopResultId=42;

app.get('/observatory/api/products',function(req, res){
    console.log("edw einai to product1")
    res.send(
        {start:0,count:1,total:1,products:[
            {id:"42",name:"e",description:"string",
            category:"string",tags:[],withdrawn:1}]
        }
    )
})
app.get('/observatory/api/products/42',function(req, res){
    console.log("edw einai to product1")
    res.send(
        {
            id:"42",name:"Toyata",description:"string",
            category:"string",tags:[],withdrawn:1
        }
    )
})
app.get('/observatory/api/products/43',function(req, res){
    console.log("edw einai to product1")
    res.send(
        {
            id:"42",name:"Cintroen",description:"string",
            category:"string",tags:[],withdrawn:1
        }
    )
})
app.get('/observatory/api/shops',function(req, res){
    console.log("edw einai o shop1")
    res.send(
        {start:0,count:1,total:1,shops:[
            {id:"42",name:"pnigika home",address:"string",lng:24,
            lat:38,tags:[],withdrawn:1}]
        }
    )
})
app.post('/observatory/api/products', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.send({message:"successful!"})
});
app.post('/observatory/api/shops', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.send({message:"successful!"})
});
app.listen(PORT, function(){
    console.log("Server running on localhost:" + PORT);
});



// app.use('/users', users);

// /// catch 404 and forwarding to error handler
// app.use(function(req, res, next) {
//     var err = new Error('Not Found');
//     err.status = 404;
//     next(err);
// });

// /// error handlers

// // development error handler
// // will print stacktrace
// if (app.get('env') === 'development') {
//     app.use(function(err, req, res, next) {
//         res.status(err.status || 500);
//         res.render('error', {
//             message: err.message,
//             error: err
//         });
//     });
// }

// // production error handler
// // no stacktraces leaked to user
// app.use(function(err, req, res, next) {
//     res.status(err.status || 500);
//     res.render('error', {
//         message: err.message,
//         error: {}
//     });
// });
// console.log("42-2");
  

// module.exports = app;
