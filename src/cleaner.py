import shutil
import magic            # Phase 0: The "Brain" for file types
import pytesseract      # Phase 0: The "Eyes" for OCR
from PIL import Image   # Phase 0: Image processing
from pathlib import Path
import time

class FileCleaner:
    # [Phase 1] The Setup
    def __init__(self, root_folder: Path):
        self.root_folder = root_folder
        
        # Mapping mime types to Folder Names
        self.type_mapping = {
            'image': 'Media/Images',
            'video': 'Media/Videos',
            'audio': 'Media/Audio',
            'application/pdf': 'Documents/PDFs',
            'application/zip': 'Archives',
            'text/plain': 'Documents/Text',
            'application/x-dosexec': 'Installers',  # .exe files
            'application/x-mach-binary': 'Installers' # Mac apps
        }

        # Your "Project" Keywords for Clustering
        self.project_keywords = [
            "Physics",
            "Finance",
            "Resume",
            "Invoice",
            "Project_Alpha" # Add your real projects here
        ]

    # [Phase 2] The "Eyes" (OCR Helper)
    def _scan_image_for_text(self, file_path: Path) -> str:
        # Private helper: Reads text inside an image.
        try:
            # Check if it's an image before trying to read it
            mime = magic.from_file(str(file_path), mime=True)
            if 'image' in mime:
                # Open image and extract text
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                return text.lower() # Return lowercase for easy comparison
        except Exception as e:
            # If OCR fails (e.g. file is corrupt), just move on. Don't crash.
            # print(f"OCR skipped for {file_path.name}: {e}")
            pass
        
        return ""

    # [Phase 3] The "Clusterer" (Context Helper)
    def _detect_project_context(self, file_path: Path) -> str:
        """
        Private helper: Checks if file belongs to a Project.
        """
        # 1. Check Filename (Fastest)
        filename_lower = file_path.name.lower()
        
        for keyword in self.project_keywords:
            if keyword.lower() in filename_lower:
                return f"Project_{keyword}"

        # 2. Check Content (Slower, but God-Tier)
        # We only scan if the filename didn't give us a match
        content_text = self._scan_image_for_text(file_path)
        
        if content_text:
            for keyword in self.project_keywords:
                if keyword.lower() in content_text:
                    print(f"OCR Magic: Found '{keyword}' inside {file_path.name}!")
                    return f"Project_{keyword}"
        
        return None

    # [Phase 4] The "Brain" (Decision Maker)
    def identify_category(self, file_path: Path) -> str:
        # Decides the final folder name.
        # PRIORITY 1: Check Projects first (Clustering)
        project_folder = self._detect_project_context(file_path)
        if project_folder:
            return project_folder

        # PRIORITY 2: Check File Type (Standard)
        try:
            # Get the real MIME type (ex., 'image/png')
            file_mime = magic.from_file(str(file_path), mime=True)
            
            # Check if any of our keys are in that mime type
            for key, folder in self.type_mapping.items():
                if key in file_mime:
                    return folder
        except Exception as e:
            print(f"Error reading file type: {e}")

        # Default fallback
        return "Misc"

    # [Phase 5] The Mover (Execution)
    def move_file(self, file_path: Path):
        """
        Moves the file to the correct folder safely.
        """
        if file_path.name.startswith(".") or file_path.name == "desktop.ini":
            return None

        category = self.identify_category(file_path)
        dest_folder = self.root_folder / category
        dest_folder.mkdir(parents=True, exist_ok=True)

        target_path = dest_folder / file_path.name
        
        # Collision handling
        if target_path.exists():
            stem = target_path.stem
            suffix = target_path.suffix
            counter = 1
            while target_path.exists():
                target_path = dest_folder / f"{stem}({counter}){suffix}"
                counter += 1

        try:
            shutil.move(str(file_path), str(target_path))
            print(f"Moved: {file_path.name}  --->  {category}")
            return str(target_path) 
            
        except Exception as e:
            print(f"Failed to move {file_path.name}: {e}")
            return None