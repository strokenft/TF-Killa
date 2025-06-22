In order to run the script, you will need Python installed and the following libraries--most of which are already built into Python;
os
sys
threading
asyncio
TikTokLive
customtkinter

If you attempt to run the JUL.py script, and it returns a 'Module Not Found' error, run the command shell prompt 'pip install' followed by the name of the module, and ensure that you are within the correct environment.

In order to turn the JUL.py into an executable file, you will have to run 'pip install pyinstaller' and run the following command shell prompt;
pyinstaller --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." JUL.py
