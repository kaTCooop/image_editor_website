import os

os.system('sudo apt-get install -y redis-server')
os.system('sudo service redis-server start')

modules = ['Flask', 'Pillow', 'flask-session[redis]', 'Flask-Cors']

for module in modules:
    if module == 'Flask':
        os.system('pip install --force-reinstall -v ' + module + '==2.3.3')


    os.system('pip install ' + module)

