import os
import sys
import docker
import subprocess
import configparser
import pathlib
from datetime import datetime
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
volume_name = config['image.docker.env']['volume_name']
save_dir_path = config['windows.general.env']['save_dir_path']
save_dir = config['windows.general.env']['save_dir']

dateNow = datetime.now().strftime("%Y%m%d_%H%M%S")
timestampLog = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

deleteOlderThan = 604800  # seconds
timestamp = datetime.timestamp(datetime.now())
pathcompleto = save_dir_path + f"{save_dir}\\"
gruppoBackup = []

configArr = [
    ('db_container_name', db_container_name),
    ('db_user', db_user),
    ('db_password', db_password),
    ('db_name', db_name),
    ('volume_name', volume_name),
    ('save_dir_path', save_dir_path)
]



##################################
#       Metodi e funzioni        #
##################################


# Funzione per aprire file
def opener(path, flags):
    return os.open(path, flags, )

# Controllo se tutte le variabili sono state definite
def checkVariables(configArr):
    for key, value in configArr:
        if not value:
            with open('log.txt', 'a', opener=opener) as f:
                print(f'Errore durante la fase di [VARIABILE MANCANTE] {key} {timestampLog}', file=f)
            print(f"Errore: la variabile '{key}' non è stata definita nel file di configurazione.")
            sys.exit(1)

#ricerca la cartella di backup nella cartella di destinazione, se non esiste la crea
def checkBackupFolder():
    backupPath = pathlib.Path(save_dir_path) / f"{save_dir}"
    if not backupPath.exists():
        print("Creazione cartella di backup...")
        backupPath.mkdir(parents=True, exist_ok=True)
        print("Cartella di backup creata.")
    else:
        print(f"Cartella backup trovata. {backupPath}")
    return backupPath

# Esegue il backup del database MySQL in un file .sql
def backupDockerMysql():

    backupPath = checkBackupFolder()
    backupFile = backupPath / f"backup_{dateNow}.sql"

    try:
        print("Eseguendo il backup del database...")
        subprocess.run([
            "docker", "exec", db_container_name,
            "mysqldump", "-u", db_user,
            f"-p{db_password}", db_name
        ], stdout=open(backupFile, 'w'), check=True)
        print(f"Backup completato: {backupFile}")
    except subprocess.CalledProcessError as e:
        with open('log.txt', 'a', opener=opener) as f:
            print(f'Errore durante la fase di [BACKUP DATABASE MYSQL] {timestampLog}', file=f)
        print(f"Errore durante il backup: {e}")
        sys.exit(1)

# Esegue il backup del volume Docker in un file .tar.gz
def backupDockerVolume():
    backupPath = checkBackupFolder()
    backupFile =f"volume_{dateNow}.tar.gz"
    
    print(f"Nome volume: {volume_name}")
    print(f"nome container: {db_container_name}")
    try:
        print("Eseguente il backup delle foto...")
        subprocess.run([
            "docker", "run" ,"--rm" ,"-v",
            f"{volume_name}:/data","-v",
            f"{backupPath}:/{save_dir}" , "ubuntu","bash","-c",
            f"cd /data && tar czf /{save_dir}/{backupFile} ."
        ])
        print(f"Backup completato: {backupFile}")
    except subprocess.CalledProcessError as e:
        with open('log.txt', 'a', opener=opener) as f:
            print(f'Errore durante la fase di [BACKUP VOLUME] {timestampLog}', file=f)
        print(f"Errore durante il backup: {e}")
        sys.exit

#funzione per raccogliere i file di backup esistenti in un array
def backupGroup():
    for path in pathlib.Path(pathcompleto).glob("*.tar.gz"):
        try:
            gruppoBackup.append(pathcompleto + path.name)
        except OSError as e:
            sys.exit(1)
        
    for path in pathlib.Path(pathcompleto).glob("*.sql"):
        try:
            gruppoBackup.append(pathcompleto + path.name)
        except OSError as e:
            sys.exit(1)

#funzione per eliminare i file di backup più vecchi di 10 giorni
def reciclyngBackup():
    for path in gruppoBackup:
        file_stat = pathlib.Path(path).stat()
        file_ctime = file_stat.st_ctime
        print(f"Controllo file: {path}, creato il: {(file_ctime)}")
        if( timestamp - file_ctime > deleteOlderThan):
            
            with open('log.txt', 'a', opener=opener) as f:
                print(f"Il file {path} è più vecchio di {deleteOlderThan/86000} giorni e verrà eliminato.")
            try:
                os.remove(path)
            except OSError as e:
                print(f"Errore durante l'eliminazione del file {path}: {e}")
                sys.exit(1)
        else:
            print(f"Il file {path} è stato creato il: {(file_ctime)} e non verrà eliminato.")


def backupCompleted():
    with open('log.txt', 'a', opener=opener) as f:
        print(f'[BACKUP COMPLETATO] {timestampLog}', file=f)

#####################################
#            START BACKUP           #
#####################################

checkVariables(configArr)

backupDockerMysql()
backupDockerVolume()

backupGroup()
reciclyngBackup()

backupCompleted()
print("Backup completato con successo.")