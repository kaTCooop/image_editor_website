import os

from flask import Flask, url_for, render_template, request, redirect, flash, session, send_file
from flask_session import Session
from werkzeug.utils import secure_filename
from time import sleep
from PIL import Image, ImageOps
from datetime import timedelta


UPLOAD_FOLDER = '/root/projects/image_editor_site/static'
ALLOWED_EXTENSIONS = {'jpeg', 'png', 'jpg'}

if os.path.isdir(os.path.join(UPLOAD_FOLDER, 'images')) is False:
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'images'))

app = Flask(__name__)
app.secret_key = os.urandom(12)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours = 24)

app.config['SESSION_TYPE'] = 'redis'

Session(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download/<name>', methods = ['GET', 'POST'])
def download_file(name):

    path = UPLOAD_FOLDER + '/images/' + name
    i = Image.open(path)

    if 'changed' not in session:
        i = ImageOps.contain(i, (512, 512))
    
    else:
        i = ImageOps.contain(i, (256, 256))

    i.save(path)
    return render_template('download_image.html', name = name)

@app.route('/edit/<name>', methods=['GET', 'POST'])
@app.route('/edit/<name>/<cut>', methods=['GET', 'POST'])
def edit_image(name, cut = 'False'):
    path = UPLOAD_FOLDER + '/images/' + name
    i = Image.open(path)
    image = ImageOps.contain(i, (512, 512))
    format = i.format.lower()
    format_len = len(format) + 1

    print(session)
    for d in session:
        print(d)

    if 'changed' not in session:
        print('changed not in session')
        origin_name = name[:-format_len] + '_origin' + '.' + format
        origin_path = UPLOAD_FOLDER + '/images/' + name[:-format_len] + '_origin' + '.' + format
        
        if os.path.exists(origin_path):
            os.remove(origin_path)

        image.save(origin_path)
        session['origin_name'] = origin_name
        session['origin_path'] = origin_path
        session.modified = True

    print(format)

    if request.method == 'POST':

        if 'submit_button' in request.form:

            if 'greyed' not in session:
                session['changed'] = True
                session['greyed'] = True
                print(session)

                image.convert('L').save(path)
                session.modified = True
                return redirect(url_for('edit_image', name = name))
            
            else:
                print('greyed in !!!')
                return redirect(url_for('edit_image', name = name))

        elif 'cut_button' in request.form:
            return redirect(url_for('edit_image', name = name, cut = 'cut'))
        
        # cutting image by 2 points
        elif 'value1' and 'value2' in request.form:
            session['changed'] = True
            session.modified = True
            
            x, y = request.form['value1'].split(';')
            point_1 = x + ';' + y
            x, y = request.form['value2'].split(';')
            point_2 = x + ';' + y

            print(point_1 + ' ' + point_2)
    
            new_name = name[:-format_len+1] + '_cut' + '.' +  format
            new_path = UPLOAD_FOLDER + '/images/' + new_name
            last_point = float(point_1.split(';')[0]), float(point_1.split(';')[1])
            current_point = float(point_2.split(';')[0]), float(point_2.split(';')[1])

            if last_point[1] < current_point[1]:
                
                if last_point[0] < current_point[0]:
                    coordinates = (last_point[0], last_point[1], current_point[0], current_point[1])

                else:
                    coordinates = (current_point[0], last_point[1], last_point[0], current_point[1])
            
            else:

                if last_point[0] < current_point[0]:
                    coordinates = (last_point[0], current_point[1], current_point[0], last_point[1])

                else:
                    coordinates = (current_point[0], current_point[1], last_point[0], last_point[1])

            img2 = ImageOps.contain(image.crop(coordinates), (512, 512))

            try:
                img2.save(new_path)
            
            except ValueError:
                return '<body bgcolor=#000000 text=white>Empty image</body>'

            return render_template('download_image.html', name = new_name)

        elif 'back_button' in request.form:
            
            if 'changed' in session:
                
                if os.path.exists(path):
                    os.remove(path)

                origin_image = Image.open(session['origin_path'])
                origin_image.save(path)
                session.clear()
                session.modified = True
                return redirect(url_for('edit_image', name=name))

            else:
                return redirect(url_for('edit_image', name=name))
        
        elif 'flip_button' in request.form:
            session['changed'] = True
            session.modified = True
            
            img2 = image.rotate(180)
            img2.save(path)
            
            return redirect(url_for('edit_image', name=name))

        elif 'mirror_button' in request.form:
            session['changed'] = True
            session.modified = True
            
            img2 = ImageOps.mirror(image)
            img2.save(path)
            
            return redirect(url_for('edit_image', name=name))

        elif 'download_button' in request.form:
            session['changed'] = True
            session.modified = True

            return send_file(path, as_attachment = True, mimetype = 'image')

        elif 'download_cut_button' in request.form:
            new_name = name[:-format_len+1] + '_cut' + '.' +  format
            return send_file(UPLOAD_FOLDER + '/images/' + new_name, as_attachment = True, \
                    mimetype = 'image', download_name = name)

        else:
            return '''
            <body bgcolor=#000000 text=white>
            <p>Wrong button</p>
            </body>
            '''
    
    image.save(path)
   
   # display cutted image
    if cut == 'cut':
        print('rendered cut')
        
        return render_template('cut.html', name = name)
    
    # calculating height of our image
    img = Image.open(path)
    width, height = img.size

    return render_template('edit.html', name = name, height = height)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            session.clear()
            session.modified = True
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images' ,filename))
            return redirect(url_for('edit_image', name=filename))
    
    return '''
        <!doctype html>
        <body bgcolor=#000000 text=white>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
        </form>
        </body>
        '''

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    
    if request.method == 'POST':
        return redirect(url_for('get_files', password=request.form['password']))

    return render_template('admin_password.html')

@app.route('/admin_get_files/<password>', methods=['GET', 'POST'])
def get_files(password):

    with open('password.config', 'r') as f:
        local_password = f.readline()[:-1]
        print(local_password)
    
    if password != local_password:
        flash('Wrong password')
        sleep(3)
        return redirect(url_for('admin'))

    if request.method == 'POST':
        
        if 'user_input' not in request.form:
            flash('No text part')
            return redirect(request.url)

        data = request.form['user_input']
        print(data)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if data == '':
            flash('No text sent')
            return redirect(request.url)

        return redirect(url_for('edit_image', name=data))

    names = os.listdir(os.path.join(app.static_folder + '/images'))
    return render_template('list_of_images.html', names=names)

