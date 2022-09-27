import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from score import init,run
import time
import pandas as pd
import io
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta

storage_account = 'modelsdeployment'
InputContainerName ='inputblob'
OutputContainerName = 'outputblob'
blobName='diabetes.csv'
account_key="tDk8cTMPcdBDyWRgqmg+2t1f2AN4LT83CKV8noztiXj87M0Rt+39cOas/ASfldE+KGEPmJRIdh6q+AStZOqV4Q=="

def read_data(source,file):
    print("Reading data")
    # creds = ManagedIdentityCredential()

    blob_service_client = BlobServiceClient(account_url= (f"https://{storage_account}.blob.core.windows.net/") , credential=account_key)

    blob = blob_service_client.get_blob_client(container=source, blob=file)
    blobStream = blob.download_blob().readall()

    data = pd.read_csv(io.BytesIO(blobStream))
    print("Completed reading data")
    return data

def write_data(dest,df):
    # creds = ManagedIdentityCredential()

    blob_service_client = BlobServiceClient(account_url= (f"https://{storage_account}.blob.core.windows.net/") , credential=account_key)
    output = df.to_csv(index=False, encoding = "utf-8")
    # Instantiate a new BlobClient
    blob = blob_service_client.get_blob_client(container=dest, blob='diabetes_output.csv')
    # upload data
    blob.upload_blob(output, blob_type="BlockBlob", overwrite=True)


def main():
    init("model/diabetes_model_file.sav")
    jsonData = read_data(InputContainerName,blobName)
    data = jsonData.drop('Outcome', axis=1)

    pred_result, pred_proba = run(data)

    data['Prediction_results'] = pred_result
    data['prediction_probability'] = pred_proba

    print(data)

    write_data(OutputContainerName,data)
    return data.to_json()

if __name__ == "__main__":
    print("Training started")
    main()
    # while True:
    #     time.sleep(60)