from flask import Flask, render_template
app = Flask(__name__)

# TODO Sync the 3 sources files : js, csv, geojson
# TODO Scale on the map
# TODO clickable points
# TODO search univerities ?
# TODO marker cluster ?


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/<euc>")
def about(euc):
    print(euc)
    return home()


if __name__ == '__main__':
    app.run(debug=True)
