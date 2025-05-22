from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import traceback

app = Flask(__name__)

# ✅ Ruta principal que acepta GET y POST desde OlaClick
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
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
            traceback.print_exc()
            return jsonify({"status": "error", "message": str(e)}), 500

    # Si es GET
    return '🟢 Webhook de Flamha activo y esperando pedidos por POST.', 200


# ✅ Ruta alternativa que ya tenías configurada
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
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


# ✅ Descargar pedidos guardados
@app.route('/descargar/<filename>', methods=['GET'])
def descargar_json(filename):
    return send_from_directory('/mnt/data/pedidos', filename, as_attachment=True)

# ✅ Listado de archivos disponibles
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




