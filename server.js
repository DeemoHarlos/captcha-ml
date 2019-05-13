const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser')
var app = express()
var port = 8787
var test = true
var text = []

var index = 0

function getText() {
	var input = fs.readFileSync('label.csv').toString()
	var items = input.split('\n')
	text = items.map(x=>x.split(' ')[1])
}

getText()


if (test) {
  app.use((req,res,next)=>{
    res.header("Access-Control-Allow-Origin", "*")
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next()
  })
}
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())
app.enable('trust proxy')

app.post('/:id',(req,res)=>{
	res.status(200)
	res.end()
	console.log('POST')
	var index = Number(req.params.id)
	text[index] = req.body.text
	var outputBuffer = new Buffer(text.map((x,i)=>i+' '+x).join('\n'))
	fs.writeFileSync('label.csv', outputBuffer)
})

app.get('/',(req,res,err)=>{
	getText()
	console.log(text[2])
	console.log('GET')
	var i = 0
	while(text[index]!=''&&index<2068) {
		i++
		index ++
		if (i>2068) break
	}
	res.status(200).send(index+'')
	index ++
	index %= 2068
})

app.listen(port,()=>{
	console.log('listening...')
})