from flask import Flask, render_template, request , abort , session 
from flask import send_from_directory
import os , shutil
from PyPDF2 import PdfFileReader, PdfFileWriter



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
app.secret_key = "some secret code"  


@app.route('/',methods=['GET','POST'])
def index():
    
    userID = session.get('userID',None)
    if userID==None:
        # supports single user at a time
        try:
            shutil.rmtree(app.config['UPLOAD_FOLDER'])
        except:
            pass            
        os.mkdir(app.config['UPLOAD_FOLDER'])
        
        # multi-user support
        userID = len(os.listdir(app.config['UPLOAD_FOLDER']))+1
        session['userID'] = userID
        os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))

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
    
    paths = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))
    kwargs['n'] = len(paths)
    kwargs['paths'] = paths
    return render_template('upload.html',kwargs = kwargs)


@app.route('/MnD')
def MnD():
    try:
        paths = [os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID']),p) for p in os.listdir(os.path.join(app.config['UPLOAD_FOLDER'],str(session['userID'])))]
        merge_pdfs(paths, output='merged.pdf')
        return send_from_directory('', filename='merged.pdf', as_attachment=True)
    except:
        abort(404)
        
if __name__=='__main__':
    app.run(debug=True)