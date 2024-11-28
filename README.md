TECH  
  
On server: nginx as web-server, gunicorn as wsgi, redis as session-storage, web-application on flask  
  
CONFIGURATION  
  
In order for this web app to work:  
1. Change password for your admin panel in password.config.example file then rename it to password.config  
2. Run 'sudo service redis-server start' before starting the app  
3. Optional: configure nginx and gunicorn to work with application  

