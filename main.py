from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Configuration Twilio
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_client = Client(account_sid, auth_token)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Récupérer les données du formulaire
        data = request.form

        # Envoyer SMS avec Twilio
        message = twilio_client.messages.create(
            body=f"Nouveau message: {data}",
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            to=os.environ.get('YOUR_PHONE_NUMBER')
        )

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
