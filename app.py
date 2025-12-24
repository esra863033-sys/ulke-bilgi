from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Ana Sayfa
@app.route('/')
def home():
    return render_template('index.html')

# Ülke Arama API'si (Backend Proxy)
@app.route('/search', methods=['GET'])
def search_country():
    country_name = request.args.get('country')
    if not country_name:
        return jsonify({'error': 'Lütfen bir ülke adı girin.'}), 400
    
    # Rest Countries API'sine istek atıyoruz
    api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()[0] # İlk eşleşen sonucu al
        
        # Gerekli verileri ayıklıyoruz
        country_data = {
            'name': data.get('name', {}).get('common', 'N/A'),
            'capital': data.get('capital', ['N/A'])[0],
            'population': f"{data.get('population', 0):,}", # Sayıyı formatla
            'continent': data.get('continents', ['N/A'])[0],
            'region': data.get('region', 'N/A'),
            'currency': list(data.get('currencies', {}).keys())[0] if data.get('currencies') else 'N/A',
            'languages': ", ".join(data.get('languages', {}).values()),
            'flag': data.get('flags', {}).get('svg', ''),
            'maps': data.get('maps', {}).get('googleMaps', '#')
        }
        return jsonify(country_data)
    else:
        return jsonify({'error': 'Ülke bulunamadı!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
