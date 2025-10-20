import requests

def refresh_access_token(refresh_token, redirect_uri, scopes, client_id, client_secret, token_url):
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        access_token = response.json()
        return access_token['access_token']

    return None


if __name__ == '__main__':

    CLIENT_ID = "0oaofouxewL4eU1oh5d7"
    CLIENT_SECRET = "4urgBxlgj8PrE936ne9z1LWIccL_WIy4fM5NJ4nwmQX5D2H59oqQniaoUPzGMBE1"
    REDIRECT_URI = "http://localhost:8501"
    AUTH_URL = "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/authorize"
    TOKEN_URL = "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token"
    API_URL = "https://sandboxapi.deere.com/platform/organizations"
    SCOPES = "org1 work1 eq1 ag1 files offline_access"
    EMPRESA = "478393"
    REFRESH_TOKEN = 'IWAP1Wc0ycicVsbv92sFtmh02i0FzPZm2z2iozBqvtk'

    teste = refresh_access_token(
        REFRESH_TOKEN,
        REDIRECT_URI,
        SCOPES,
        CLIENT_ID,
        CLIENT_SECRET,
        TOKEN_URL
    )
    print(teste)