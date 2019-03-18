# coding:utf-8
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from app.exam_user_train import exam_user_train

@app.route('/colloct', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        exa = exam_user_train()
        exa.listener()
        #print(111111)
    return render_template('colloct.html',
        title='Detect Data',
        form = form)
@app.route('/colloct1', methods = ['GET', 'POST'])
def login1():
    form = LoginForm()

    if form.validate_on_submit():
        exa=exam_user_train()
        exa.listener()
        #print(1111111)
    return render_template('colloct1.html',
        title='Detect Data',
        form = form)