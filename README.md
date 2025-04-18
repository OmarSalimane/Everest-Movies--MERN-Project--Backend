# Movie Recommendation Chatbot Backend

This repository contains a Flask backend for an OpenAI-powered movie recommendation chatbot.

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```
   pip install flask flask-cors openai python-dotenv pymongo
   ```
3. Create a `.env` file with your keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URI=your_mongodb_uri
   ```

## Dataset

Download the Movies Dataset from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) and place the CSV files in a `data` folder.

## Running the App

```
flask run
```

The chatbot API will be available at: http://127.0.0.1:5000/api/chatbot
