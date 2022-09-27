# Read arguments
#acrname:featurebranchname
while getopts s:r:a:n:c: flag
do
    case "${flag}" in
        s) subscription=${OPTARG};;
        r) resourcegroup=${OPTARG};;
        a) aksservice=${OPTARG};;
        n) deploymentname=${OPTARG};;
        c) deploymentconfigYAML=${OPTARG};; 
    esac
done

echo "Starting deployment"

echo "Resource Group: $resourcegroup";
echo "Kubernetes Service: $aksservice";
echo "Model deployment Name:$deploymentname";
echo "Model deployment configuration YAML:$deploymentconfigYAML";

# Change Working directory to "../" where deployment.yaml is residing
cd "../"

#Connect to Kubernetes
az account set --subscription "$subscription"
az aks get-credentials --resource-group "$resourcegroup" --name "$aksservice"

echo "Connected to AKS service"

# Delete the deployment if already present
kubectl delete deployment.apps/"$deploymentname" --ignore-not-found=true

# Create the deployment as per the deployment.yaml file
kubectl create -f "$deploymentconfigYAML"

# Display the pods and status of deployment
kubectl get pods --show-labels

echo "Deployment completed"