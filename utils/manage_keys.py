import keyring
from keyring.errors import KeyringError
from logs.logger import logger

SERVICE_NAME = "AutoTicketApp"


def save_credentials(username: str, password: str):
    try:
        keyring.set_password(SERVICE_NAME, username, password)
        return True
    except KeyringError as e:
        logger.exception(f"Keyring error: {e}")
        return False


def get_credential(username: str) -> str:
    try:
        return keyring.get_password(SERVICE_NAME, username)
    except KeyringError as e:
        logger.exception(f"Error retrieving credential: {e}")
        return None


def delete_credential(username: str):
    try:
        keyring.delete_password(SERVICE_NAME, username)
        return True
    except KeyringError as e:
        logger.exception(f"Keyring error: {e}")
        return False
