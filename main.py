from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Webhook SMS service is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        numero = data.get('numero')
        message = data.get('message')
        
        if not numero or not message:
            return jsonify({'error': 'Numéro et message requis'}), 400
        
        # Paramètres Free Mobile
        user = "03814779"
        pass_key = "bvD2CXpgIAIBPy"
        
        # URL Free Mobile
        url = f"https://smsapi.free-mobile.fr/sendmsg?user={user}&pass={pass_key}&msg={message}"
        
        print(f"📱 Envoi SMS vers {numero}: {message}")
        print(f"🔗 URL: {url}")
        
        # Requête avec timeout court
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            return jsonify({
                'status': 'success',
                'message': 'SMS envoyé!',
                'numero': numero
            }), 200
        else:
            return jsonify({
                'status': 'error', 
                'message': f'Erreur API: {response.status_code}'
            }), 400
            
    except requests.Timeout:
        return jsonify({'status': 'error', 'message': 'Timeout API SMS'}), 408
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

