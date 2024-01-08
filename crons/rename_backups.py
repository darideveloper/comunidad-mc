# Add parent folder to path
import os
import sys
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Setup django settings
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comunidad_mc.settings')
django.setup()

import shutil
from datetime import datetime
from app import models

log_origin_name = "Rename Backups"
log_type_error = models.LogType.objects.get (name="error")
try:

    # Current date
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H-%M-%S")

    # Get new backup file
    current_folder = os.path.dirname(os.path.abspath(__file__))
    parent_folder = os.path.dirname(current_folder)
    backup_folder = os.path.join(parent_folder, 'sql', 'backups')

    backup_files = os.listdir(backup_folder)
    new_backup_files = [file for file in backup_files if file == "backup"]

    log_origin = models.LogOrigin.objects.get (name=log_origin_name)

    if new_backup_files:
        backup_file = new_backup_files[0]
        
        # Rename file
        backup_file_path = os.path.join(backup_folder, backup_file)
        backup_file_path_new = os.path.join(backup_folder, f"backup_{now_str}")
        shutil.move (backup_file_path, backup_file_path_new)
        
        models.Log.objects.create (
            origin=log_origin,
            details=f"Done. Filenam to: {backup_file_path_new}"
        )
    else:
        models.Log.objects.create (
            origin=log_origin,
            details=f"No new backup files found",
            log_type=log_type_error
        )
            
except Exception as e:
    
    log_type_error = models.LogType.objects.get (name="error")
    log_origin = models.LogOrigin.objects.get (name=log_origin_name)
    models.Log.objects.create (
        origin=log_origin,
        details=f"Uhknown error: {e}",
        log_type=log_type_error,
    )
    