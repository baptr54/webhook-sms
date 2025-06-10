from flask import Flask, request, jsonify
import requests
import hmac
import hashlib

app = Flask(__name__)

# Configuration Zadarma (à modifier avec vos vrais identifiants)
ZADARMA_KEY = "votre_cle_api"
ZADARMA_SECRET = "votre_secret_api" 
VOTRE_NUMERO = "33123456789"  # Votre numéro qui recevra les SMS

@app.route('/')
def home():
    return "Webhook SMS actif ! 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Récupérer les données du webhook
        data = request.get_json()
        
        # Message à envoyer
        message = f"Nouveau webhook reçu:\n{str(data)}"
        
        # Envoyer SMS via Zadarma
        send_zadarma_sms(VOTRE_NUMERO, message)
        
        return jsonify({"status": "SMS envoyé"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_zadarma_sms(numero, message):
    url = "https://api.zadarma.com/v1/sms/send/"
    
    # Données pour l'API
    params = {
        'number': numero,
        'message': message[:160]  # Limite SMS
    }
    
    # Signature Zadarma (simplifié pour test)
    headers = {
        'Authorization': f'{ZADARMA_KEY}:{ZADARMA_SECRET}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(url, data=params, headers=headers)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

