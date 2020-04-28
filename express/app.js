const express=require('express');
const bodyParser=require('body-parser'); 
const cors=require('cors');
var spawn = require('child_process').spawn;
var cont=require('./controller')
var app=express();
app.use(cors({origin:"*"}));
app.use(bodyParser.json());
app.listen(3000,()=> console.log("Server start")); 
app.use('/nlp',cont); 

