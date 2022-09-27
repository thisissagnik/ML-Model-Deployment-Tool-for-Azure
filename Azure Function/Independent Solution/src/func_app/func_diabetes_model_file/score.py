############################################################################################
###                 PLATFORM CONFIG 
############################################################################################

import logging
import datetime
import json
import pandas as pd
import numpy as np
import pickle
import os
import sys


def init(model_name):

    global model

    ############################################################################################
    ###                 LOADING THE MODEL
    ############################################################################################
    
    dir_path = os.path.dirname(os.path.abspath(__file__))
    
    modelfile = open(dir_path+"/"+model_name, "rb")  
    model = pickle.load(modelfile)

############################################################################################
###                                     MODEL RUN 
############################################################################################
def run(dt):

    ############################################################################################
    ###                 Data pre processing
    ############################################################################################
    result_df = dt


    ############################################################################################
    ###                 PREDICT THE RESULT
    ############################################################################################
    # Sample_Input_tran =input_data

    pred_result = model.predict(result_df)
    pred_proba = max(model.predict_proba(result_df.values.reshape(1,-1))[0]) #Added changes to fetch the max out of the list for prediction probability

    return pred_result, pred_proba



def main():
    init("")
    jsonData = []
    
    print(run(jsonData))

if __name__ == "__main__":
    main()