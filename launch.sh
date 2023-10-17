#bin/bash

# Activate conda capabilities
eval "$(conda shell.bash hook)"
source ~/Apps/miniconda3/etc/profile.d/conda.sh

# check if screen is running and quit if it is
if screen -list | grep -q "website"; then
    screen -X -S "website" quit
fi 

# Launch the website and server

cd website &&
screen -dmS website bash -c "npm run dev" &&
cd .. &&

cd server &&
conda activate IML-app &&
python server.py &&

# Close sreen when server is closed
screen -X -S "website" quit