# -*- coding: UTF-8 -*-
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import pandas

app = Flask(__name__)

df = pandas.read_csv('test16.csv')
data = df.to_dict(orient = 'records')


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
    return render_template('main.html',
                           data=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)