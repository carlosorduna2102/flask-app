from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import json

# Define el alcance necesario para acceder a Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_calendar():
    """Autentica al usuario usando token.json o inicia el flujo OAuth si es necesario."""
    creds = None

    # Verifica si las credenciales existen en una variable de entorno
    if os.environ.get("GOOGLE_TOKEN"):
        creds = Credentials.from_authorized_user_info(json.loads(os.environ["GOOGLE_TOKEN"]), SCOPES)

    # Verifica si el archivo token.json existe
    elif os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Si no hay credenciales válidas, inicia el flujo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresca el token automáticamente
            creds.refresh(Request())
        else:
            # Inicia el flujo de autenticación manual
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        
        # Guarda las credenciales en token.json para autenticaciones futuras
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

def create_event(creds, title, description, location, start_time, end_time, timezone):
    """Crea un evento en Google Calendar."""
    try:
        # Construye el servicio de Google Calendar
        service = build('calendar', 'v3', credentials=creds)
        
        # Define los datos del evento
        event = {
            'summary': title,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            }
        }
        
        # Inserta el evento en el calendario principal
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        
        # Devuelve el enlace al evento creado
        return created_event.get('htmlLink')
    except Exception as e:
        raise Exception(f"Error al crear el evento: {str(e)}")
