from flask import Flask, render_template, url_for, request
import json
import csv
app = Flask(__name__)

# TODO search univerities ?
# TODO marker cluster ?


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/euc/<euc>", methods=["GET", "POST"])
def about(euc):
    if request.method == 'GET':
        # EUC formated to prevents issues with . in url
        uni = get_from_euc('.'.join(euc.split('-')))
        return render_template('university.html', uni=uni)
    if request.method == 'POST':
        set_from_euc(request.json['properties']['EUC'], request.json)
        return {'status': 'modification save successfull'}


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        f = request.files['file']
        # update Geojson
        f.save('./static/sources/'+f.filename)
        with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.geojson'), encoding='utf-8-sig') as json_file:
            data = json.load(json_file)
        # Update ErasmusBody
        with open('./'+url_for('static', filename='sources/ErasmusBody.js'), 'w', encoding='utf-8-sig') as js_file:
            js_file.write('var geobody = ')
            json.dump(data, js_file, indent=4, ensure_ascii=False)
            js_file.write(';')
        # Update csv
        csv_columns_original = ['katedra', 'platnost do', 'Name of institute', 'Name of institute (EN)', 'Country Code', 'City Code', 'Erasmus Code', 'EUC', 'City', 'Representative Name', 'Representative Function', 'Latitude', 'Longitude', 'Domain', 'Website', 'ECTSWebsite', 'Language of Instruction 1', 'Language of Instruction 2', 'Student Mobility for Studies - Level', 'Staff Mobility for Studies - Level', 'Autumn Term', 'Spring Term', 'Subject area name', 'Subject area code',
                                'Number of students', 'Number of months', 'Name of D. Coordinator', 'Departmental Coordinator', 'Phone', 'Fax', 'Email', 'Street', 'Zip code', 'City1', 'Country', 'Name of I. Coordinator', 'Institutional Coordinator', 'Phone 2', 'Fax 2', 'Email 2', 'Street 2', 'Zip code 2', 'City 2', 'Country 2', 'Grading', 'WWW for Incoming Students', 'Course Catalogue', 'Housing', 'Visa Information', 'Insurance Information', 'Students and Stuff with disailities', 'neco1', 'neco2', 'Logo']
        csv_columns_dynamic = data['features'][0]['properties'].keys()
        csv_columns = csv_columns_dynamic if request.form.get(
            'dynamic_csv_columns') else csv_columns_original
        with open('./'+url_for('static', filename='sources/IIA-CZ.PLZEN01-data-valid.csv'), 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.DictWriter(
                csv_file, fieldnames=csv_columns, extrasaction='ignore')
            writer.writeheader()
            for row in data['features']:
                writer.writerow(row['properties'])

        return {'status': 'file upload successfull'}


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
        json.dump(data, fp, indent=4,  ensure_ascii=False)


if __name__ == '__main__':
    app.run()
