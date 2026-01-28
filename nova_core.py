import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from bs4 import BeautifulSoup
import urllib.parse
import random
import os
import platform
import shutil



# -------------------------
# Initialize recognizer & TTS
# -------------------------
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 165)

voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.name.lower() or "david" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break


import subprocess
import sys

def on_wake_word():
    subprocess.Popen([sys.executable, "jarvis_orb.py"])


def speak(text):
    print("Nova:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------------
# Helper functions
# -------------------------
def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The time right now is {now}"

def get_date():
    today = datetime.date.today().strftime("%A, %d %B %Y")
    return f"Today is {today}"

def tell_joke():
    jokes = [
        "Why did the computer show up at work late? Because it had a hard drive!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why was the math book sad? Because it had too many problems.",
        "What’s a robot’s favorite snack? Computer chips!",
        "Why did the AI go to therapy? It had deep learning issues!",
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I asked my computer for a joke, but it said '404 Humor not found'.",
        "Parallel lines have so much in common... it’s a shame they’ll never meet!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break... and it said 'no problem, I’ll go to sleep.'"
    ]
    return random.choice(jokes)

def web_search(query):
    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}&hl=en"
        headers = {"User-Agent": "Mozilla/5.0"}
        page = requests.get(url, headers=headers, timeout=6)
        soup = BeautifulSoup(page.text, "html.parser")
        answer_box = soup.find("div", class_="BNeawe")
        if answer_box:
            return answer_box.get_text(strip=True)
    except Exception as e:
        print("web_search error:", e)
    return None

# -------------------------
# Cross-Platform App Opening
# -------------------------
def open_app(app_name):
    os_name = platform.system().lower()
    app_name = app_name.lower()

    common_apps = {
        "chrome": {
            "windows": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "darwin": "/Applications/Google Chrome.app",
            "linux": "google-chrome"
        },
        "edge": {
            "windows": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "darwin": "/Applications/Microsoft Edge.app",
            "linux": "microsoft-edge"
        },
        "whatsapp": {
            "windows": os.path.expandvars(r"%LOCALAPPDATA%\WhatsApp\WhatsApp.exe"),
            "darwin": "/Applications/WhatsApp.app",
            "linux": "whatsapp"
        },
        "notepad": {
            "windows": "notepad.exe",
            "darwin": "TextEdit",
            "linux": "gedit"
        },
        "calculator": {
            "windows": "calc.exe",
            "darwin": "Calculator",
            "linux": "gnome-calculator"
        },
        "vscode": {
            "windows": os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            "darwin": "/Applications/Visual Studio Code.app",
            "linux": "code"
        },
        "spotify": {
            "windows": os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
            "darwin": "/Applications/Spotify.app",
            "linux": "spotify"
        }
    }

    target = None
    if app_name in common_apps:
        target = common_apps[app_name].get(os_name)

    if target:
        try:
            if os_name == "windows":
                subprocess.Popen(target)
            elif os_name == "darwin":
                subprocess.Popen(["open", "-a", target])
            else:
                if shutil.which(target):
                    subprocess.Popen([target])
                else:
                    return f"{app_name} not found on Linux."
            return f"Opening {app_name}."
        except Exception as e:
            return f"Could not open {app_name}: {e}"
    else:
        try:
            if os_name == "windows":
                subprocess.Popen(app_name)
            elif os_name == "darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                if shutil.which(app_name):
                    subprocess.Popen([app_name])
                else:
                    return f"{app_name} not found on Linux."
            return f"Trying to open {app_name}."
        except Exception:
            return f"I couldn’t find {app_name} on your system."

# -------------------------
# YouTube Handling
# -------------------------
def handle_youtube(command):
    cmd_lower = command.lower()

    if "play" in cmd_lower:
        idx = cmd_lower.find("play")
        query = command[idx + len("play"):].strip()
        if query:
            try:
                import pywhatkit
                pywhatkit.playonyt(query)
                return f"Playing {query} on YouTube."
            except Exception as e:
                return f"Sorry, I couldn't play {query} due to {e}."
        else:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube homepage."

    elif "search" in cmd_lower:
        idx = cmd_lower.find("search")
        query = command[idx + len("search"):].strip()
        if query:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(query)}"
            webbrowser.open(url)
            return f"Opening YouTube and searching for {query}."
        else:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube homepage."

    else:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube."

# -------------------------
# Predefined Nova FAQ
# -------------------------
def nova_faq(command):
    cmd = command.lower()
    os_name = platform.system()
    if "your name" in cmd or "who are you" in cmd:
        return "My name is Nova, your personal assistant."
    elif "date of birth" in cmd or "birthday" in cmd or "when were you born" in cmd:
        return "I was created on 24th July 2025."
    elif "system" in cmd or "configuration" in cmd or "computer info" in cmd:
        try:
            info = f"Operating System: {os_name}, Platform: {platform.platform()}, Processor: {platform.processor()}"
            return info
        except Exception:
            return "I could not retrieve system information."
    else:
        return None

# -------------------------
# System default goodbye sound
# -------------------------
def play_goodbye_sound():
    system = platform.system()
    if system == "Windows":
        import winsound
        winsound.MessageBeep()
    elif system == "Darwin":
        os.system('afplay /System/Library/Sounds/Glass.aiff')
    else:
        print("\a")  # Terminal bell as fallback

# -------------------------
# Command processing
# -------------------------
def process_command(command):
    if not command:
        return None
    cmd = command.lower()

    # FAQ
    faq_answer = nova_faq(cmd)
    if faq_answer:
        return faq_answer

    # Praise
    praise = ["nice work", "good work", "well done", "awesome", "great job", "great work"]
    if any(p in cmd for p in praise):
        return random.choice(["Thanks!", "Glad you liked it!", "Appreciate it!"])

    # Time/date
    if "time" in cmd:
        return get_time()
    if "date" in cmd or "today" in cmd:
        return get_date()

    # Offline jokes
    if "joke" in cmd or "funny" in cmd:
        return tell_joke()

    # App opening
    if cmd.startswith("open ") and "youtube" not in cmd:
        app_name = cmd.replace("open ", "").strip()
        return open_app(app_name)

    # YouTube handling
    if "youtube" in cmd:
        return handle_youtube(command)

    # Google
    if "open google" in cmd:
        webbrowser.open("https://google.com")
        return "Opening Google."

    # Exit phrases
    if any(x in cmd for x in ["stop", "exit", "quit", "goodbye", "shut up", "keep quiet"]):
        return "exit"

    # Fallback search
    result = web_search(command)
    if result:
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(command)}")
        return result
    else:
        webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(command)}")
        return "I couldn’t find a short answer, so I opened Google for you."

# -------------------------
# Listening
# -------------------------
def listen(timeout=6, phrase_time_limit=6):
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.4)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return None

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Recognition error:", e)
        return None

# -------------------------
# Main Nova loop
# -------------------------
def nova():
    speak("Hello, I am Nova. How can I help you?")
    while True:
        command = listen()
        if not command:
            speak("Sorry, I didn't catch that.")
            continue

        result = process_command(command)
        if result == "exit":
            play_goodbye_sound()
            speak("Goodbye!")
            break
        if result:
            speak(result)

# -------------------------
# Run assistant
# -------------------------
if __name__ == "__main__":
    nova()
