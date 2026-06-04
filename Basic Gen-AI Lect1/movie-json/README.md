# movie-json

How to run the extraction script from PowerShell (Windows)

Prerequisites
- Create and activate a Python virtual environment in the repository root (there is a .venv in this workspace).
- Install dependencies:

```powershell
c:/Users/Hp/Desktop/Generative-AI/.venv/Scripts/python.exe -m pip install -r "c:/Users/Hp/Desktop/Generative-AI/requirements.txt"
```

Run the script

```powershell
# Activate the venv (optional if you call the venv python directly)
c:\Users\Hp\Desktop\Generative-AI\.venv\Scripts\Activate.ps1

# Run and type/paste the movie paragraph when prompted
c:/Users/Hp/Desktop/Generative-AI/.venv/Scripts/python.exe "c:/Users/Hp/Desktop/Generative-AI/movie-json/code.py"

# Or pass the paragraph as a single argument (quote it if it contains spaces)
c:/Users/Hp/Desktop/Generative-AI/.venv/Scripts/python.exe "c:/Users/Hp/Desktop/Generative-AI/movie-json/code.py" "A thrilling 2022 sci-fi film starring Alice and Bob..."
```

Notes
- The script expects environment variables for any API keys; create a `.env` file in the repository root if needed. The script uses `load_dotenv()` to load variables.
- If you encounter import errors, ensure the packages in `requirements.txt` are installed into the venv.
