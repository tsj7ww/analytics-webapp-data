STAGE="dev" # dev, test, prod

if [$STAGE == "dev"]
then
   docker compose ./base/docker-compose.yml dev
elif [$STAGE == "test"]
then
    docker compose ./base/docker-compose.yml test
elif [$STAGE == "prod"]
then
    terraform ./init.tf
else
   echo "Error!"
fi 

python ./base.py $STAGE