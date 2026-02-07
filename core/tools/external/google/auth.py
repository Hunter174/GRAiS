from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError


def get_credentials(credentials_file, token_file, scopes):
    creds = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), scopes)

    if creds and creds.scopes:
        missing = set(scopes) - set(creds.scopes)
        if missing:
            raise RuntimeError(f"OAuth token missing required scopes: {missing}")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                token_file.unlink(missing_ok=True)
                creds = None

        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file),
                scopes,
            )
            creds = flow.run_local_server(
                port=0,
                prompt="consent",
            )

            token_file.parent.mkdir(parents=True, exist_ok=True)
            token_file.write_text(creds.to_json())

    return creds
