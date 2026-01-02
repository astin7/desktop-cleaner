import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.cleaner import FileCleaner

class CleanerHandler(FileSystemEventHandler):
    def __init__(self, cleaner_instance, logger_func=None):
        self.cleaner = cleaner_instance
        self.logger = logger_func # The Microphone

    def on_modified(self, event):
        if event.is_directory: return
        
        file_path = Path(event.src_path)
        if file_path.name == ".DS_Store" or file_path.suffix == ".tmp": return

        # Wait for download to finish
        if self._wait_for_file_ready(file_path):
            # Move the file
            new_path = self.cleaner.move_file(file_path)
            
            # If successful, speak into the microphone
            if new_path and self.logger:
                message = f"✅ Moved: {file_path.name} -> {Path(new_path).parent.name}"
                self.logger(message)

    def _wait_for_file_ready(self, file_path: Path, retries=5) -> bool:
        if not file_path.exists(): return False
        historical_size = -1
        for _ in range(retries):
            try:
                current_size = file_path.stat().st_size
                if current_size == historical_size and current_size > 0:
                    return True 
                historical_size = current_size
                time.sleep(1) 
            except OSError:
                return False
        return False

class DesktopWatcher:
    def __init__(self, folder_to_watch: Path, logger_func=None):
        self.folder_to_watch = folder_to_watch
        self.cleaner = FileCleaner(folder_to_watch)
        # Pass the logger function down to the handler
        self.event_handler = CleanerHandler(self.cleaner, logger_func)
        self.observer = Observer()

    def start(self):
        print(f"👀 Watching {self.folder_to_watch} for new files...")
        self.observer.schedule(self.event_handler, str(self.folder_to_watch), recursive=False)
        self.observer.start()

    def stop(self):
        print("\nStopping watcher...")
        self.observer.stop()
        self.observer.join()