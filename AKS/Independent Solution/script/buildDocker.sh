# Read arguments
#acrname:acrrepo
while getopts a:r: flag
do
    case "${flag}" in
        a) acrname=${OPTARG};;
        r) acrrepo=${OPTARG};;
    esac
done

# Working directory to "/src"
cd "../"

#Create a tag for the new image
image_tag=$(date '+%Y%m%d%H%M%S')

echo "ACR Name: $acrname";
echo "Release Tag: $image_tag";
echo "ACR Repository Name:$acrrepo";
#Build and deploy docker images 

docker build --tag "$acrname"/"$acrrepo":"$image_tag" .
az acr login --name "$acrname"
docker push  "$acrname"/"$acrrepo":"$image_tag"
