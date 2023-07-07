import os
import shutil
from datetime import datetime
from app import models

# Current date
now = datetime.now()
now_str = now.strftime("%Y-%m-%dT%H-%M-%S")

# Get new backup file
current_folder = os.path.dirname(os.path.abspath(__file__))
parent_folder = os.path.dirname(current_folder)
backup_folder = os.path.join(parent_folder, 'sql', 'backups')

backup_files = os.listdir(backup_folder)
new_backup_files = [file for file in backup_files if file == "backup"]

logs_origin = models.LogOrigin.objects.get (name="Rename Backups")
logs_type_error = models.LogType.objects.get (name="error")

if new_backup_files:
    backup_file = new_backup_files[0]
    
    # Rename file
    backup_file_path = os.path.join(backup_folder, backup_file)
    backup_file_path_new = os.path.join(backup_folder, f"backup_{now_str}")
    shutil.move (backup_file_path, backup_file_path_new)
    
    models.Log.objects.create (
        origin=logs_origin,
        details=f"Renamed backup file to {backup_file_path_new}"
    )
else:
    models.Log.objects.create (
        origin=logs_origin,
        details=f"No new backup files found",
        log_type=logs_type_error
    )
        
    
    