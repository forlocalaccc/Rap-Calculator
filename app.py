from flask import Flask,request, jsonify, render_template
import csv
import pandas as pd

app = Flask(__name__)

def get_unique_values(file,col):
    df = pd.read_csv(file)
    unique_values = df[col].unique()
    return unique_values

@app.route('/')
def index():
    certi_values = get_unique_values('BACK.csv','CERTI')
    shape_values = get_unique_values('RAP.csv','SHAPE')
    color_values = get_unique_values('RAP.csv','COLOR')
    clarity_values = get_unique_values('RAP.csv','CLARITY')
    cut_values = get_unique_values('RAP.csv','CUT')
    flr_values = get_unique_values('BACK.csv','FLR')
    
    return render_template('index.html', certi_values=certi_values,shape_values=shape_values,
                            color_values=color_values,clarity_values=clarity_values,
                            cut_values=cut_values,flr_values=flr_values)

@app.route('/submit-data', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        certi = request.form.get('certi')
        shape = request.form.get('shape')
        carat = float(request.form.get('carat'))
        color = request.form.get('color')
        clarity = request.form.get('clarity')
        cut = request.form.get('cut')
        flr = request.form.get('flr')
        if request.form.get('roughcarat') != '':
            ro_carat = float(request.form.get('roughcarat'))
        else:
            ro_carat = request.form.get('roughcarat')

        rap_df = pd.read_csv('RAP.csv')
        back_df = pd.read_csv('BACK.csv')

        rap_row = rap_df.loc[(rap_df['SHAPE'] == shape) &
                        (rap_df['FROM CTS'] <= carat) &
                        (rap_df['TO CTS'] >= carat) &
                        (rap_df['COLOR'] == color) &
                        (rap_df['CLARITY'] == clarity) &
                        (rap_df['CUT'] == cut)]
        rap = rap_row['PRICE'].values[0]
        back_row = back_df.loc[(back_df['CERTI'] == certi) &
                        (back_df['FROM CTS'] <= carat) &
                        (back_df['TO CTS'] >= carat) &
                        (back_df['COLOR'] == color) &
                        (back_df['CLARITY'] == clarity) &
                        (back_df['FLR'] == flr)]
        back = back_row['%'].values[0]
        price = round((rap - ((rap*back)/100))*carat)

        if ro_carat == '':
            data  = f'${rap} / -{back}% / Value: ${price}'
        else:
            ro_price = round(price/ro_carat)
            data  = f'${rap} / -{back}% / Value: ${price} / Ro: ${ro_price}'


        return jsonify({'ppc': data})

if __name__ == '__main__':
    app.run(debug=True)
