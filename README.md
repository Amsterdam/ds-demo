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
 
# Uploading a schema

    curl -X POST \
      http://localhost:8000/ds_demo/schemas/ \
      -H 'Content-Length: 3280' \
      -H 'Content-Type: application/json' \
      -d '{
                "name": "bouwdossiers",
                "description": "Beschrijving",
                "schema": {
                    "$id": "https://schemas.data.amsterdam.nl/v0.1/bouwdossiers",
                    "type": "object",
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "required": [
                        "id",
                        "dataset",
                        "type"
                    ],
                    "properties": {
                        "id": {
                            "$ref": "https://schemas.data.amsterdam.nl/v0.1#/definitions/id"
                        },
                        "type": {
                            "type": "string"
                        },
                        "titel": {
                            "type": "string",
                            "description": "Titel"
                        },
                        "dataset": {
                            "$ref": "https://schemas.data.amsterdam.nl/v0.1#/definitions/dataset"
                        },
                        "adressen": {
                            "type": "array",
                            "items": {
                                "$ref": "https://schemas.data.amsterdam.nl/v0.1#/definitions/uri",
                                "$class": "https://schemas.data.amsterdam.nl/v0.1/bag#verblijfsobject"
                            },
                            "description": "Lijst van adressesn waarop dit bouwdossier betrekking heeft"
                        },
                        "datering": {
                            "type": "string",
                            "description": "Datering"
                        },
                        "openbaar": {
                            "type": "boolean",
                            "description": "Openbaar"
                        },
                        "stadsdeel": {
                            "$ref": "https://schemas.data.amsterdam.nl/v0.1#/definitions/uri",
                            "$class": "https://schemas.data.amsterdam.nl/v0.1/gebieden#stadsdeel",
                            "description": "Stadsdeel"
                        },
                        "dossiertype": {
                            "type": "string",
                            "description": "Dossiertype"
                        },
                        "subdossiers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "titel": {
                                        "type": "string"
                                    },
                                    "bestanden": {
                                        "type": "array",
                                        "items": {
                                            "type": "string",
                                            "format": "uri"
                                        },
                                        "minItems": 1
                                    }
                                }
                            },
                            "description": "Subdossiers"
                        },
                        "dossiernummer": {
                            "type": "string",
                            "description": "Dossiernummer"
                        }
                    },
                    "additionalProperties": false
                }
            }'