import os

# storage_account = "ptsg5jitadls01"

storage_account = os.environ["adls_storage_account"]
container_name = "pi-data"

#======================================================================
#===================DB Connection configuration========================
#======================================================================

# server = 'ptsg-5jitpidb01.database.windows.net' 
# database = 'ptsg-5jitpidb01'

server = os.environ["SQL_Server_Name"]
database = os.environ["SQL_Server_Database"]

# Windows Authentication based connection string
#connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;'

# SQL Server Authentication based connection string
#username = "xxxxx"
#password = "xxxxx"
#connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password

# Managed identity connection string
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Authentication=ActiveDirectoryMsi'