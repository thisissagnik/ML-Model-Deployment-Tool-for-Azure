# Read arguments from config file
. configuration/config.cfg

#Create a tag for the new image
image_tag=$(date '+%Y%m%d%H%M%S')

# gererate the image name
imagename="$acrname"/"$acrrepo":"$image_tag"

# build the docker image using buildDocker.sh and push the image to ACR
bash buildDocker.sh -a $acrname -r $acrrepo -i $imagename

# Get resource ID of the user-assigned identity
userID=$(az identity show --resource-group $regname --name $acimsi --query id --output tsv)

echo "ACR Name: $acrname";
echo "Release Tag: $image_tag";
echo "ACR Repository Name:$acrrepo";
echo "ACI Name: $aciname";
echo "Resource Group: $regname";
echo "Image Name: $imagename";
echo "ACI Assigned Identity: $userID";

# set MSYS_NO_PATHCONV to 1 to execute container instance script using bash terminal
export MSYS_NO_PATHCONV=1

# Create Azure container instance with the latest image pushed into ACR by dockerBuild.sh
az container create \
    --name $aciname \
    --resource-group $regname \
    --image $imagename \
    --acr-identity $userID \
    --assign-identity $userID \
    --ports 80 \
    --dns-name-label aci-image-$image_tag

echo 'ACI created and Image deployed successfully.'