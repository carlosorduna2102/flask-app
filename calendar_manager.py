from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Define el alcance necesario para acceder a Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_calendar():
    """Autentica al usuario y devuelve las credenciales."""
    creds = None

    # Verifica si ya existe el token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas, intenta autenticarse
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            # Muestra la URL de autenticación en los logs
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"Abre este enlace en tu navegador para autenticarte: {auth_url}")
            raise Exception("No es posible continuar. Por favor, completa la autenticación manual y sube 'token.json' al servidor.")
        
        # Guarda las credenciales en un archivo token.json
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

