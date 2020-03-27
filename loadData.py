import json
import requests
import pandas as pd
from flask import Flask,request,make_response,Response
from flask import jsonify, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
result = {}
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



def confirmed(values):
    deaths =0 
    recovered = 0
    confirmed = values[-1]['confirmed']
    date = values[-1]['date']
    deaths = values[-1]['deaths']
    recovered = values[-2]['recovered']
    velocity = len(values) - values.index(next(filter(lambda i: i['confirmed'] > 0 and i['confirmed'] != None, values)))

    # for value in values:
    #     if value['deaths'] != None:
    #         deaths+= value['deaths']
    #     if value['recovered'] != None:
    #         recovered+= value['recovered']

    return (date,confirmed,deaths,recovered, velocity )

# def confirmed(values):
#     return values[-1]


def fetchData():
    r = requests.get('https://pomber.github.io/covid19/timeseries.json')
    data = json.loads(r.text)
    print(data['India'])
    
    my_dictionary = dict(map(lambda kv: (kv[0], list(confirmed(kv[1]))) , data.items()))

    df = pd.DataFrame(list(my_dictionary.values()))
    df.columns= ['date','confirmed','deaths','recovered','velocity']
    df.index = (list(my_dictionary.keys()))
    df['recovered'].fillna(value = 0, inplace= True)
    print(df.describe())
    print(df.head())
    print(df.loc['India'].values)
    print(df.loc['China'].values)
    print(df['recovered'].max())
    return df

@app.route('/head',methods = ['GET'])
@cross_origin()
def send_dataframe():
    df = fetchData()
    return (df.head(5).to_html())

@app.route('/dataframe', methods = ['POST'])
@cross_origin()
def sendDataframe():
    req= request.form['number']
    
    df = fetchData()

    return (df.head(int(req)).to_html())

@app.route('/sendByCountry', methods = ['POST'])
@cross_origin()
def sendByCountry():
    req= request.form['country']
    
    df = fetchData()

    return (df.loc[req].to_frame().to_html())
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)