import os.path
import pickle
import io
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from handlers.settings.google import load_google_key
from logs.logger import logger

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_PATH = 'token.pickle'


def drive_service():
    creds = None
    temp_file_path = None  # Track temp file
    try:
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                temp_file_path = load_google_key()  # load JSON temp file
                flow = InstalledAppFlow.from_client_secrets_file(
                    temp_file_path,
                    scopes=SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Deleted temporary key: {temp_file_path}")
            except Exception as ex:
                logger.exception(f"Warning: Failed to delete temp file: {ex}")

    service = build('drive', 'v3', credentials=creds)
    return service


def list_folder(folder_id):
    service = drive_service()
    query = f"('{folder_id}' in parents) and (mimeType='application/vnd.google-apps.folder' or mimeType='application/vnd.google-apps.document') and trashed = false"
    results = service.files().list(
        q=query,
        pageSize=50,
        fields="files(id, name, mimeType)"
    ).execute()

    return results.get("files", [])


def download_file_as_docx(file_id, destination_path):
    service = drive_service()
    request = service.files().export_media(
        fileId=file_id,
        mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

    fh = io.FileIO(destination_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()