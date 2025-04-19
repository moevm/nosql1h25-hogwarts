#!/bin/bash

API_URL="http://localhost:5000/api"

# факультеты
curl -X POST "$API_URL/houses" -H "Content-Type: application/json" -d '{
  "name": "Gryffindor",
  "founder": "Godric Gryffindor"
}'

echo

curl -X POST "$API_URL/houses" -H "Content-Type: application/json" -d '{
  "name": "Slytherin",
  "founder": "Salazar Slytherin"
}'

echo

# зелья
curl -X POST "$API_URL/poisons" -H "Content-Type: application/json" -d '{
  "name": "Polyjuice Potion",
  "effect": "Allows user to take the form of someone else",
  "difficulty": "Hard"
}'

echo

curl -X POST "$API_URL/poisons" -H "Content-Type: application/json" -d '{
  "name": "Draught of Living Death",
  "effect": "Puts the drinker into a death-like slumber",
  "difficulty": "Very Hard"
}'

echo

# заклинания
curl -X POST "$API_URL/spells" -H "Content-Type: application/json" -d '{
  "name": "Expelliarmus",
  "effect": "Disarms your opponent",
  "type": "Charm"
}'

echo

curl -X POST "$API_URL/spells" -H "Content-Type: application/json" -d '{
  "name": "Avada Kedavra",
  "effect": "Causes instant death",
  "type": "Curse"
}'

echo

# персонажи
curl -X POST "$API_URL/characters" -H "Content-Type: application/json" -d '{
  "name": "Hermione Granger",
  "born": "1979-09-19",
  "died": null,
  "blood_status": "muggle-born",
  "gender": "female",
  "description": "Brightest witch of her age",
  "house": "Gryffindor",
  "spells": ["Expelliarmus"],
  "poisons": ["Draught of Living Death"],
  "relationships": [
    {
      "target_character": "Harry Potter",
      "type": "friend"
    }
  ]
}'

echo

curl -X POST "$API_URL/characters" -H "Content-Type: application/json" -d '{
  "name": "Draco Malfoy",
  "born": "1980-06-05",
  "died": null,
  "blood_status": "pure-blood",
  "gender": "male",
  "description": "Son of Lucius Malfoy",
  "house": "Slytherin",
  "spells": ["Avada Kedavra"],
  "relationships": [
    {
      "target_character": "Harry Potter",
      "type": "rival"
    }
  ]
}'

echo

curl -X POST "$API_URL/characters" -H "Content-Type: application/json" -d '{
  "name": "Harry Potter",
  "born": "1980-07-31",
  "died": null,
  "blood_status": "half-blood",
  "gender": "male",
  "description": "The Boy Who Lived",
  "house": "Gryffindor",
  "spells": ["Expelliarmus"],
  "poisons": ["Polyjuice Potion"],
  "relationships": [
    {
      "target_character": "Hermione Granger",
      "type": "friend"
    },
    {
      "target_character": "Draco Malfoy",
      "type": "rival"
    }
  ] 
}'

echo
