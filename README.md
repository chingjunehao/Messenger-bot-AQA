# Messenger-bot-AQA
![demo](/assets/application_demo.png)
Messenger bot that returns you the aesthetic score of your image when you send it an image.
```
├── Messenger-bot-AQA
│   ├── assets
│   ├── Flask-serve-model
│   └── NodeJS-FB-webhook
```

## Flask-serve-model
Directory that stores the trained model and Flask API that serve the model on heroku. Models are from this [repository](https://github.com/chingjunehao/SSL-Inpainting-AQA).

## NodeJS-FB-webhook
Directory that stores the heroku hosted NodeJS that serve the webhook to communicate with Facebook and Flask API.

## TODO
1) Steps to create the same project.