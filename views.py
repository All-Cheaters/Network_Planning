"""
Routes and views for the flask application.
"""
from FlaskWeb.DBconfig import *
from FlaskWeb.ItemForm import ProjectForm, MainForm



@app.route('/')
@app.route('/new/')
def new():
    form_one = ProjectForm()
    return render_template(
        'new.html',
        title='new',
        form_one = form_one
    )

@app.route('/view/')
def view():
    return render_template(
        'view.html',
        title='view'
    )

@app.route('/change/')
def change():
    form_one = ProjectForm()
    return render_template(
        'change.html',
        title='change',
        form_one = form_one
    )

@app.route('/graph/')
def graph():
    return render_template(
        'graph.html',
        title='graph'
    )


#from FlaskWeb.DBconfig import *
#from FlaskWeb.ItemForm import ProjectForm, MainForm

#@app.route('/', methods=['GET', 'POST'])
#def submit_item():
#    form_one = ProjectForm()
#    form_two = MainForm()
    
#    return render_template('change.html', form_one = form_one, form_two = form_two)
