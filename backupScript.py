import os
import sys
import docker
import subprocess
import logging
import configparser
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

##################################
#      Caricamento variabili     #
##################################

config = configparser.ConfigParser()
config.read('backup.config.ini')
db_container_name = config['mysql.docker.env']['db_container_name']
db_user = config['mysql.docker.env']['db_user']
db_password = config['mysql.docker.env']['db_password']
db_name = config['mysql.docker.env']['db_name']
db_volume_name = config['image.docker.env']['images_volume_name']
onedrivePath = config['windows.general.env']['save_dir_path']

configarr = [
    ('db_container_name', db_container_name),
    ('db_user', db_user),
    ('db_password', db_password),
    ('db_name', db_name),
    ('db_volume_name', db_volume_name),
    ('onedrivePath', onedrivePath)
]

for key, value in configarr:
    if not value:
        print(f"Errore: la variabile '{key}' non è stata definita nel file di configurazione.")
        sys.exit(1)

##################################
#       Metodi e funzioni        #
##################################


#ricerca la cartella di backup nella cartella di destinazione, se non esiste la crea
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
        
        


#####################################
#            START BACKUP           #
#####################################

backupMysql()
backupDockerVolume()
