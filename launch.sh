#bin/bash

if screen -list | grep -q "website"; then
    screen -X -S "website" quit
fi 

cd website &&
screen -dmS website bash -c "npm run dev" &&
cd .. &&

cd server &&
python server.py &&
screen -X -S "website" quit