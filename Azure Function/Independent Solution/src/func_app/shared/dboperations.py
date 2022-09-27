import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import urllib
import shared.config  as connection
import logging

connectionString = connection.connectionString
    
def executeStoredProcedure(procName,paramList,params,SchemaName = "dbo",isGetResult = 0):

    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()
    cnxn.autocommit = True
    # Prepare the stored procedure execution script and parameter values
    storedProc = "Exec ["+SchemaName+"].["+procName+"] " + paramList
    # Execute Stored Procedure With Parameters
    cursor.execute(storedProc, params)
    
    # Iterate the cursor
    if isGetResult == 1:
        row = cursor.fetchone() 
    elif isGetResult == 2:
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchall() 
        for i in range(0,len(row)):
            row[i]=tuple(row[i])
        sql_data = pd.DataFrame(row, columns=columns)
    else:
        cursor.commit()
    # Close the cursor and delete it
    cursor.close()
    del cursor

    # Close the database connection
    cnxn.close()  
    if isGetResult == 1:
        return row
    elif isGetResult == 2:
        return sql_data
    else:    
        return "Data inserted successfully"


def insertDataFromDF(df, TableName, SchemaName = "dbo"):

    # Configure the Connection
    Params = urllib.parse.quote_plus(connectionString)
    ConnStr = 'mssql+pyodbc:///?odbc_connect={}'.format(Params)
    Engine = create_engine(ConnStr)
    
    # Load the Data in DataFrame into Table
    #index = False is to support identity column
    df.to_sql(TableName, con=Engine, schema=SchemaName, if_exists='append',index = False)
    return "Data inserted successfully"
  

# Test script
if __name__ == "__main__":
    data = executeStoredProcedure("usp_getpitagcount","@equipmentcluster = ?", ("BOG System"),"dbo",1)
    print(data[0])
