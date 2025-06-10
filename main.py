from flask import Flask, request, jsonify
import requests
import hmac
import hashlib

app = Flask(__name__)

# Configuration Zadarma
ZADARMA_KEY = "90f769203bbc7e181f77"
ZADARMA_SECRET = "e9eea5a786f90e643c19" 

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    # Le numéro et le message sont envoyés dans le webhook
    numero = data.get('numero')  # Numéro du destinataire
    message = data.get('message')  # Message à envoyer
    
    if not numero or not message:
        return jsonify({"error": "Numero et message requis"}), 400
    
    # Envoyer SMS via Zadarma
    result = send_sms(numero, message)
    return jsonify({"success": True, "result": result})

def send_sms(to, text):
    # Code Zadarma...
    return "SMS envoyé"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
