TECH  
  
On server: nginx as web-server, gunicorn as wsgi, redis as session-storage, web-application on flask  
  
SET UP  
  
1. Run setup.py or install required modules manually  
2. Install redis if you didn't run setup.py  
  
CONFIGURATION  
  
In order for this web app to work:  
1. Change password for your admin panel in password.config.example file then rename it to password.config  
2. Run 'sudo service redis-server start' before starting the app  
3. Optional: configure nginx and gunicorn to work with application  
  
START  
  
1. Run gunicorn like this : 'gunicorn -w 4 main:app' or 'gunicorn -c /etc/gunicorn/config.py main:app' with config file   
2. Or run flask-wsgi 'python3 start.py'  

