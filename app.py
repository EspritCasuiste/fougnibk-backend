from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        # 1. Récupérer les données du formulaire
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # 2. Construire le message
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = "Fougni.bk <serviceclient@fougnibk.ci>"
        msg["To"] = "serviceclient@fougnibk.ci"
        msg["Reply-To"] = email
        msg.set_content(f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}")

        # 3. Envoi de l'email via SMTP SSL
        with smtplib.SMTP_SSL("mail.fougnibk.ci", 465) as smtp:
            smtp.login("serviceclient@fougnibk.ci", "fougniservice")
            smtp.send_message(msg)

        # 4. Réponse côté client
        return jsonify({"success": True, "message": "Votre message a été envoyé avec succès."})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Point d’entrée
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
