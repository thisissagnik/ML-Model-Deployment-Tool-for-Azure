from azureml.core.webservice import AksWebservice, Webservice
from azureml.core.model import Model
from azureml.core.compute import AksCompute
from azureml.core.model import InferenceConfig
from azureml.core import Environment
from azureml.core import Workspace
from azureml.core.conda_dependencies import CondaDependencies
import logging
import yaml
import ast
from azureml.exceptions import UserErrorException
from azureml.core import Run
#===================Load configurations===================
try:
    with open('config.yaml', 'r') as file:
        confg = yaml.safe_load(file)
except (IOError, ValueError, EOFError, FileNotFoundError) as ex:
    logging.error("Config file not found")
    logging.error(ex)
    raise ex
except Exception as YAMLFormatException:
    logging.error("Config file not found")
    logging.error(YAMLFormatException)
    raise YAMLFormatException
#=======================Parse configurations======================
deploymentConfig = str(confg.get('DeploymentConfig',{})) 

deploymentConfig = ast.literal_eval(deploymentConfig) 
#==================================================================

def getAMLWorkspace():
    try:
        ws = Workspace.from_config()
    except UserErrorException as ex:
        current_run = Run.get_context()
        ws = current_run.experiment.workspace
    except Exception as ex:
        ws = Workspace(subscription_id=subscription_id,
                resource_group=resource_group,
                workspace_name=workspace_name)   
    return ws

def deploy():
    '''
    Description: Deploy method to setup model and environment and deploy model from AML workspace
    '''
    try:
        ws = getAMLWorkspace()

        logging.info("Workspace configuration succeeded")
    except Exception as ex:
        logging.error("Workspace not accessible. Change your parameters or create a new workspace")
        raise ex
        
    try:
        logging.info("Start: Model registration")
        model = Model.register(ws,model_name=model_name, model_path=model_path)
    except Exception as ex:
        logging.error("Error in model registration")
        raise ex

    # try:
    #     # Load existing environment if exists, else create one
    train_env = Environment.get(workspace=ws,name="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu")
    # except:
        # print("Creating Environment")
        # train_env = Environment.from_pip_requirements(env_name, source_directory+"requirement.txt")
        # train_env.register(workspace=ws)

    # Prepare inference configuration
    inference_config = InferenceConfig(source_directory=source_directory,entry_script=entry_script,environment=train_env)

    # Deploy model to AKS endpoint
    try:
        logging.info("Start: Model deployment")
        aks_target = AksCompute(ws,aks_cluster_target)
        
        # Deployment configuration of the endpoint
        deployment_config = AksWebservice.deploy_configuration(cpu_cores = 2, memory_gb = 2, auth_enabled=False)

        service = Model.deploy(ws, deploymentEndpoint, [model], inference_config, deployment_config, aks_target, overwrite=True)
        service.wait_for_deployment(show_output=True)
        logging.info(service.state)
        logging.info(service.scoring_uri)
    except Exception as ex:
        logging.error("Error in model deployment")
        raise ex

if __name__ == "__main__":

    # Parse input arguments
    subscription_id = deploymentConfig.get("subscription_id")
    resource_group = deploymentConfig.get("resource_group")
    workspace_name = deploymentConfig.get("amlworkspace")
    entry_script = deploymentConfig.get("entryScriptname")
    env_name = deploymentConfig.get("environmentname")
    aks_cluster_target = deploymentConfig.get("akscluster")
    deploymentEndpoint = deploymentConfig.get("deploymentendpointname")
    source_directory = deploymentConfig.get("source_directory")
    model_name=deploymentConfig.get("modelname")
    model_path=model_name+'.sav'

    deploy()
    