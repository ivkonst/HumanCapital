from classifier import Classifier
import time
from flask import Flask, render_template, request
import logging
from logging.handlers import RotatingFileHandler
import requests
# import re
from bs4 import BeautifulSoup
import codecs
import random
import pandas as pd
import numpy as np
# import time
# import math
# import csv



def get_pos_1(url):
    try:
        pos_1 = BeautifulSoup(url, 'lxml').findAll('h3', attrs={'class':'_1h3Zg ADNB4 _1BoTZ'})[0].text
    except:
        pos_1 = ''
    return pos_1
def get_len_pos_1(url):
    try:
        len_pos_1 = ' '.join(BeautifulSoup(url, 'lxml').findAll('div',
                                attrs={'class':'_1h3Zg _1LKcB _1xK5K _21a7u'})[1].span.text.split('\xa0'))
    except:
        len_pos_1 = ''
    return len_pos_1


def get_pos_2(url):
    try:
        pos_2 = BeautifulSoup(url, 'lxml').findAll('h3', attrs={'class':'_1h3Zg ADNB4 _1BoTZ'})[1].text
    except:
        pos_2 = ''
    return pos_2
def get_len_pos_2(url):
    try:
        len_pos_2 = ' '.join(BeautifulSoup(url, 'lxml').findAll('div',
                                attrs={'class':'_1h3Zg _1LKcB _1xK5K _21a7u'})[3].span.text.split('\xa0'))
    except:
        len_pos_2 = ''
    return len_pos_2


def get_pos_3(url):
    try:
        pos_3 = BeautifulSoup(url, 'lxml').findAll('h3', attrs={'class':'_1h3Zg ADNB4 _1BoTZ'})[2].text
    except:
        pos_3 = ''
    return pos_3
def get_len_pos_3(url):
    try:
        len_pos_3 = ' '.join(BeautifulSoup(url, 'lxml').findAll('div',
                                attrs={'class':'_1h3Zg _1LKcB _1xK5K _21a7u'})[5].span.text.split('\xa0'))
    except:
        len_pos_3 = ''
    return len_pos_3


def get_pos_4(url):
    try:
        pos_4 = BeautifulSoup(url, 'lxml').findAll('h3', attrs={'class':'_1h3Zg ADNB4 _1BoTZ'})[3].text
    except:
        pos_4 = ''
    return pos_4
def get_len_pos_4(url):
    try:
        len_pos_4 = ' '.join(BeautifulSoup(url, 'lxml').findAll('div',
                                attrs={'class':'_1h3Zg _1LKcB _1xK5K _21a7u'})[7].span.text.split('\xa0'))
    except:
        len_pos_4 = ''
    return len_pos_4


# def get_pos_5(url):
#     try:
#         pos_5 = BeautifulSoup(url, 'lxml').findAll('h3', attrs={'class':'_1h3Zg ADNB4 _1BoTZ'})[4].text
#     except:
#         pos_5 = ''
#     return pos_5
# def get_len_pos_5(url):
#     try:
#         len_pos_5 = ' '.join(BeautifulSoup(url, 'lxml').findAll('div',
#                                 attrs={'class':'_1h3Zg _1LKcB _1xK5K _21a7u'})[9].span.text.split('\xa0'))
#     except:
#         len_pos_5 = ''
#     return len_pos_5


# Создаём  экземпляр flask-a
app = Flask(__name__)
# app.url_map.strict_slashes = False
# Создаём эксземпляр нашей модели
classifier = Classifier()


# Парсинг формы
def parse_form(form):

    # return {
    #     'proffesions': form.get('prof', ''),
    #     'pos_1': get_pos_1(form.get('f')), 'len_pos_1': get_len_pos_1(form.get('f')),
    #     'pos_2': get_pos_2(form.get('f')), 'len_pos_2': get_len_pos_2(form.get('f')),
    #     'pos_3': get_pos_3(form.get('f')), 'len_pos_3': get_len_pos_3(form.get('f')),
    #     'pos_4': get_pos_4(form.get('f')), 'len_pos_4': get_len_pos_4(form.get('f'))
    #     # 'experience': float(form.get('exp', 0.) or 0),
    #     # 'is_first_category': form.get('fst_cat') == 'true',
    #     # 'is_phd':  form.get('phd') == 'true',
    # }
    print(form.get('f'))
    f1 = codecs.open(form.get('f'), 'r').read()
    return [form.get('prof'),
            get_pos_1(f1), get_len_pos_1(f1),
            get_pos_2(f1), get_len_pos_2(f1),
            get_pos_3(f1), get_len_pos_3(f1),
            get_pos_4(f1), get_len_pos_4(f1) ]


# Основная функция, от flask-a нужен декоратор
@app.route("/price", methods=["POST", "GET"])
def index_page(text="", prediction_message=""):
    # GET запрос - просто получение кода страницы - возвращем то, что есть
    if request.method == "GET":
        return render_template('hello.html')

    # POST запрос - получение кода страницы, но с учётом дополнительных посылаемых данных
    if request.method == "POST":
        # Извлекаем данные и парсим
        app.logger.info('POST request, start to parse data')
        obj = parse_form(request.form)
        app.logger.info('Data is parsed, the result is')
        app.logger.info(obj)
        # Делаем предсказание
        prediction = classifier.predict(obj)
        # app.logger.info('The prediction is {}'.format(prediction))
        # Возвращаем страницу с правильно заполненными значениями
        return render_template(
            'hello.html', 
            # is_phd='checked' if obj['is_phd'] else '',
            # is_first_category='checked' if obj['is_first_category'] else '',
            # proffesions=' '.join(obj['proffesions']),
            # experience=str(obj['experience']),
            prediction=prediction
        )


if __name__ == "__main__":
    # Правильный способ логгировать данные - библиотека logging
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('demo.log', maxBytes=10000, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(host='::', port=5000, debug=True)
