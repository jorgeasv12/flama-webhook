from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
import traceback  # 👈 para mostrar el error real

app = Flask(__name__)

@app.route('/')
def home():
    return 'Webhook activo. Esperando pedidos de OlaClick.', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if not data:
            raise ValueError("No se recibió contenido JSON válido.")

        event_type = data.get("event", "sin_evento")

        folder_path = "/mnt/data/pedidos"
        os.makedirs(folder_path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{event_type}_{timestamp}.json"
        filepath = os.path.join(folder_path, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Pedido guardado en: {filepath}")
        return jsonify({"status": "ok", "message": f"Pedido guardado: {filename}"}), 200

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        traceback.print_exc()  # 👈 muestra el error completo en los logs
        return jsonify({"status": "error", "message": str(e)}), 500

from flask import send_from_directory

@app.route('/descargar/<filename>', methods=['GET'])
def descargar_json(filename):
    return send_from_directory('/mnt/data/pedidos', filename, as_attachment=True)
@app.route('/listado', methods=['GET'])
def listado_archivos():
    try:
        folder_path = "/mnt/data/pedidos"
        archivos = os.listdir(folder_path)
        archivos = [f for f in archivos if f.endswith(".json")]
        return jsonify(archivos), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



