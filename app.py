from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return 'Webhook activo. Esperando pedidos de OlaClick.', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        event_type = data.get("event", "sin_evento")

        # Crear carpeta si no existe (opcional, en Render no sirve, pero útil localmente)
        os.makedirs("pedidos", exist_ok=True)

        # Guardar archivo con nombre descriptivo (solo útil en desarrollo local)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{event_type}_{timestamp}.json"

        with open(os.path.join("pedidos", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # ✅ Imprimir información en Logs de Render
        print(f"[OK] Pedido recibido. Evento: {event_type}")
        print("Contenido del pedido:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

        return jsonify({"status": "ok", "message": "Evento recibido"}), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

