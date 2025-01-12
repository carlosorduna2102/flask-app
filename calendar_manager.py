from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import re

# Alcance necesario para Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_calendar():
    """Autentica y obtiene credenciales para Google Calendar."""
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    return creds

def create_event(credentials, title, description, date, time, timezone):
    """Crea un evento en el calendario."""
    service = build('calendar', 'v3', credentials=credentials)
    
    # Convertir fecha y hora a formato ISO
    start_datetime = f"{date}T{time}:00{timezone}"
    end_datetime = f"{date}T{time}:00{timezone}"  # Puedes ajustar para sumar 1 hora automáticamente
    
    event = {
        'summary': title,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Alerta un día antes
                {'method': 'popup', 'minutes': 10},       # Alerta 10 minutos antes
            ],
        },
    }
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    return event_result.get('htmlLink')

def parse_message(message):
    """Extrae los detalles del mensaje."""
    # Ejemplo: "checar acuerdo de este expediente en 2025-01-15 a las 10:00"
    match = re.search(r'(.+) en (\d{4}-\d{2}-\d{2}) a las (\d{2}:\d{2})', message)
    if match:
        title = match.group(1).strip()
        date = match.group(2)
        time = match.group(3)
        return title, date, time
    else:
        raise ValueError("No se pudo interpretar el mensaje. Asegúrate de incluir 'en [fecha] a las [hora]'.")

if __name__ == '__main__':
    creds = authenticate_calendar()
    
    # Mensaje de prueba
    user_message = "checar acuerdo de este expediente en 2025-01-15 a las 10:00"
    try:
        title, date, time = parse_message(user_message)
        timezone = "America/Mexico_City"
        link = create_event(creds, title, "Evento creado desde GPT", date, time, timezone)
        print(f"Evento creado exitosamente: {link}")
    except ValueError as e:
        print(f"Error al procesar el mensaje: {e}")
