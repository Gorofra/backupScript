<h1>First Version</h1>
<p>The first version allows direct modification of the backup.config.ini file, with the required information to easily perform backup to a folder of choice.<br> 


<h1>Docker backup Script</h1>
<i>English version below</i><br><br>
Questo script può essere utilizzato in caso si abbia bisogno di fare un Backup di un app che sfrutta un container Docker mysql e un volume Docker per salvare altri tipi di dati, ad esempio immagini, Direttamente su Onedrive o la cartella che preferisci;<br><br>
Utilizza il metodo MYSQLDUMP per il database sql e i comandi docker direttamente da terminale per il volume.<br><br>
Ti bastera seguire passo passo i seguenti punti , assicurati di inserire correttamente le variabili del tuo docker/mysql all'interno di .env<br><br>
Utilizzando Task Manager ( Utilità di pianificazione ) potrai automatizzare il tuo backup che verra salvato direttamente nella Cartella Onedrive del dispositivo, 
rendendoti sicuro di non perdere quei dati e con un costo nullo visto che il piano gratuito è piu che sufficente per piccole app. <br><br>

Passo (1) creare l'ambiente e clonare la repository:<br>
Crea un ambiente python con VirtualEnv CHIAMATA "env"<br>
Installa pip<br>
Clona la repository e installa i requirements.txt:<br>
pip install -r requirements.txt <br>
Usa backup.config.ini.example come base per il tuo backup.config.ini che dovra trovarsi nella stessa cartella del file .exe <br>
Inserisci i dati del docker e del tuo database<br><br>

Passo (2) creare un eseguibile con PYinstaller ( se il tuo antivirus da problemi togli l'opzione --onefile ):<br>
Comando creazione .exe con env:<br>pyinstaller --onefile --icon=icona.ico --name backup_manager backupScript.py<br><br>

Passo (3) impostare ricorrenza con taskManager(windows):<br>
all'avvio dell'app con task manger di windows assicurati che nella tabella azioni quando aggiungi " Avvio programma "
assicurati di inserire la cartella in cui è stata generata e si trova l'exe sotto l'opzione " Start " o " Inizia ".<br>
Programma o script:<br>
C:\path\to\backupScript\dist\backup_manager.exe<br>
Aggiungi argomenti (facoltativo):<br>
Lasciare vuoto<br>
Inizio (facoltativo):<br>
C:\path\to\backupScript\dist\


<br><br><br><br>
<h1>Docker backup Script eng</h1> This script can be used when you need to make a backup of an app that uses a Docker mysql container and a Docker volume to save other types of data, for example images, directly on OneDrive or in the folder of your choice;<br><br>
It uses the MYSQLDUMP method for the sql database and docker commands directly in terminal for the volume.<br><br> 
You just need to follow step by step the following points, make sure to correctly insert the variables of your docker/mysql inside .env<br><br>
Using Task Manager (Task Scheduler) you will be able to automate your backup that will be saved directly in the Onedrive folder of the device,
making you safe from losing that data and at zero cost since the free plan is more than sufficient for small apps. <br><br>

Step (1) create the environment and clone the repository:<br>
Create a python environment with VirtualEnv CALLED "env"<br>
Install pip<br>
Clone the repository and install the requirements.txt<br>
pip install -r requirements.txt <br>
Use backup.config.ini.example as a base for your backup.config.ini, which must be located in the same folder as the .exe file.<br>
Insert the data of docker and your database<br><br>

Step (2) create an executable with PYinstaller (if your antivirus gives problems remove the --onefile option):<br>
Command to create .exe with env:<br>
pyinstaller --onefile --icon=icona.ico --name backup_manager backupScript.py<br><br>
add backup.config.ini and log.txt in the same folder as the .exe file.

Step (3) set recurrence with taskManager(windows):<br>
at app startup with windows task manager make sure that in the actions table when you add "Start program"
make sure to insert the folder where the exe was generated and is located under the "Start" or "Begin" option.<br>
Program or script:<br>
C:\path\to\backupScript\dist\backup_manager.exe<br>
Add arguments (optional):<br>
Leave empty<br>
Start (optional):<br>
C:\path\to\backupScript\dist\
