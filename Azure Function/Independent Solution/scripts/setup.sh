# Read arguments
#model:type
while getopts m:t: flag
do
    case "${flag}" in
        m) model=${OPTARG};;
        t) type=${OPTARG};;
    esac
done
echo "Model Name: $model";
echo "Function Type: $type";

# Working directory to "../func_app"
cd "../src/func_app"

# Step 1: Create Function App code template using the parameters
func init --worker-runtime python --docker 
func new --name "func_${model}" --template "$type" #Azure Blob Storage trigger

# cp -f ../requirements.txt requirements.txt

# Step 2: Update function app structure to call and score models
# Update function level files
cp ../../functiontemplate/score.py "func_${model}"/
cp ../../functiontemplate/config.py "func_${model}"/
cp -f ../../functiontemplate/__init__.py "func_${model}"/__init__.py
cp -f ../../functiontemplate/function.json "func_${model}"/function.json

# Copy model file from model_path to function app
cp -r ../../model/"$model."* "func_${model}"/

#Replace the placeHolders with paramanets
#1. Replace place holders in config file
sed -i "s/\${model}/$model/" "func_${model}"/config.py
#2. Replace the function folder name in __init__ file
sed -i "s/\${func_model}/func_${model}/g" "func_${model}"/__init__.py
#3. Replace function path in function.json file
sed -i "s/\${model}/$model/" "func_${model}"/function.json


