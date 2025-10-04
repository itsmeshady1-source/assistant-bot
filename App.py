import os
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# اقرأ مفتاح الـ API من متغير البيئة (ممنوع تكتب المفتاح هنا)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set the OPENAI_API_KEY environment variable in your Codespace or repo secrets")

openai.api_key = OPENAI_API_KEY

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_reply():
    user_input = request.form.get("msg", "")
    if not user_input:
        return jsonify({"reply": "Please send a message."})
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, friendly assistant for a fitness/business brand. Keep answers short and actionable."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.2
        )
        bot_reply = resp["choices"][0]["message"]["content"].strip()
    except Exception as e:
        bot_reply = f"Error: {str(e)}"
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
