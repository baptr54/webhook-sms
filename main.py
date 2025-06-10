from flask import Flask, request, jsonify
import requests
import hmac
import hashlib
import base64
from datetime import datetime

app = Flask(__name__)

# Configuration Zadarma
ZADARMA_KEY = "90f769203bbc7e181f77"
ZADARMA_SECRET = "e9eea5a786f90e643c19"

@app.route('/')
def home():
    return "🚀 Webhook SMS Zadarma actif !"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        print(f"📨 Webhook reçu: {data}")
        
        # Récupérer numéro et message depuis le webhook
        numero = data.get('numero')
        message = data.get('message')
        
        if not numero or not message:
            return jsonify({"error": "❌ 'numero' et 'message' requis"}), 400
        
        # Nettoyer le numéro (enlever espaces, tirets, etc.)
        numero_clean = ''.join(filter(str.isdigit, numero))
        
        # Ajouter +33 si ça commence par 06/07 (France)
        if numero_clean.startswith('06') or numero_clean.startswith('07'):
            numero_clean = '33' + numero_clean[1:]
        
        print(f"📱 Envoi SMS vers: {numero_clean}")
        print(f"💬 Message: {message}")
        
        # Envoyer le SMS
        result = send_sms_zadarma(numero_clean, message)
        
        return jsonify({
            "success": True, 
            "numero": numero_clean,
            "message": message,
            "result": result
        })
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

def send_sms_zadarma(to, text):
    try:
        url = "https://api.zadarma.com/v1/sms/send/"
        
        # Paramètres pour l'API Zadarma
        params = {
            'number': to,
            'message': text
        }
        
        # Signature pour Zadarma (requis pour l'authentification)
        method = 'POST'
        params_string = '&'.join([f"{k}={v}" for k, v in sorted(params.items())])
        string_to_sign = method + url + params_string
        
        signature = base64.b64encode(
            hmac.new(
                ZADARMA_SECRET.encode('utf-8'),
                string_to_sign.encode('utf-8'),
                hashlib.sha1
            ).digest()
        ).decode('utf-8')
        
        headers = {
            'Authorization': f'{ZADARMA_KEY}:{signature}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post(url, data=params, headers=headers)
        
        print(f"📡 Réponse Zadarma: {response.status_code}")
        print(f"📄 Contenu: {response.text}")
        
        return response.json() if response.status_code == 200 else {"error": response.text}
        
    except Exception as e:
        return {"error": f"Erreur envoi SMS: {str(e)}"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

