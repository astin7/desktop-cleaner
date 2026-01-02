import shutil
import os
import psutil
import platform
from pathlib import Path

class SystemOptimizer:
    def __init__(self):
        self.os_type = platform.system()
        
    def get_system_stats(self):
        """Returns a string with current CPU and RAM usage."""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        return f"CPU: {cpu}% | RAM: {memory}%"

    def get_cache_paths(self):
        """Identifies safe-to-delete cache folders based on OS."""
        paths = []
        user_home = Path.home()

        if self.os_type == "Darwin": # MacOS
            # The main user cache folder on Mac
            paths.append(user_home / "Library/Caches")
            # Optional: Slack/Discord logs often get huge
            paths.append(user_home / "Library/Logs")
            
        elif self.os_type == "Windows":
            # The Temp folder on Windows
            paths.append(Path(os.environ.get('TEMP')))
            # Windows Prefetch (Requires Admin, maybe skip for now)
        
        return paths

    def run_speed_up(self):
        """Deletes temporary files to free space/resources."""
        cleaned_size_mb = 0
        cache_folders = self.get_cache_paths()
        logs = []

        for folder in cache_folders:
            if not folder.exists():
                continue
            
            # Walk through the folder and delete contents
            for item in folder.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink() # Delete file
                        cleaned_size_mb += size
                    elif item.is_dir():
                        size = sum(f.stat().st_size for f in item.glob('**/*') if f.is_file())
                        shutil.rmtree(item) # Delete folder
                        cleaned_size_mb += size
                except Exception:
                    # Skip files currently in use (common in Caches)
                    pass
        
        # Convert bytes to MB
        mb_freed = round(cleaned_size_mb / (1024 * 1024), 2)
        return f"Speed Up Complete! Freed {mb_freed} MB of junk cache."