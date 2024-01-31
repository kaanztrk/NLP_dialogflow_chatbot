# NLP Chatbot for Food Ordering

## Overview

This project implements a Natural Language Processing (NLP) chatbot for food ordering, utilizing Google Dialogflow for conversational interactions. The backend is developed using Python and Flask, with MySQL serving as the database for food items, order tracking, and order details.

## Features

- **User Interaction Flow:**
  1. User initiates with greetings, and the chatbot directs them to say "new order" or "track order".
  2. User can create a new order by specifying food items and quantities.
  3. Modification of the order is possible by adding or removing items before completion.
  4. Upon completion, the chatbot generates an order ID for tracking.
  5. Users can track their orders using the provided order ID.

- **Dialogflow Integration:**
  - Trained the Dialogflow NLP chatbot to understand user statements and intents related to ordering and tracking.

- **Backend Implementation:**
  - Utilizes Flask for handling HTTP requests.
  - In-memory storage (`inprogress_orders`) manages orders in progress until completion.
  - MySQL database stores information about food items, order tracking, and order details.

- **Ngrok for Localhost Security:**
  - Ngrok is used to secure the localhost, allowing Dialogflow to communicate with the backend over a secure HTTPS connection.

## Prerequisites

- Python (>=3.6)
- FastAPI
- Dialogflow Account and Project
- MySQL Database
- Ngrok

## Getting Started

- **Clone the repository:**
  - Utilizes Flask for handling HTTP requests.
  - git clone https://github.com/your-username/NLP-Chatbot-Food-Ordering.git
  - cd NLP-Chatbot-Food-Ordering

- **Install dependencies:**
  - pip install -r requirements.txt

- Set up MySQL database and configure db_config in db_helper.py with your credentials.

- **Run Ngrok to secure the localhost:**
  - ngrok http 8000

- Update the Dialogflow fulfillment URL with the Ngrok HTTPS URL.

- **Run the FastAPI application:**
  - uvicorn main:app --reload

- Access the chatbot interface by opening home.html in a web browser.

## Usage
- Visit the website and interact with the chatbot to place new orders, modify existing ones, and track orders.

## Credits
This project was created by kaanztrk (with the help of YouTube series of "codebasics" YouTube channel).
