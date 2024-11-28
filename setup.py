import os

os.system('sudo apt-get install -y redis-server')

modules = ['Flask', 'Pillow', 'flask-session[redis]']

for module in modules:
    if module == 'Flask':
        os.system('pip install --force-reinstall -v ' + module + '==2.3.3')
        continue


    os.system('pip install ' + module)

