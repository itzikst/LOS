---
description: How to set up a local debug session for the LOS backend
---

Follow these steps to run the LOS backend locally for debugging:

1. **Open a terminal** in the `LOS` project directory:
   `cd c:\Users\itzik\.gemini\antigravity\scratch\LOS`

2. **Activate the virtual environment**:
   `.\venv\Scripts\activate`

3. **Install dependencies**:
   `C:\Users\itzik\.gemini\antigravity\scratch\LOS\venv\Scripts\pip.exe install -r requirements.txt`

4. **Run the Flask application** (using the absolute path):
   `C:\Users\itzik\.gemini\antigravity\scratch\LOS\venv\Scripts\python.exe main.py`
   > [!IMPORTANT]
   > Copy and paste this exact absolute path. It bypasses any path confusion or global Python aliases.

5. **Test the API**:
   Open your browser or use `curl`:
   `http://127.0.0.1:8080/?start_lat=31.7719&start_lng=35.2170&end_lat=31.8&end_lng=35.25`

## Debugging with VS Code
If you are using VS Code:
1. Open the `LOS` folder.
2. Click on the **Run and Debug** icon in the sidebar.
3. Select **Python Debugger: Flask**.
4. Set breakpoints in `los.py` or `main.py` by clicking to the left of the line numbers.
