import ibm_db

try:
 con=ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fzn32689;PWD=bPKXp7YkTR3uKK3a",'','')
 print(con)
 stmt=ibm_db.exec_immediate(con,"SELECT  * FROM registration")
 print("SUCCESSFULLY CONNECTED")
except:
    print("failed")