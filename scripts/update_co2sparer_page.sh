#! /bin/bash
echo "FIRST LINE"
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
#set -e
#set -u
echo "STARTED"
#git clone https://github.com/co2sparer/co2sparer.github.io.git
#git clone git@github.com:co2sparer/co2sparer.github.io.git
cd $SCRIPT_DIR

eval `ssh-agent`
ssh-add ~/.ssh/co2sparer_update_deploy_key

git pull
# retrieve data
#curl https://api.awattar.de/v1/marketdata > market_data_next_24h.json
/usr/bin/python3 reformat_json_to_table.py
echo "RAN PYTHON"
cp README.md ..
# remove old files
echo "REMOVING README"
rm README.md
echo "UPDATING GIT NOW"
# update git commit
git add --all
START_TIME=`date '+%Y-%m-%d-%H:%M:%S'`
git commit -m "AUTOMATIC UPDATE PRICE LIST: $START_TIME"
git push origin main
echo "DONE!!"
