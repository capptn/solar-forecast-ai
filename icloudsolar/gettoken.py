import requests

# Setze die Basis-URL der iCloudSolar API
BASE_URL = 'https://augateway.isolarcloud.com'  # Beispiel-URL, anpassen nach API-Dokumentation

# Authentifizierungsinformationen
EMAIL = 'f.gdanietz@rudack-elektrotechnik.de'
PASSWORD = 'Rudack8510065!'

# Funktion, um einen Token zu erhalten
def get_auth_token(email, password):
    url = f"{BASE_URL}/auth/token"  # Der Endpunkt für die Token-Anfrage
    payload = {
        'email': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()['token']  # Anpassen nach API-Dokumentation
    else:
        print(f"Fehler bei der Token-Anfrage: {response.status_code}")
        print(response.json())
        return None

# Beispielaufruf der Funktion
if __name__ == "__main__":
    token = get_auth_token(EMAIL, PASSWORD)
    
    if token:
        print("Erhaltener Token:")
        print(token)
    else:
        print("Kein Token erhalten.")
