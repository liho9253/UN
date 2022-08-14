
from flask import Flask, render_template, request, session
from flask_paginate import Pagination, get_page_args
import os, sys
app = Flask(__name__)


@app.route('/')
def index():
    
    return render_template('try.html')

@app.route('/update',methods=['GET','POST'])
def update():
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5002, debug=True)