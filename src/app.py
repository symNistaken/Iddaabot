from flask import Flask, render_template, request, session, redirect, url_for
import os
import contextlib
from predictors.gemini_predictor import GeminiPredictor
from datetime import datetime

with open(os.devnull, 'w') as devnull, contextlib.redirect_stderr(devnull):
    import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "GÜVENLİ_BİR_SECRET_KEY"

genai.configure(api_key="AIzaSyB4ptLib_l0yrs3LsylaXcROe_kGRcA8V0")

predictor = GeminiPredictor(model_name="gemini-2.0-flash",)

@app.route("/", methods=["GET", "POST"])
def chat():
    if "conversation" not in session:
        session["conversation"] = []

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input.lower() in ["exit", "quit"]:
            session["conversation"] = []
            return redirect(url_for("chat"))
        
        if not user_input or len(user_input) < 3:
            prediction = "Lütfen daha anlamlı bir mesaj girin."
            session["conversation"].append({"sender": "Sistem", "message": prediction})
            session.modified = True
            return redirect(url_for("chat"))
        
        match_data = user_input  # Assume user input is match data
        try:
            prediction = predictor.predict_match(match_data)
        except Exception as e:
            prediction = "Bir hata oluştu, lütfen tekrar deneyin."
        
        session["conversation"].append({
            "sender": "Müşteri",
            "message": user_input,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        session["conversation"].append({
            "sender": "iddaa Bot",
            "message": prediction,
            "timestamp": datetime.now().strftime("%H:%M")
        })
        session.modified = True

        return redirect(url_for("chat"))  # POST sonrası redirect

    return render_template("chat.html", conversation=session.get("conversation", []))

@app.route("/clear", methods=["POST"])
def clear_conversation():
    session["conversation"] = []
    return ("", 204)

if __name__ == "__main__":
    app.run(debug=True)


