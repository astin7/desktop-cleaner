from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from src.cleaner import FileCleaner
import shutil
import time

# 1. Setup the "Sandbox" (A fake Desktop)
sandbox = Path.home() / "Desktop" / "Cleaner_Test_Zone"

def setup_sandbox():
    """Creates a folder and fills it with dummy files for testing."""
    if sandbox.exists():
        shutil.rmtree(sandbox) # Wipes it clean to start fresh
    sandbox.mkdir()

    print(f"Creating test files in: {sandbox}")

    # TEST A: Standard Files (Should go to Documents, Media/Images)
    (sandbox / "boring_document.txt").touch()
    (sandbox / "vacation_photo.jpg").touch()
    
    # TEST B: Filename Project Clustering (Should go to Project_Physics)
    (sandbox / "Physics_Homework_Final.pdf").touch()

    # TEST C: OCR "God Mode" (Should go to Project_Invoice)
    # We need to create a REAL image with text inside for Tesseract to read.
    print("Generating a fake receipt image for OCR test...")
    img = Image.new('RGB', (400, 200), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    # We write the word "Invoice" in black text
    d.text((10,10), "This is an official Invoice for $500", fill=(0,0,0))
    img.save(sandbox / "random_scan_001.png")

    # TEST D: Collision (Should be renamed)
    (sandbox / "duplicate.txt").touch()
    (sandbox / "duplicate.txt").touch() # This won't actually create two, so we handle it in logic usually, 
                                       # but for this test, we'll just let the cleaner run twice.

def run_test():
    setup_sandbox()
    
    # Initialize your cleaner
    cleaner = FileCleaner(sandbox)

    print("\n--- STARTING CLEAN ---")
    
    # Loop through the sandbox and clean every file
    # We list files first so we don't trip over folders we just created
    files_to_move = [f for f in sandbox.iterdir() if f.is_file()]
    
    for file in files_to_move:
        cleaner.move_file(file)

    print("\n--- TEST COMPLETE ---")
    print(f"Go check the folder: {sandbox}")
    print("Expectations:")
    print("1. 'boring_document.txt' -> Documents/Text")
    print("2. 'Physics_Homework...' -> Project_Physics")
    print("3. 'random_scan_001.png' -> Project_Invoice (Did OCR work?)")

if __name__ == "__main__":
    run_test()