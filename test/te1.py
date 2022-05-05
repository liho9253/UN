# -*- coding: UTF-8 -*-
# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import pandas

app = Flask(__name__)
pandas.set_option('max_colwidth',100)
pandas.set_option('display.max_columns', None)
pandas.set_option('display.max_row', None)

df = pandas.read_csv('test16.csv')
df.replace("\r\n",'<br>', inplace=True,regex = True)

data = df.to_dict(orient = 'records')


print(data[0])




def get_page(offset=0, per_page=10):
    return data[offset: offset + per_page]


@app.route('/')
def index():

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(data)
    pagination_users = get_page(offset=offset, per_page=per_page)
    
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            total=total,
                            css_framework='bootstrap4')
    return render_template('main2.html',
                           data=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)
if __name__ == "__main__":
    """
        export FLASK_APP=fet_main.py
        export FLASK_ENV=fet_develop
        flask run
    """
    app.run(host="localhost", port=5001, debug=True)