# AWT-Project

## Getting started
Run the following in root folder to start the system:

- `docker-compose up --build` Build Server and then start Neo4J Database and Server
- `curl -X POST http://localhost:5000/initialize` Initiliaze the Database and Store (takes around 5 Minutes)


## Development
Use the following commands for development:

- `pipenv install` to install requirements
- `pipenv run python -m flask run` to start the server (for Dev/Debug purposes)
- `curl -X POST http://localhost:5000/initialize` to initiliaze the Database and Store (takes around 10 Minutes)
- `docker-compose start db` Only start Neo4J Database
- `pipenv run python -m spacy download de_core_news_sm` To download german spaCy Data
- `pipenv run python -m spacy download en_core_web_sm` To download english spaCy Data

### Clean up Database
1. `match (a) -[r] -> () delete a, r` to clean up relations
2. `match (a) delete a` to clean up nodes

## API server
You can find the documentation of our API at `http://localhost:5000/api/docs` once you have the system up and running.

## Preprocessing
To use the preprocessing pipeline use the following code:
```
from app.preprocessing_utils import PreprocessorGerman
prc_pipeline = PreprocessorGerman()
preprocessed_course_descriptions = prc_pipeline.preprocess_course_descriptions(course_descriptions)
```
