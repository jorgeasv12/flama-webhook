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
        data = request.json

        # Crear nombre de archivo con fecha y hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pedido_{timestamp}.json"

        # Asegurar que la carpeta "pedidos" existe
        os.makedirs("pedidos", exist_ok=True)

        # Guardar el JSON recibido
        with open(os.path.join("pedidos", filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({"status": "ok", "message": "Pedido recibido"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
