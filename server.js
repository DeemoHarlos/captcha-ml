const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser')
var app = express()
var port = 8787
var test = true
var text = []

var index = 0

function getText() {
	var input = fs.readFileSync('temp.csv').toString()
	text = input.split('\n')
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
	var id = Number(req.params.id)
	text[id] = req.body.text
	var outputBuffer = Buffer.from(text.join('\n'))
	fs.writeFileSync('temp.csv', outputBuffer)
})

app.get('/',(req,res)=>{
	getText()
	console.log('GET')
	var i = 0
	while(text[index]!=''&&text[index]!='\r') {
		i++
		index ++
		index %= 3000
		if (i>=3000) break
	}
	res.status(200).send(index+'')
	index ++
	index %= 3000
})

app.listen(port,()=>{
	console.log('listening...')
})