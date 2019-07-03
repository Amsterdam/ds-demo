# ds-demo

Demo project for Data Services

# Requirements

    Python >= 3.5

# Local running

## Preparation for running and developing locally

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r src/requirements.txt
    
    docker-compose up -d database

## Run the server locally

Make sure port 8000 is available     

    export DJANGO_SETTINGS_MODULE=ds_demo.settings
    ./src/manage.py runserver
    
Open your browser with the [health-check](http://localhost:8000/heatlth)

# Running in Docker
 
## Preparation for running and developing locally
 
Make sure port 8000 is available     
     
     docker-compose up -d
     
Open your browser with the [health-check](http://localhost:8000/heatlth)
 