#!/bin/bash

curl -X POST http://localhost:5000/api/import \
  -H "Content-Type: application/json" \
  -d '{
  "houses": [
    {
      "name": "Gryffindor",
      "traits": ["bravery", "courage"]
    },
    {
      "name": "Slytherin",
      "traits": ["cunning", "ambition"]
    }
  ],
  "spells": [
    {
      "name": "Expelliarmus",
      "effect": "Disarms the opponent",
      "type": "Charm"
    },
    {
      "name": "Avada Kedavra",
      "effect": "Kills instantly",
      "type": "Curse"
    }
  ],
  "poisons": [
    {
      "name": "Polyjuice Potion",
      "effect": "Takes the form of someone else",
      "difficulty": "Hard"
    },
    {
      "name": "Draught of Living Death",
      "effect": "Induces death-like sleep",
      "difficulty": "Very Hard"
    }
  ],
  "characters": [
    {
      "name": "Harry Potter",
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
    },
    {
      "name": "Hermione Granger",
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
    },
    {
      "name": "Draco Malfoy",
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
    }
  ]
}'
