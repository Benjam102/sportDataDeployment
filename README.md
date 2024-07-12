# Application configuration for deployment

This file explains how to configure the project for deployment on a server. I will deal with a small part of the configuration of the proxy reverse NGINX used. However, for an in-depth description of how the server works, please refer to the documentation made on the configuration of the server available on the github of the lab and made by another French student.

# Table of Contents
1. [Configuration of our application ](#configuration-of-our-application)
     - [File setting located in the folder sportsDataForNerds](#file-setting-located-in-the-folder-sportsdatafornerds)
     - [Domain name in the admin of the website](#domain-name-in-the-admin-of-the-website)
2. [Configuration on the server](#configuration-on-the-server)
     - [Connection to the server](#connection-to-the-server)
     - [Go to our project](#go-to-our-project)
     - [Updated the project](#updated-the-project)
     - [Explanation of the script](#explanation-of-the-script)
         - [Deleting the old version of the project](#deleting-the-old-version-of-the-project)
         - [Importation of the new version](#importation-of-the-new-version)
         - [Restart our application on the port 8002](#restart-our-application-on-the-port-8002)
    - [Configuration of our domain in NGINX](#configuration-of-our-domain-in-nginx)
       
## Configuration of our application 

We're just going to modify one file to put the project into production and modify the domain name indicates in the database.

### File setting located in the folder sportsDataForNerds

Uncomment all the following lines and delete the one just above them if they are duplicated :
- Path access to the file .env: we have removed the database from the main folder to separate the website part and the database with the scraping routines. So, we can work independently on both parts.
```python
load_dotenv(os.path.join(BASE_DIR, '../', '.env')) 
```
- DEBUG: it allows you to no longer displays site errors directly online
```python
DEBUG = False
```
- ALLOWED_HOSTS: it allows you to specify the domain names authorised to access the application. Here, we have only authorized access for the project's subdomain and not the entire domain.
```python
ALLOWED_HOSTS = [os.environ.get('DOMAIN_NAME_1'), os.environ.get('DOMAIN_NAME_2')]
```
- DATABASES: we moved the database to another folder, so we need to modify the path to access the database.
```python
'NAME': os.path.join(BASE_DIR, '../database', 'db.sqlite3'),
```
- CSRF: it allows to accepts CSRF requests only from the entire domain tcdrail.com.
```python
CSRF_TRUSTED_ORIGINS = [
     'https://*.tcdrail.com/'
]
```
- CSRF: it allows us to ensure that CSRF cookies are only sent via HTTPS.
```python
CSRF_COOKIE_SECURE = True
```
- CSRF: it allows us to ensure that session cookies are only sent via HTTPS.
```python
SESSION_COOKIE_SECURE = True
```
### Domain name in the admin of the website

It is important to indicate the domain name of the site that will serve the various requests. The default is http://example.com/ or something else. It is therefore necessary to connect to the website admin in order to change this domain name to our own. To do this, refer to the google drive. 

Once connected, go the section site and click on 'site'. Then click on the domain which is not ours and change it by https://sportdatafornerds.tcdrail.com.

## Configuration on the server

Here, we are going to see what we need to do on the server. At the end, we will see the configuration of the reverse proxy NGINX made by another french student.

### Connection to the server

```sh
ssh root@tcdrail.com
```
```sh
ssh root@194.164.22.54
```
For the password, go to [ionos.co.uk](https://www.ionos.co.uk/), section 'Servers & Cloud'. Click on 'My VPS' and you will see the password.

### Go to our project

When you arrive on the server, launch the virtual environment of the project :
```sh
pyenv activate sportData
```
Then go to the folder of the project :
```sh
cd websites/sportsDataForNerds/
```
sportsDataForNerds/  
├── .env  
├── database/  
├── sportDataDeployment/  

where :
- `.env` : Fichier de configuration pour les variables d'environnement.
- `database/` : Dossier de la base de données et des routines de scraping.
- `sportDataDeployment/` : Dossier contenant le projet.

### Updated the project

If you have not made any changes to the database, you can run the following script :
```sh
./update_code.sh
```

If you have made any changes to the database, you will need to uncomment these two lines :
```sh
rm -r ../database/db.sqlite3
mv db.sqlite3 ../database
```

** However, it is important to make a backup of the server database before running the bash script with these uncommented instructions. **

### Explanation of the script 

Here, we are going to explain the different commands of the script.

#### Deleting the old version of the project

Our application listens on TCP port 8002. So, we need to stop the application listening on TCP port 8002 by the following command :
```sh
sudo fuser -k 8002/tcp
```
Then delete the project folders containing the project files and the static files that will be served by nginx.
```sh
rm -r sportDataDeployment
rm -r /www/data/sportDataDeployment/staticfiles/
```
If you have modified the database, you need to delete it after making a backup.
```sh
rm -r ../database/db.sqlite3
mv db.sqlite3 ../database
```

#### Importation of the new version

Git clone from the gitlab of the lab :
```sh
git clone ...
```
Collect the static files :
```sh
python manage.py collectstatic
```
 They will be located in the path indicated in STATIC_ROOT in the project's setting.py file. that is on the folder located in /www/data/sportDataDeployment/staticfiles/. 

#### Restart our application on the port 8002

Get into the project file and start the uvicorn web server so that our application listens on port 8002 :
```sh
cd sportDataDeployment
nohup uvicorn sportsDataForNerds.asgi:application --host localhost --port 8002 &
```
A nohup.out file will be created, which will be our log file.

### Configuration of our domain in NGINX
In the file tcdrail.com located in /etc/nginx/sites-available, we have for our subdomain :
```sh
server {
    server_name www.sportdatafornerds.tcdrail.com sportdatafornerds.tcdrail.com;

    # Redirection of requests for the domain name specified above to localhost:8002, where the web application runs
    location / {
        proxy_pass http://localhost:8002;
        include /etc/nginx/proxy_common.conf;
    }

    # Configuration so that Nginx can serve our static files from /www/data/sportDataDeployment/staticfiles and 404 error handling.
    location /static {
        alias /www/data/sportDataDeployment/staticfiles;
        autoindex on;
        try_files $uri $uri/ =404;
    }

    listen 443 ssl;
}
```
For more details, please refer to the server documentation available on the laboratory's github.
