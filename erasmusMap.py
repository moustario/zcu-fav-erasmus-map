from flask import Flask, render_template, url_for
import json
app = Flask(__name__)

# TODO Sync the 3 sources files : js, csv, geojson
# TODO Scale on the map
# TODO clickable points
# TODO search univerities ?
# TODO marker cluster ?


@app.route("/")
def home():
    return render_template('index.html')


# @app.route("/<euc>")
# def about(euc):
#     print(euc)
#     with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson')) as json_file:
#         data = json.load(json_file)
#     print(data)
#     return render_template('university.html')


if __name__ == '__main__':
    app.run()
