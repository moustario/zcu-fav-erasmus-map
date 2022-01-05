from flask import Flask, render_template, url_for
import json
app = Flask(__name__)

# TODO Sync the 3 sources files : js, csv, geojson
# TODO Scale on the map
# TODO search univerities ?
# TODO marker cluster ?


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<euc>")
def about(euc):
    # EUC formated to prevents issues with . in url
    uni = get_from_euc('.'.join(euc.split('-')))
    return render_template('university.html', uni=uni)


def get_from_euc(euc):
    with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson'), encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
    for uni in data['features']:
        if uni['properties']['EUC'] == euc:
            return uni
    return dict()


if __name__ == '__main__':
    app.run()
