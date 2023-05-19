STAGE="dev" # dev, test, prod

if [$STAGE == "dev"]
then
   statement1
elif [$STAGE == "test"]
then
    statement1
elif [$STAGE == "prod"]
then
    sh ./init.tf
    
else
   
fi 