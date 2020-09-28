# Age of Empires 2 API
[![Build Status](https://travis-ci.com/aalises/age-of-empires-II-api.svg?branch=master)](https://travis-ci.com/aalises/age-of-empires-II-api)
[![Coverage Status](https://coveralls.io/repos/github/aalises/age-of-empires-II-api/badge.svg?branch=master)](https://coveralls.io/github/aalises/age-of-empires-II-api?branch=master)
[![Docker Image](https://img.shields.io/badge/Docker%20image-latest-blue.svg?link=https://hub.docker.com/r/aalises/aoe2api/)](https://hub.docker.com/r/aalises/aoe2api/)


API available at : https://age-of-empires-2-api.herokuapp.com

Age of Empires II API created with:
 - `Flask + FlaskRESTful` 
 - `SQLite` (DB)
 - `SQLAlchemy` (ORM)
 - `Flasgger` (Swagger Docs)
 - `Pytest + Coverage` (Tests)

Which allows you to retrieve information about the civilizations, technologies, units and structures of AOE2. To run you can use `Docker`, for example:

```
docker build -t aoe2api:v1 .
docker run --name aoe2api -p 8080:80 -d aoe2api:v1 
```
or pull the image from DockerHub:

```
docker pull aalises/aoe2api:latest
```
The routes are: 
- Main API route: `localhost:8080/api/v1`
- Docs Route: `localhost:8080/docs`

To test using `pytest`, just run

```
python -m pytest
```

For testing the coverage using `coverage` run:

```
coverage run -m pytest
```
## Models
---

### Civilization
---
Model describing a civilization in AOE2.
Parameters:

- **_id**: Integer denoting the unique ID for that civilization
- **name**: Name of the civilization (e.g Britons)
- **expansion**: Expansion the civilization was introduced
- **army_type**: Predominant army type of the civilization (e.g Archers, or Infantry)
- **unique_unit**: Unique unit of the civilization
- **unique_tech**: Unique Technology of the Civilization
- **team_bonus**: Bonuses for the Team the civilization belongs to
- **civilization_bonus**: Bonuses of the civilization

### Technology
---
Model describing a Technology in AOE2.
Parameters:

- **_id**: Integer denoting the unique ID for that technology
- **name**: Name of the technology
- **expansion**: Expansion the technology was introduced
- **age**: Age in which the technology can be developed
- **develops_in**: structure in which the technology is developed
- **cost**: Cost of the technology (JSON object)
- **build_time**: Build time in seconds
- **applies_to**: Units or civilizations the technology applies to
- **description**: Description of the technology

### Unit
---
Model describing a Unit in AOE2.
Parameters:

- **_id**: Integer denoting the unique ID for that unit
- **name**: Name of the unit
- **description**: Description of the unit
- **expansion**: Expansion the unit was introduced
- **age**: Age in which the unit can be produced
- **created_in**: Structure the unit is created in
- **cost**: Cost of the unit (JSON object)
- **build_time**: Build time in seconds
- **reload_time**: Reload time (Float)
- **attack_delay**: Attack delay when you give the order to attack (Float)
- **movement_rate**: Movement Rate
- **line_of_sight**: Line of sight of the unit
- **hit_points**: Hit points (health) of the unit
- **range**: Range of the unit. There can be a minimum and maximum range in the format (min-max)
- **attack**: Attack of the unit
- **armor**: Armor of the unit divided into melee/pierce
- **attack_bonus**: Attack bonuses of the unit
- **armor_bonus**: Armor bonuses of the unit
- **search_radius**: Search Radius of the unit
- **accuracy**: Attack accuracy (percentage) of the unit
- **blast_radius**: Attack blast radius

### Structure
---
Model describing a Structure in AOE2.
Parameters:

- **_id**: Integer denoting the unique ID for that structure
- **name**: Name of the structure
- **expansion**: Expansion the structure was introduced
- **age**: Age in which the structure can be created
- **cost**: Cost of the structure (JSON object)
- **build_time**: Build time in seconds
- **hit_points**:  Hit points (health) of the structure
- **line_of_sight**: Line of sight of the structure
- **armor**:  Armor of the structure divided into melee/pierce
- **range**: Range of the structure. There can be a minimum and maximum range in the format (min-max)
- **reload_time**: Reload time in seconds between projectiles
- **attack**: Attack of the structure
- **special**: Some other properties of the structure / garrison


## Resources

The API allows to retrieve information about **civilizations, structures, units and technologies** for the AOE2 Age of Kings and The Conquerors.
The base route returns an object with the different resources you can access

- ### GET /civilizations
Gets all civilizations in a JSON list
- ### GET /civilization/<id: string>
Gets a given civilization with a string representing an ID (integer e.g 1, 34), or the name (britons,teutons). The name instead of spaces can be parsed with underscores or hyphens.

Example call `/api/v1/civilization/bizantines`

```
{
  "id": 3, 
  "name": "Bizantines", 
  "expansion": "Age of Kings", 
  "army_type": "Defensive", 
  "unique_unit": [
    "http://localhost/unit/cataphract"
  ], 
  "unique_tech": [
    "http://localhost/technology/logistica"
  ], 
  "team_bonus": "Monks +50% heal speed", 
  "civilization_bonus": [
    "Buildings (except gates) have +10% HP in Dark Age / +20% HP in Feudal Age  / +30% in Castle Age / +40% in Imperial Age", 
    "Spearman skirmisher and camel lines cost 25% less", 
    "Fire Ships attack 20% faster", 
    "Imperial Age costs -33%", 
    "Town Watch is free"
  ]
}
```

- ### GET /units
Gets all units in a JSON list

- ### GET /unit/<id: string>
Gets a given unit with a string representing an ID (integer e.g 1, 34), or the name longbowman, archer). The name instead of spaces can be parsed with underscores or hyphens (unit/teutonic_knight or unit/turtle-ship, for example)

Example call `/api/v1/unit/berserk`

```
{
  "id": 69, 
  "name": "Berserk", 
  "description": "Viking unique unit. Infantry that slowly heals itself", 
  "expansion": "Age of Kings", 
  "age": "Castle", 
  "created_in": "http://localhost/structure/castle", 
  "cost": {
    "Food": 65, 
    "Gold": 25
  }, 
  "build_time": 16, 
  "reload_time": 2.0, 
  "movement_rate": 1.05, 
  "line_of_sight": 3, 
  "hit_points": 55, 
  "attack": 9, 
  "armor": "0/1", 
  "attack_bonus": [
    "+2 eagles", 
    "+2 buildings"
  ]
}
```

- ### GET /structures
Gets all structures in a JSON list

- ### GET /structure/<id: string>
Gets a given structure with a string representing an ID (integer e.g 1, 34), or the name (mill, market). The name instead of spaces can be parsed with underscores or hyphens (structure/siege_workshop, for example)

Example call `/api/v1/structure/29`
```
 {
    "id": 29, 
    "name": "Mill", 
    "expansion": "Age of Kings", 
    "age": "Castle", 
    "cost": {
      "Wood": 100
    }, 
    "build_time": 35, 
    "hit_points": 1000, 
    "line_of_sight": 5, 
    "armor": "2/9", 
    "special": [
      "Max 40 farms queued"
    ]
  }
```

- ### GET /technologies
Gets all technologies in a JSON list

- ### GET /technology/<id: string>
Gets a given technology with a string representing an ID (integer e.g 1, 34), or the name (masonry, architecture). The name instead of spaces can be parsed with underscores or hyphens (technology/garland_wars, for example)

Example call `/api/v1/technology/gold_mining`
```
{
  "id": 58, 
  "name": "Gold Mining", 
  "expansion": "Age of Kings", 
  "age": "Feudal", 
  "develops_in": "http://localhost/structure/mining_camp", 
  "cost": {
    "Food": 100, 
    "Wood": 75
  }, 
  "build_time": 30, 
  "applies_to": [
    "Gold Miners"
  ], 
  "description": "Work rate * 1.15 (15% faster)"
}
```

## Donations

The Age of Empires II API was originally conceived as a pet project, and is using the free plan on Heroku. As some people is using it, we are running out of the free dyno hours on Heroku so the API is down.

Help to keep it running! If you're using it as a teaching resource or for a project, consider sending a $7 donation to help keep the service up for one more month, as we will be able to upgrade to the Hobby plan on Heroku.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=A3MTLTHWX686N&source=url)

Become a backer!

