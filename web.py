from flask import Flask
from flask import render_template, redirect, url_for
import pandas as pd
app = Flask(__name__)

#读数据

@app.route('/')
def index():
    return redirect(url_for('show_table', type='DMTX'))

@app.route('/<string:type>/', methods=['GET'])
def show_table(type):
    datas = []
    #判断类型读文件
    if type == 'DMTX':
        df = pd.read_csv('DMTX.csv', encoding='gbk')
        flag = 0
    elif type == "DXS":
        df = pd.read_csv('DXS.csv', encoding='gbk')
        flag = 1
    else:
        return '<font style="align:center;" size=36px color=red>505 请检查参数是否正确！！！</font>'
    #处理Nan
    df = df.fillna(0)
    for index, row in df.iterrows():
        datas.append(list(row))
    return render_template('show_table.html', datas=datas, flag=flag)



if __name__ == '__main__':
    app.run()