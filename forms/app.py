from flask import Flask, request, jsonify
from flask_cors import CORS  # Ajouté pour activer CORS
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
CORS(app)  # Active CORS pour permettre les requêtes depuis ton site HTML

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = "Fougni.bk <serviceclient@fougnibk.ci>"
        msg["To"] = "serviceclient@fougnibk.ci"
        msg["Reply-To"] = email
        msg.set_content(f"Nom : {name}\nEmail : {email}\n\nMessage :\n{message}")

        with smtplib.SMTP_SSL("mail.fougnibk.ci", 465) as smtp:
            smtp.login("serviceclient@fougnibk.ci", "fougniservice")
            smtp.send_message(msg)

        return jsonify({"success": True, "message": "Votre message a été envoyé avec succès."})
    except Exception as e:
        print("Erreur serveur :", e)
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
