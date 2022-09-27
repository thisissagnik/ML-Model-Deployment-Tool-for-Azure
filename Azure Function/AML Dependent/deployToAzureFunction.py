from azureml.core.model import Model
from azureml.core.model import InferenceConfig
from azureml.core import Environment
from azureml.core import Workspace
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DockerConfiguration
import logging
import yaml
import ast
from azureml.exceptions import UserErrorException
from azureml.core import Run
from azureml.contrib.functions import package
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

    try:
        # Load existing environment if exists, else create one
        train_env = Environment.get(workspace=ws,name="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu")
    except:
        print("Creating Environment")
        train_env = Environment.from_pip_requirements(env_name, source_directory+"requirement.txt")
        train_env.register(workspace=ws)
    docker_config = DockerConfiguration(use_docker=True)
    # Prepare inference configuration
    inference_config = InferenceConfig(source_directory=source_directory,entry_script=entry_script,environment=train_env)

    # Deploy model to Azure Function endpoint
    try:
        logging.info("Start: Model deployment")

        docker_image = package(ws, [model], inference_config, auth_level=None,trigger="http")
        docker_image.wait_for_creation(show_output=True)
        logging.info(docker_image.state)
        logging.info(docker_image.scoring_uri)
        
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
    source_directory = deploymentConfig.get("source_directory")
    model_name=deploymentConfig.get("modelname")
    model_path=model_name+'.sav'

    deploy()
    