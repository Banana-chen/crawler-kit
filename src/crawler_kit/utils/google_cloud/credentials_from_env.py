from google.oauth2.service_account import Credentials
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def credentials_from_env():
    credentials = Credentials.from_service_account_info(
        dict(
            type="service_account",
            project_id=getenv("PROJECT_ID"),
            client_email=getenv("CLIENT_EMAIL"),
            private_key=getenv("PRIVATE_KEY"),
            token_uri="https://oauth2.googleapis.com/token",
        )
    )
    return credentials


if __name__ == "__main__":
    credentials_from_env()
