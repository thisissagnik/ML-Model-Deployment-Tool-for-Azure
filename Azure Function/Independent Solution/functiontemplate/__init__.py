import logging
import datetime
import json 
import pandas as pd

import azure.functions as func
import os
import sys

def main(myblob: func.InputStream):
                 
    dir_abs_path = os.getcwd()
    sys.path.insert(0, dir_abs_path)

    from ${func_model}.score import init, run
    from ${func_model}.config import model_name
    from shared.exceptions import EmptyInputfileError,NonUniqueTimeStampError,PiTagMissmatchError,NonNumericValueError,SQLDataLoadError,FileMovementError,ModelScoringError

    try:

        jsonData= json.load(myblob)
        dt = pd.DataFrame.from_dict(jsonData)
        ############################################################################################
        ###                                 Validate Raw Data
        ############################################################################################


        ###########################################################################################
        ##                                 Load Raw Data
        ###########################################################################################


        ############################################################################################
        ###                                 DATA Transformation
        ############################################################################################


        ############################################################################################
        ###                                 Model Prediction
        ############################################################################################

        #Load the ML Model
        try:
            init(model_name)
            pred_result, pred_proba = run(dt)
            pred_result = float(pred_result[0])

        except Exception as ex:
            raise ModelScoringError("Exception with Model prediction process: "+ str(ex))


        ############################################################################################
        ###                                 Save Predictions 
        ############################################################################################


    except Exception as ex:
        logging.error(f"Error Code : {ex.errcode} \n"
                      f"Error Type : {ex.errtype} \n"                         
                      f"Error Message : {ex.errmsg} \n")
    
        src = myblob.name