'use strict'

const express = require('express')
const bodyParser = require('body-parser')
const request = require('request')
const app = express()

app.set('port', (process.env.PORT || 5000))

// Process application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({extended: false}))

// Process application/json
app.use(bodyParser.json())

// Index route
app.get('/', function (req, res) {
	res.send('Hello world, I am a chat bot')
})

// for Facebook verification
app.get('/webhook/', function (req, res) {
	if (req.query['hub.verify_token'] === '') {
		res.send(req.query['hub.challenge'])
	}
	res.send('Error, wrong token')
})

const token = ""

function sendTextMessage(sender, text) {
    let messageData = { text:text }
    request({
	    url: 'https://graph.facebook.com/v2.6/me/messages',
	    qs: {access_token:token},
	    method: 'POST',
		json: {
		    recipient: {id:sender},
			message: messageData,
		}
	}, function(error, response, body) {
		if (error) {
		    console.log('Error sending messages: ', error)
		} else if (response.body.error) {
		    console.log('Error: ', response.body.error)
	    }
    })
}

app.post('/webhook/', function (req, res) {
    let messaging_events = req.body.entry[0].messaging
    for (let i = 0; i < messaging_events.length; i++) {
	    let event = req.body.entry[0].messaging[i]
        let sender = event.sender.id
        if (event.message.attachments) {
            let atts = event.message.attachments
            if(atts[0].type === "image"){
             var imageURL = atts[0].payload.url;
             request({
			    url: 'https://immense-beyond-76026.herokuapp.com/prediction',
			    method: 'POST',
			    body: {url: imageURL},
			    headers: {'User-Agent': 'request'},
				json: true 
			}, function(error, response, body) {
			sendTextMessage(sender, response.body)
            })
            
            }
        }
    }
    res.sendStatus(200)
})




// Spin up the server
app.listen(app.get('port'), function() {
	console.log('running on port', app.get('port'))
})