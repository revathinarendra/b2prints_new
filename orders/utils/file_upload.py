# your_app/utils/file_upload.py

import os
from supabase import create_client, Client

# Load environment variables
url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_ANON_KEY')
supabase: Client = create_client(url, key)

def upload_file(file, path):
    try:
        response = supabase.storage.from_('images').upload(path, file)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Upload failed: {response.text}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
