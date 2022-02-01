# Google Rasa Entegration

## Description
Entegration of Google Speech To Text API and Google Text To Speech API to Rasa (an open-source machine learning framework for conversational AI). In this way, we can use Rasa chatbot with our voice and get responses with Google's voice.

## Installation
Clone this repository, install Rasa with pip (pip install rasa), use "rasa init", then train Rasa with "rasa train" command. 

Also you need an Google Cloud account that these APIs activated. You need to get your API Service Account Key and change its path from code (Speech.py 16).

## Usage
Use "rasa run --enable-api" to run rasa server. Run our python program with "python addons/Speech.py" and say something. 

## Roadmap
This is a demo for now. I will improve it.

## Project status
I am currently continue developing.