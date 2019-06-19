from qgis.utils import *
import psycopg2
import os
postgis="0"
schema=''
print (os.path.dirname(os.path.realpath(__file__)).replace('\\','/') + '/db_conf.ini')
if os.path.isfile(os.path.dirname(os.path.realpath(__file__)).replace('\\','/')  + '/db_conf.ini'):


 with open(os.path.dirname(os.path.realpath(__file__)).replace('\\','/')  + '/db_conf.ini', "r") as lines:
    line = lines.read().splitlines()
    postgis = line[4]
    lines.close()

if postgis == "2":
    print (postgis)
    datadb = 'postgres'
    dbName='"'+line[0]+'",'+'"5432"'+',"'+line[1]+'","'+line[2]+'","'+line[3]+'"'
    ocon = psycopg2.connect(host=line[0], port=5432, dbname=line[1],  user= line[2],password=line[3] )
    ocon.set_client_encoding('LATIN1')
    schema = "cxf_in."
    funzsql = "ST_GeomFromText"
   # QMessageBox.information(None, "Dbase Manager :", "Connesso a Postgis")
else:
    print ("spatial")
    postgis = "0"
    datadb = 'spatialite'
    dbName =  os.path.dirname(os.path.realpath(__file__)).replace('\\','/')   + '/catasto.sqlite'
    ocon = spatialite_connect(dbName)
    ocur = ocon.cursor()

    ocur.execute('SELECT InitSpatialMetadata()')
    ocur.close()
    ocon.commit()
    schema = ''
    funzsql = "GeomFromText"


