from flask import Response
import json
def custom_jsonify(data):
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

url_to_name_mapping = {
    "/doviz-kurlari/": "Doviz_Kurlari",
    "/altin-fiyatlari/": "Altin_Fiyatlari"
}