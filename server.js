const fs = require('fs')
const express = require('express')
const bodyParser = require('body-parser')
var app = express()
var port = 8787
var test = true
var csv = []
var num = 20000

var index = 0
var check = 0

function getCsv() {
	var input = fs.readFileSync('temp.csv').toString()
	line = input.split('\n')
	csv = line.map(x=>{
		var arr = x.split(' ')
		return {'text':arr[0],'checked':Number(arr[1])}
	})
}

getCsv()


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

app.get('/',(req,res)=>{
	console.log('GET')
	var i = 0
	while(csv[index].checked>check) {
		i++
		index ++
		index %= num
		if (i>= num) check ++
	}
	res.status(200).send(index+' '+csv[index].text)
	index ++
	index %= num
})

app.post('/:id',(req,res)=>{
	res.status(200)
	res.end()
	console.log('POST')
	var id = Number(req.params.id)
	var newAns = req.body.text
	if (csv[id].text == newAns) csv[id].checked ++
	else csv[id].text = newAns
	var outputBuffer = Buffer.from(csv.map(x=>x.text+' '+x.checked).join('\n'))
	fs.writeFileSync('temp.csv', outputBuffer)
})

app.listen(port,()=>{
	console.log('listening...')
})