from flask import Flask, render_template, request, redirect, url_for
from data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pkdex/<pkmn_type>')
def pkdex(pkmn_type):
    pkmn_list = read_pkmn_by_pkmn_type(pkmn_type)
    return render_template("pkdex.html", pkmn_type=pkmn_type, Pokemon=pkmn_list)

@app.route('/pkdex/<int:pkmn_id>')
def pkmn(pkmn_id):
    pkmn = read_pkmn_by_pkmn_id(pkmn_id)
    return render_template("pkmn.html", pkmn=pkmn)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processed', methods=['post'])
def processing():
    pkmn_data = {
        "pkmn_type": request.form['pkmn_type'],
        "name": request.form['pkmn_name'],
        "description": request.form['pkmn_desc'],
        "url": request.form['pkmn_url']
    }
    insert_pkmn(pkmn_data)
    return redirect(url_for('pkdex', pkmn_type=request.form['pkmn_type']))


@app.route('/modify', methods=['POST'])
def modify():
    if request.form["modify"] == "edit":
        pkmn_id = request.form["pkmn_id"]
        pkmn = read_pkmn_by_pkmn_id(pkmn_id)
        return render_template('update.html', pkmn=pkmn)
    elif request.form["modify"] == "delete":
        pkmn_id = request.form["pkmn_id"]
        pkmn = read_pkmn_by_pkmn_id(pkmn_id)
        delete_pkmn(pkmn_id)
        return redirect(url_for("pkdex", pkmn_type=pkmn["pkmn_type"]))

@app.route('/update', methods=['POST'])
def update():
    pkmn_data = {
        "pkmn_id" : request.form["pkmn_id"],
        "pkmn_type": request.form['pkmn_type'],
        "pkmn_name": request.form['pkmn_name'],
        "pkmn_description": request.form['pkmn_desc'],
        "pkmn_url": request.form['pkmn_url']
    }
    update_pkmn(pkmn_data)
    return redirect(url_for('pkmn', pkmn_id=request.form['pkmn_id']))

if __name__ == "__main__":
    app.run(debug=True)