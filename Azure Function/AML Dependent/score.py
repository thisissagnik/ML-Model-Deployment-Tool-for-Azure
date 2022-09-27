import logging
import datetime
import json
import pandas as pd
import numpy as np
import pickle
import os
import sys
import joblib
from azureml.core import Workspace
from azureml.core.model import Model

def init():
    ############################################################################################
    ###                 LOADING THE MODEL
    ############################################################################################
    global model

    print(os.getenv('AZUREML_MODEL_DIR'))
    model_name="diabetes"
    # Get the path to the deployed model file and load it
    try: 
        logging.info("Loading from saved file")
        model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), model_name+".sav")
        model = joblib.load(model_path)
    except:
        logging.info("Loading registered model")
        model_path = Model.get_model_path(model_name)
        model = joblib.load(model_path)
    
    
############################################################################################
###                                     MODEL RUN 
############################################################################################
def run(dt):
    print("==========Start: Model scoring============")
    ############################################################################################
    ###                 Data pre processing
    ############################################################################################
    print(dt)
    result_df = pd.read_json(json.loads(dt))

    print(result_df)
    
    ############################################################################################
    ###                 PREDICT THE RESULT
    ############################################################################################
    pred_result = model.predict(result_df)
    pred_proba = model.predict_proba(result_df)[::,1]

    print(pred_result)
    print("==========End: Model scoring============")
    return json.dumps({"result": "Success"})
