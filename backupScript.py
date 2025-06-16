import os
import sys
import docker
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


##################################
#       Metodi e funzioni        #
##################################

def checkOneDrive():
    username = os.getenv('USERNAME')
    onedrivePath = f"C:\\Users\\{username}\\OneDrive"
    if os.path.exists(onedrivePath):
        print("cartella onedrive trovata")
        return onedrivePath
    else:
        print("cartella onedrive NON trovata")
        exit(1)
    

#ricerca la cartella di backup in OneDrive, se non esiste la crea
def checkBackupFolder():
    backupPath = Path(onedrivePath) / "Backup"
    if not backupPath.exists():
        print("Creazione cartella di backup...")
        backupPath.mkdir(parents=True, exist_ok=True)
        print("Cartella di backup creata.")
        
    else:
        print("Cartella backup trovata.")
        
    return backupPath

# Esegue il backup del database MySQL in un file .sql

def backupMysql():

    backupPath = checkBackupFolder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backupFile = backupPath / f"backup_{timestamp}.sql"

    db_container_name = os.getenv('DB_CONTAINER_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    try:
        print("Eseguendo il backup del database...")
        subprocess.run([
            "docker", "exec", db_container_name,
            "mysqldump", "-u", db_user,
            f"-p{db_password}", db_name
        ], stdout=open(backupFile, 'w'), check=True)
        print(f"Backup completato: {backupFile}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il backup: {e}")
        sys.exit(1)
    
# Esegue il backup del volume Docker in un file .tar.gz
def backupDockerVolume():
    backupPath = checkBackupFolder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backupFile =f"volume_{timestamp}.tar.gz"

    db_container_name = os.getenv('DB_CONTAINER_NAME')
    db_volume_name = os.getenv('IMAGES_VOLUME_NAME')
    print(f"Nome volume: {db_volume_name}")
    print(f"nome container: {db_container_name}")
    try:
        print("Eseguente il backup delle foto...")
        subprocess.run([
            "docker", "run" ,"--rm" ,"-v",
            f"{db_volume_name}:/data","-v",
            f"{backupPath}:/Backup" , "ubuntu","bash","-c",
            f"cd /data && tar czf /Backup/{backupFile} ."
        ])
        print(f"Backup completato: {backupFile}")
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il backup: {e}")
        sys.exit
        
        
##################################
#      Caricamento variabili     #
##################################
load_dotenv()

requiredVars = [
    "DB_CONTAINER_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "USERNAME",
    "IMAGES_VOLUME_NAME"
]

missingVars=[var for var in requiredVars if not os.getenv(var)]

if missingVars:
    print(f"ERRORE: Variabili mancanti nel .env: {', '.join(missingVars)}")
    exit(1)

print (" variabili d'ambiente caricate correttamente")


#####################################
#       Controllo directory         #
#####################################

onedrivePath = checkOneDrive()

#####################################
#            START BACKUP           #
#####################################

backupMysql()
backupDockerVolume()