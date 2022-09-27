# This script helps to setup user managed identity that can be used to pull private docker images from ACR to ACI.

# Read arguments from config file
. configuration/config.cfg

# create user managed identity
az identity create --resource-group $regname --name $acimsi
# Get resource ID of the user-assigned identity
userID=$(az identity show --resource-group $regname --name $acimsi --query id --output tsv)
# Get service principal ID of the user-assigned identity
spID=$(az identity show --resource-group $regname --name $acimsi --query principalId --output tsv)
# Get the Resource ID of ACR
registry_id=$(az acr show -n $acrname --query id --output tsv)

echo "MSI Resource ID: $userID"
echo "MSI Service Principal ID: $spID"
echo "ACR Resource ID: $registry_id"

# set MSYS_NO_PATHCONV to 1 to execute container instance script using bash terminal
export MSYS_NO_PATHCONV=1

# grant the acrpull role to the identity 
az role assignment create --assignee $spID --scope $registry_id --role acrpull

