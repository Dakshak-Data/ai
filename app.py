import streamlit as st
import threading
import time
import nova_core

st.set_page_config(page_title="Nova Assistant", page_icon="🤖", layout="centered")

# -------------------------
# Global state (thread-safe)
# -------------------------
CHAT_BUFFER = []
RUNNING_FLAG = False
THREAD_OBJ = None

# -------------------------
# UI Styling
# -------------------------
st.markdown("""
<style>
.chat-box {
    background-color: #111;
    padding: 10px;
    border-radius: 10px;
    height: 420px;
    overflow-y: auto;
    color: #00ffcc;
    font-family: monospace;
}
.user { color: #ffffff; }
.nova { color: #00ffcc; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Voice Loop Thread
# -------------------------
def voice_loop():
    global RUNNING_FLAG

    nova_core.speak("Hello, I am Nova. How can I help you?")
    CHAT_BUFFER.append(("Nova", "Hello, I am Nova. How can I help you?"))

    while RUNNING_FLAG:
        command = nova_core.listen()

        if not command:
            continue

        CHAT_BUFFER.append(("You", command))

        result = nova_core.process_command(command)

        if result == "exit":
            nova_core.play_goodbye_sound()
            nova_core.speak("Goodbye!")
            CHAT_BUFFER.append(("Nova", "Goodbye!"))
            RUNNING_FLAG = False
            break

        if result:
            nova_core.speak(result)
            CHAT_BUFFER.append(("Nova", result))

        time.sleep(0.1)

# -------------------------
# UI Layout
# -------------------------
st.title("🤖 Nova Voice Assistant")
st.caption("Streamlit Interface for your Python AI Assistant")

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Nova", use_container_width=True):
        if not RUNNING_FLAG:
            RUNNING_FLAG = True
            THREAD_OBJ = threading.Thread(target=voice_loop, daemon=True)
            THREAD_OBJ.start()

with col2:
    if st.button("⛔ Stop Nova", use_container_width=True):
        RUNNING_FLAG = False

# -------------------------
# Chat Display
# -------------------------
st.markdown("### 💬 Conversation")

chat_html = '<div class="chat-box">'
for sender, msg in CHAT_BUFFER:
    css = "user" if sender == "You" else "nova"
    chat_html += f"<p class='{css}'><b>{sender}:</b> {msg}</p>"
chat_html += "</div>"

st.markdown(chat_html, unsafe_allow_html=True)

# Auto refresh UI
time.sleep(0.4)
st.rerun()
