# Read arguments
#acrname:acrRepoName:image
while getopts a:r:i: flag
do
    case "${flag}" in
        a) acrname=${OPTARG};;
        r) acrrepo=${OPTARG};;
        i) imagename=${OPTARG};;
    esac
done


# Working directory to "/src"
# cd "src/"
cd ".."


#Build and deploy docker images 

docker build --tag "$imagename" .
az acr login --name "$acrname"
docker push  "$imagename"

# echo $image_tag
echo "Docker Build Successfully."
