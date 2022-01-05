from flask import Flask, render_template, url_for, request
import json
app = Flask(__name__)

# TODO Sync the 3 sources files : js, csv, geojson
# TODO Scale on the map
# TODO search univerities ?
# TODO marker cluster ?


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<euc>", methods=["GET", "POST"])
def about(euc):
    if request.method == 'GET':
        # EUC formated to prevents issues with . in url
        uni = get_from_euc('.'.join(euc.split('-')))
        return render_template('university.html', uni=uni)
    if request.method == 'POST':
        set_from_euc(request.json['properties']['EUC'], request.json)
        return {'status': 'operation success'}


def get_from_euc(euc):
    with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson'), encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
    for uni in data['features']:
        if uni['properties']['EUC'] == euc:
            return uni
    return dict()


def set_from_euc(euc, uni):
    with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson'), encoding='utf-8-sig') as json_file:
        data = json.load(json_file)
    for university in data['features']:
        if university['properties']['EUC'] == euc:
            university['properties'] = uni['properties']
            university['geometry'] = uni['geometry']
            print(university)
    with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson'), 'w', encoding='utf-8-sig') as fp:
        json.dump(data, fp, indent=4)


if __name__ == '__main__':
    app.run()
