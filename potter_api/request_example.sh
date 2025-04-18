curl -X POST http://localhost:5000/api/houses      -H "Content-Type: application/json"      -d '{
           "name": "Gryffindor",
           "founder": "Godric Gryffindor"
         }'


curl -X POST http://localhost:5000/api/poisons      -H "Content-Type: application/json"      -d '{
           "name": "Veritaserum"
         }'


curl -X POST http://localhost:5000/api/spells      -H "Content-Type: application/json"      -d '{
           "name": "Expelliarmus"
         }'


curl -X POST http://localhost:5000/api/spells      -H "Content-Type: application/json"      -d '{
           "name": "Lumos"
         }'


curl -X POST http://localhost:5000/api/characters      -H "Content-Type: application/json"      -d '{
           "name": "Draco Malfoy",
           "blood_status": "pure-blood",
           "gender": "male"
         }'


curl -X POST http://localhost:5000/api/characters      -H "Content-Type: application/json"      -d '{
           "name": "Hermione Granger",
           "blood_status": "muggle-born",
           "gender": "female",
           "house": "Gryffindor"
         }'


curl -X POST http://localhost:5000/api/characters      -H "Content-Type: application/json"      -d '{
           "name": "Harry Potter",
           "blood_status": "half-blood",
           "gender": "male",
           "description": "The Boy Who Lived",
           "house": "Gryffindor",
           "spells": ["Expelliarmus", "Lumos"],
           "poisons": ["Veritaserum"],
           "relationships": [
               {
                   "target_character": "Hermione Granger",
                   "type": "Friend"
               },
               {
                   "target_character": "Draco Malfoy",
                   "type": "Enemy"
               }
           ]
         }'