from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os, sys
from flaskext.mysql import MySQL


# Open up terminal and type the following commands:
# $ mysql -u root -p
# mysql> CREATE DATABASE Data;
# mysql> USE Data;
# mysql> CREATE TABLE Songs(id INT NOT NULL AUTO_INCREMENT, name VARCHAR(100) NOT NULL, filepath VARCHAR(100) NOT NULL, PRIMARY KEY(id));
# WABBA LABBA DUB DUB BITCH



mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'emart22'
app.config['MYSQL_DATABASE_DB'] = 'Data'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Can also rename the uploaded file if you want
            #os.rename(UPLOAD_FOLDER + filename, UPLOAD_FOLDER+'niloofar.jpg')
            FILEPATH = UPLOAD_FOLDER + filename

            # Create db connection to upload new file
            db = mysql.connect()
            cursor = db.cursor()
            cursor.execute("INSERT INTO Songs (name, filepath) VALUES (%s,%s)", (filename, FILEPATH))
            db.commit()
            db.close()
            print ("\nSuccessfully added a file to the database (specified uploading folder).")
            print (" Name: " + filename)
            print (" Path: " + FILEPATH)

            # New db connection for printing all the records to the terminal
            dbx = mysql.connect()
            c = dbx.cursor()
            users = c.execute("SELECT * FROM Songs ORDER BY id ASC")
            users = c.fetchall()

            # Can also use Json Decoders for pretty printing, but i like it messy XD
            print ("\nPrinting all the records in the db - for debugging purpose")
            print (str(users))

    return render_template('upload.html')


@app.route('/')
def index():
      return '''
      <a href='upload'>Click to upload</a>
      '''

if __name__ == '__main__':
    app.run()
