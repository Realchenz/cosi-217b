"""Simple Web interface to spaCy entity recognition

To see the pages point your browser at http://127.0.0.1:5000.

"""


from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

import ner

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dependencies.db'
db = SQLAlchemy(app)

class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(100))
    dependency = db.Column(db.String(100))
    token = db.Column(db.String(100))

with app.app_context():
    db.create_all()

def add_dependencies(sent):
    for token in sent:
        dependency = Dependency(head=token.head.text, dependency=token.dep_, token=token.text)
        db.session.add(dependency)
    db.session.commit()

@app.get('/get')
def index_get():
    return render_template('form2.html', input=open('input.txt').read())

@app.post('/post')
def index_post():
    text = request.form['text']
    doc = ner.SpacyDocument(text)
    markup = doc.get_entities_with_markup()
    markup_paragraphed = ''
    for line in markup.split('\n'):
        if line.strip() == '':
            markup_paragraphed += '<p/>\n'
        else:
            markup_paragraphed += line

        text = request.form['text']
        doc = ner.SpacyDocument(text)
        
    # Get the dependency relationships for each sentence
    dependency_info = []
    for sent in doc.doc.sents:
        sent_text = sent.text
        sent_dependencies = [(token.head.text, token.dep_, token.text) for token in sent]
        add_dependencies(sent)
        dependency_info.append({'sentence': sent_text, 'dependencies': sent_dependencies})
    
    return render_template('result2.html', markup=markup_paragraphed, dependency_info=dependency_info)

@app.route('/')
def index():
    dependencies = Dependency.query.all()
    return render_template('result3.html', dependencies=dependencies)

if __name__ == '__main__':

    app.run(debug=True)
