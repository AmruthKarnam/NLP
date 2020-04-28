const express =require('express');
var router= express.Router();
var spawn = require('child_process').spawn;
router.post('/getsarcasm',(req,res) => {
    input_tweet = req.body.tweet;
    
    console.log("here");
    //res.send(['hi']);
    var process = spawn('python3',['./get_sarcasm.py',input_tweet]);
    console.log(input_tweet);
    process.stdout.on('data',function(class_predicted){
        res.send(class_predicted);
        console.log("there");
    });
    
});

router.post('/getsentiment',(req,res) => {
    input_comment = req.body.tweet;
    console.log("Inside Get Sentiment");
    var num=0;
    var process = spawn('python3',['senti.py',input_comment]);
    process.stdout.on('data',function(sentiment_predicted){
        console.log(sentiment_predicted.toString());
        
        res.send([sentiment_predicted.toString()]);
    });
});
module.exports=router;