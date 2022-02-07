#! /bin/bash
#set -e
#set -u
# external parameters:
BASE_REQUEST_URL=$1
echo "STARTED"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# activate local python virtual environment
echo $SCRIPT_DIR/../venv/bin/activate
source $SCRIPT_DIR/../venv/bin/activate

#git clone https://github.com/co2sparer/co2sparer.github.io.git
#git clone git@github.com:co2sparer/co2sparer.github.io.git
cd $SCRIPT_DIR

eval `ssh-agent`
ssh-add ~/.ssh/co2sparer_update_deploy_key

git pull
# retrieve data
python reformat_json_to_table.py $BASE_REQUEST_URL
cp README.md ..
# remove old files
rm README.md

# update git commit
git add --all
START_TIME=`date '+%Y-%m-%d-%H:%M:%S'`
git commit -m "AUTOMATIC UPDATE PRICE LIST: $START_TIME"
git push origin main
echo "DONE!!"
