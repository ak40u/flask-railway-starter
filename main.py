import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "8842069396:AAG37_X_NHnDRTHPnEKX-B8P8E5we_P7X24"
GEMINI_KEY = "AQ.Ab8RN6Jh1jIGxdNnsVWQUiq1U93KzpLMiJBzPJaStl80XENCMw"
ALLOWED_USER_ID = 8821953203

def send_telegram_msg(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            payload.pop("parse_mode", None)
            requests.post(url, json=payload, timeout=10)
    except Exception as e:
        try:
            payload.pop("parse_mode", None)
            requests.post(url, json=payload, timeout=10)
        except:
            pass

def get_gemini_reply(user_prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={GEMINI_KEY}"
    sys_prompt = ("Eres la Inteligencia Artificial privada de Isaac, desarrollador de Nova TV. "
                  "Respondes de forma experta, concisa y amable sobre IPTV, clientes, ventas y soporte. "
                  "Código de Downloader: 4123514. Servidores: NOVA 1 (Alfa TV) y NOVA 2 (Zona TV).")
    payload = {
        "contents": [{"parts": [{"text": f"{sys_prompt}\n\nIsaac pregunta: {user_prompt}"}]}]
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        pass
    return f"🤖 Hola Isaac. Recibí tu mensaje: '{user_prompt}'. Asistente de Nova TV listo."

@app.route('/', methods=['GET'])
def home():
    return "Servidor Webhook Nova TV 24/7 Activo en Railway"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"status": "error"}), 400

        if 'message' in data:
            msg = data['message']
            from_id = msg.get('from', {}).get('id')
            chat_id = msg.get('chat', {}).get('id')

            if from_id != ALLOWED_USER_ID:
                send_telegram_msg(chat_id, "⛔ Acceso privado exclusivo para Isaac / Nova TV.")
                return jsonify({"status": "unauthorized"}), 200

            text = msg.get('text', '').strip()
            if not text:
                send_telegram_msg(chat_id, "🎙️ Mensaje recibido. Actualmente procesamos consultas en texto.")
                return jsonify({"status": "ok"}), 200

            lower_t = text.lower()

            if "enviar lista" in lower_t or "dame la lista" in lower_t:
                reply = ("📄 *Lista Completa de Servidor Alfa TV:*\n\n"
                         "• Películas (VOD): 29,426\n"
                         "• Títulos de Series: 3,534\n"
                         "• Canales en Vivo: 1,767\n"
                         "• Total Títulos Únicos: 34,727\n\n"
                         "El archivo completo está guardado en tu PC en: `C:\\Users\\Admin\\Downloads\\solo_los_links_unicos.txt`")
            elif "whale" in lower_t or "web" in lower_t:
                reply = ("📺 *Avance de la WebApp para Whale OS:*\n\n"
                         "• Se instalaron las librerías nativas de Flutter Web (`web/index.html`).\n"
                         "• Se ajustó el reproductor para compatibilidad cross-platform HTML5.\n"
                         "• La app WebApp usará los mismos botones NOVA 1 y NOVA 2 con URLs encriptadas.")
            elif "compil" in lower_t or "apk" in lower_t:
                reply = ("🔨 *Compilación de App:*\n\n"
                         "Para compilar el APK en tu computadora, la laptop debe estar encendida en Android Studio.")
            else:
                reply = get_gemini_reply(text)

            send_telegram_msg(chat_id, reply)

        return jsonify({"status": "ok"}), 200
    except Exception as err:
        return jsonify({"status": "error", "message": str(err)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
