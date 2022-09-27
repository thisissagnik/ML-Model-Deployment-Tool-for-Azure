from score import init,run
import os
import pandas as pd
import io
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

storage_account = 'blobstoragetestacc'
InputContainerName ='inputblob'
OutputContainerName = 'outputblob'
blobName='diabetes.csv'


def read_data(source,file):
    creds = ManagedIdentityCredential()
    blob_service_client = BlobServiceClient(account_url= (f"https://{storage_account}.blob.core.windows.net/") , credential=creds)

    blob = blob_service_client.get_blob_client(container=source, blob=file)
    blobStream = blob.download_blob().readall()

    data = pd.read_csv(io.BytesIO(blobStream))

    return data

def write_data(dest,df):
    creds = ManagedIdentityCredential()
    blob_service_client = BlobServiceClient(account_url= (f"https://{storage_account}.blob.core.windows.net/") , credential=creds)
    output = df.to_csv(index=False, encoding = "utf-8")
    # Instantiate a new BlobClient
    blob = blob_service_client.get_blob_client(container=dest, blob='diabetes_output.csv')
    # upload data
    blob.upload_blob(output, blob_type="BlockBlob")


def main():
    init("model/diabetes_model_file.sav")
    jsonData = read_data(InputContainerName,blobName)
    data = jsonData.drop('Outcome', axis=1)

    pred_result, pred_proba = run(data)

    data['Prediction_results'] = pred_result
    data['prediction_probability'] = pred_proba

    # print(data)

    write_data(OutputContainerName,data)



if __name__ == "__main__":
    main()