import os
import sys
import docker
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv



 # subprocess.run(["docker","exec","--help"])

##################################
#      Caricamento variabili     #
##################################

load_dotenv()

required_vars = [
    "DB_CONTAINER_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "USERNAME"
]

missing_vars=[var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"ERRORE: Variabili mancanti nel .env: {', '.join(missing_vars)}")
    exit(1)

print (" variabili d'ambiente caricate correttamente")


#####################################
# Creazione cartella se inesistente #
#####################################

