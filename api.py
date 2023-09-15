from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from util import *
from constant import *

app = Flask(__name__)

@app.route(ApiPath.RATES, methods=[Methods.GET])
def scrape():
    # Örnek olarak Wikipedia'yı kullanıyorum
    url = Url.REQUEST_URL

    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to retrieve webpage"}), 500

    soup = BeautifulSoup(response.content, 'html.parser')

    soup = soup.find("div","detL")
    # URL'lerin listesi
    urls = ['/doviz-kurlari/', '/altin-fiyatlari/']

    data = {}

    for url in urls:
        # Belirtilen URL'yi içeren kutuyu bulma
        box_div = soup.find('a', href=url).find_parent('div', class_='boxTitle').find_parent('div')

        # Kutudaki tabloyu bulma
        table = box_div.find('table')
        table_data = {}

        # Tablodaki her satır için döngü
        for row in table.find_all('tr')[1:]:  # Başlığı atlayarak
            columns = row.find_all('td')
            currency = columns[0].text.strip()
            buy_rate = columns[1].text.strip()
            sell_rate = columns[2].text.strip()
            percentage = columns[3].text.strip()
            table_data[currency] = {
                'Alis': buy_rate,
                'Satis': sell_rate,
                '%': percentage
            }

        # Ana veri sözlüğüne eklenir
        data[url_to_name_mapping[url]] = table_data


    return custom_jsonify({
        "list": data
    })

if __name__ == '__main__':
    app.run(debug=True)