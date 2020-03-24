call C:\\ProgramData\\Anaconda3\\Scripts\\activate.bat
start chrome.exe "http://localhost:8000"
cd ../../Server/
python -m http.server 8000 --cgi
