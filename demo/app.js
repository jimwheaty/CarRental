var express = require('express');
// var path = require('path');
// var favicon = require('static-favicon');
// var logger = require('morgan');
// var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
const cors = require('cors');

const PORT = 3000;

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
        x:"23.818984", y:"38.050653", name:"Takissssss", info:"Spitarona"
     },
     {
        x:'24', y:'38', name:"Pnigikaaa", info:"mallon skafos"
     }
     ]);
    // res.status(200).send({"message":"geiaaa"})
    //res.send({x:38.050855, y:23.819017/*, name: "Takis", value: "42"*/ })
    // res.send('hel42lo world');

});
app.post('/observatory/api/upload', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    console.log("token=",req.header("x-observatory-auth"))
    res.status(200).send({"message": "Data recieved"})
});
app.post('/observatory/api/login', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.status(200).send([{
        "success":"true",
        "message":"Authentication successful!",   "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTM0OTMzNTY2LCJleHAiOjE1MzUwMTk5NjZ9.3xOdoxpK8hb42ykjMIl6rwLafB63Y-EQNOO9fFamp68"
     }])
});
app.get('/observatory/api/logout', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    res.status(200).send([{
        "message":"logout successful"
    }])
    console.log("logout token=",req.header("x-observatory-auth"))
});
app.post('/observatory/api/signup', function(req, res){
    res.header("Access-Control-Allow-Origin", "*");
    console.log(req.body);
    res.status(200).send([{
        "success":"true",
        "message":"Authentication successful!",   "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTM0OTMzNTY2LCJleHAiOjE1MzUwMTk5NjZ9.3xOdoxpK8hb42ykjMIl6rwLafB63Y-EQNOO9fFamp68"
     }])
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
