# 🤖 AI Desktop Cleaner (Pro)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6%20(Qt)-green.svg)](https://doc.qt.io/qtforpython/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive, automated desktop organization tool built with Python. This application goes beyond simple file sorting by using Optical Character Recognition (OCR) to "read" the contents of your files and group them by context, all wrapped in a professional, dark-mode GUI.

*(**Pro Tip:** Take a screenshot of your app with the "SystemCare" sidebar visible and paste it here!)*

---

## Features

* **Context-Aware Sorting:** Unlike standard cleaners that sort by file extension, this tool uses OCR (Tesseract) to read text inside images and PDFs to categorize them by project (e.g., grouping a PNG receipt and a PDF invoice into a "Financial" folder).
* **Real-Time Automation:** A background "Watchdog" service monitors your desktop 24/7. Files are sorted the instant they are saved or downloaded.
* **Smart Stability Checks:** Intelligently detects when large files are still downloading to prevent corruption during movement.
* **System Speed Up:** Includes a "Boost" module that analyzes CPU/RAM usage and clears system cache/junk files to free up resources.
* **Professional GUI:** A responsive, dark-themed interface built with **PySide6 (Qt)**, featuring live activity logging and system monitoring.

---

## Technology Stack

* **Language:** Python
* **GUI Framework:** PySide6 (Qt for Python)
* **OCR Engine:** Tesseract (via `pytesseract`)
* **Automation:** Watchdog (Filesystem events)
* **System Utilities:** psutil (CPU/RAM monitoring)
* **Image Processing:** Pillow (PIL)
* **File Identification:** python-magic (Libmagic)

---

## Getting Started

Follow these instructions to get a local copy of the project up and running.

### Prerequisites

* Python 3.9 or higher
* **Tesseract OCR Engine** (Required for the "Reading" feature)
    * *Mac:* `brew install tesseract`
    * *Windows:* [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
* **Libmagic** (Required for file type detection)
    * *Mac:* `brew install libmagic`
    * *Windows:* `pip install python-magic-bin`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/astin7/ai-desktop-cleaner.git](https://github.com/astin7/ai-desktop-cleaner.git)
    cd ai-desktop-cleaner
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv env
    source env/bin/activate

    # For Windows
    python -m venv env
    .\env\Scripts\activate
    ```
3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Application:**
    ```bash
    python main.py
    ```

---

## Usage

1.  **Select Target:** Upon launching, use the "Select Folder" button to choose which directory to monitor (Defaults to `Desktop/Cleaner_Test_Zone` for safety).
2.  **Start Cleaning:** Click the large **SCAN** button. The app is now live. Drop any file into the target folder, and watch it instantly move to the correct category.
3.  **Boost System:** Click the **Speed Up** tab in the sidebar to view real-time CPU/RAM stats. Click **BOOST** to clear temporary cache files and free up memory.
4.  **Customize Rules:** Open `src/cleaner.py` to add your own "Project Keywords" (e.g., "Physics", "Clients") to the sorting logic.

---

## Author

Created by **Astin**.

* GitHub: [@astin7](https://github.com/astin7)
* LinkedIn: [Astin Huynh](https://www.linkedin.com/in/astin-huynh-3a4a24352/)

---

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.