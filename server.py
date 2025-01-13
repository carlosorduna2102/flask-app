from flask import Flask, request, jsonify
from calendar_manager import authenticate_calendar, create_event
import os  # Importamos os para usar la variable de entorno PORT

# Inicializar Flask y autenticar Google Calendar
app = Flask(__name__)
creds = authenticate_calendar()  # Autenticación al iniciar el servidor

# Ruta básica para verificar que el servidor está funcionando
@app.route('/')
def home():
    return "Servidor Flask en ejecución y listo para recibir solicitudes."

# Endpoint para crear eventos en Google Calendar
@app.route('/create_event', methods=['POST'])
def create_event_endpoint():
    """Endpoint para crear eventos en Google Calendar."""
    data = request.json  # Recibir datos en formato JSON
    title = data.get('title', 'Evento sin título')
    description = data.get('description', '')
    location = data.get('location', 'Sin ubicación')
    start_time = data['start_time']  # Requiere 'YYYY-MM-DDTHH:MM:SS'
    end_time = data['end_time']      # Requiere 'YYYY-MM-DDTHH:MM:SS'
    timezone = data.get('timezone', 'America/Mexico_City')

    # Crear el evento con los datos proporcionados
    try:
        link = create_event(creds, title, description, location, start_time, end_time, timezone)
        return jsonify({'message': 'Evento creado exitosamente', 'link': link}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Leer el puerto de la variable de entorno PORT (Render lo asigna automáticamente)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Si no está definido, usa el puerto 8080
    app.run(host='0.0.0.0', port=port)
