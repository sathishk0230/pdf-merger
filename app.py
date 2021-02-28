from flask import Flask, render_template, request , abort , session , redirect , url_for
from flask import send_from_directory
import os , shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
import json


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = os.environ.get('SECRET_KEY','ts)369t=l^xxb&o0-w@q8z$ri#=8w_)1c(hkm*dt2ri0ch(u07')
if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])


@app.route('/',methods=['GET','POST'])
def index():
    walk = list(os.walk(app.config['UPLOAD_FOLDER']))
    print(walk)
    if len(walk)>5:
        shutil.rmtree(app.config['UPLOAD_FOLDER'])
    else:
        for path in walk:
            try:
                if 'done' in path[2]:
                    shutil.rmtree(path[0])
            except:
                break

    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    # delete completed users data
    
    userID = session.get('userID',None)
    if userID==None:
        userID = len(os.listdir(app.config['UPLOAD_FOLDER']))+1
        session['userID'] = userID
        try:
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))
        except:
            pass

    kwargs = dict()
    if request.method=='GET':
        pass
    elif request.method=='POST':
        try:
            f = request.files['myfile'] 
            path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                str(session['userID']),
                f.filename)
            f.save(path)
        except FileNotFoundError:
            abort(400)
    try:
        paths = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))
        # user completed download
        if paths==None:
            return redirect(url_for('bye'))
        kwargs['n'] = len(paths)
        kwargs['paths'] = paths
    except:
        return redirect(url_for('bye'))

    return render_template('upload.html',kwargs = kwargs)

@app.route('/bye')
def bye():
    session['userID']=None
    return render_template('bye.html',kwargs={})


@app.route('/MnD')
def MnD():
    try:
        paths = [os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID']),p) for p in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))]
        merge_pdfs(paths, output='merged.pdf')
        with open(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID']),'done'),'w') as file:
            pass
        return send_from_directory('', filename='merged.pdf', as_attachment=True)
    except:
        abort(404)



@app.route('/billlookup/')
def billlookup():
    data = {
        'key1':"1",
        'key':"20"
    }
    # if request.method=="POST":
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/billpayment/')
def billlookup():
    data = {
        'key1':"1",
        'key2':"20"
    }
    # if request.method=="POST":
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__=='__main__':
    app.run(debug=bool(os.environ.get('DEBUG',False)))