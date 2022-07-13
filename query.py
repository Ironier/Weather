# -*- coding: utf-8 -*-
from time import time
from flask import Flask, request, render_template
from spider import parse_urlpage, realtime_data
from gevent import pywsgi

dict_return = {'data':[]}
locs = ['武汉','孝感','黄冈','十堰','襄阳','神农架','随州','恩施','宜昌','荆门','荆州','潜江','天门','仙桃','鄂州','咸宁','黄石']

dict_return['locs'] = locs
for i in locs:
    data = parse_urlpage(i)
    dict_return['data'].append(data) #所有城市数据

global cur_city_data,cur_city
cur_city_data  = realtime_data(locs[0]) #焦点城市数据
cur_city = 0

def isDigit(x):
    return '0'<=x and x<='9'

app = Flask(__name__)
@app.route('/query/', methods=['GET', 'POST'])
def query():
    global cur_city_data,cur_city

    if request.method == 'POST':    #接收到前端发来的消息
        code = request.form.get('name')
        elements = code.split('/')
        time_bound = []
        target = []
        for element in elements:
            if(isDigit(element[0])):
                time_bound.append(element) #时间
            if(element in locs):
                target.append(element) #目的地
        if(len(target)>=2):
            cur_data = {'data':[],'locs':[]}
            for i in range(len(dict_return['locs'])):
                city = dict_return['locs'][i]
                if(city in target):
                    cur_data['locs'].append(city)
                    cur_data['data'].append(dict_return['data'][i])
            cur_city_data = realtime_data(target[0])
            cur_city = 0
        else:
            if(len(target)==1):
                cur_city_data = realtime_data(element)
                cur_city = locs.index(element)
            cur_data = dict_return

        for i in range(len(cur_data['data'])):
            if(len(time_bound)==1):     #只输入了一个时间,则作为时间上限
                idx2 = cur_data['data'][i]['data_7d']['TIME'].index(time_bound[0])
                cur_data['data'][i]['data_7d']['TIME'] = cur_data['data'][i]['data_7d']['TIME'][0:idx2+1]
                cur_data['data'][i]['data_7d']['CELSIUS'] = cur_data['data'][i]['data_7d']['CELSIUS'][0:idx2+1]
                cur_data['data'][i]['data_7d']['WEATHER'] = cur_data['data'][i]['data_7d']['WEATHER'][0:idx2+1]
                cur_data['data'][i]['data_7d']['WIND'] = cur_data['data'][i]['data_7d']['WIND'][0:idx2+1]
                cur_data['data'][i]['data_7d']['WIND_LEVEL'] = cur_data['data'][i]['data_7d']['WIND_LEVEL'][0:idx2+1]
            elif len(time_bound)>=2:    #只输入两个以上时间,取前两个作为下限和上限
                idx = cur_data['data'][i]['data_7d']['TIME'].index(time_bound[0])
                idx2 = cur_data['data'][i]['data_7d']['TIME'].index(time_bound[1])
                cur_data['data'][i]['data_7d']['TIME'] = cur_data['data'][i]['data_7d']['TIME'][idx:idx2+1]
                cur_data['data'][i]['data_7d']['CELSIUS'] = cur_data['data'][i]['data_7d']['CELSIUS'][idx:idx2+1]
                cur_data['data'][i]['data_7d']['WEATHER'] = cur_data['data'][i]['data_7d']['WEATHER'][idx:idx2+1]
                cur_data['data'][i]['data_7d']['WIND'] = cur_data['data'][i]['data_7d']['WIND'][idx:idx2+1]
                cur_data['data'][i]['data_7d']['WIND_LEVEL'] = cur_data['data'][i]['data_7d']['WIND_LEVEL'][idx:idx2+1]
    else:
        cur_data = dict_return
    return render_template('query.html', dict_return = cur_data, cur_city_data=cur_city_data, cur_city = cur_city)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()