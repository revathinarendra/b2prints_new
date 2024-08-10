import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_ANON_KEY')

if not url or not key:
    raise ValueError("Supabase URL or Key not found in environment variables")

supabase: Client = create_client(url, key)

def upload_file(file, path):
    try:
        # Ensure that 'file' is in a format compatible with Supabase
        response = supabase.storage.from_('images').upload(path, file)

        # Check if the response object has a 'status_code' attribute
        if hasattr(response, 'status_code') and response.status_code == 200:
            return response.json()
        else:
            # Log and raise an exception for failed uploads
            raise Exception(f"Upload failed: {response.text}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
