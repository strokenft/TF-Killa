import customtkinter as ctk
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, JoinEvent
from TikTokLive.client.errors import UserNotFoundError
import threading
import asyncio
import os
import sys

ctk.set_appearance_mode("dark")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Themes: "blue", "dark-blue", "green"

def start_gui():
    client = None
    client_thread = None
    connected = False
    lines_buffer = []

    def append_output(text):
        lines_buffer.append(text)
        if len(lines_buffer) > 100:
            lines_buffer.pop(0)

        output.configure(state="normal")
        output.delete(1.0, ctk.END)
        output.insert(ctk.END, "\n".join(lines_buffer) + "\n")
        output.configure(state="disabled")
        output.see(ctk.END)

    def safe_append_output(text):
        window.after(0, append_output, text)

    def enable_ui():
        connect_btn.configure(state="normal")
        username_entry.configure(state="normal")

    def safe_enable_ui():
        window.after(0, enable_ui)

    def start_client(username):
        nonlocal client, client_thread, connected
        client = TikTokLiveClient(unique_id=username)
        connected = True

        @client.on(ConnectEvent)
        async def on_connect(event):
            if connected:
                safe_append_output("✅ Connected to LIVE!")

        @client.on(JoinEvent)
        async def on_join(event):
            if connected:
                safe_append_output(f"👤 @{event.user.nickname} joined!")

        def run():
            try:
                asyncio.set_event_loop(asyncio.new_event_loop())
                client.run()
            except UserNotFoundError:
                safe_append_output("❌ User not found. Please check the username and try again.")
                safe_enable_ui()
                nonlocal connected
                connected = False
            except Exception as e:
                safe_append_output(f"⚠️ Unexpected error: {e}")
                safe_enable_ui()
                connected = False

        client_thread = threading.Thread(target=run, daemon=True)
        client_thread.start()

    def on_connect_click():
        username = username_entry.get().strip().lstrip("@")
        if username:
            start_client(username)
            connect_btn.configure(state="disabled")
            username_entry.configure(state="disabled")

    window = ctk.CTk()
    window.wm_attributes("-alpha", 0.9)
    window.title("Joined User Logger!")
    window.geometry("500x400")
    window.minsize(400, 300)

    # Load .ico from PyInstaller bundle or dev folder
    if hasattr(sys, "_MEIPASS"):
        icon_path = os.path.join(sys._MEIPASS, "favicon.ico")
    else:
        icon_path = "favicon.ico"

    try:
        window.iconbitmap(icon_path)
    except Exception as e:
        print(f"Couldn't set window icon: {e}")

    # Layout
    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(3, weight=1)

    label = ctk.CTkLabel(window, text="Enter your TikTok LIVE username:", anchor="w", font=ctk.CTkFont(size=16))
    label.grid(row=0, column=0, pady=(15, 5), padx=15, sticky="we")

    username_entry = ctk.CTkEntry(window, placeholder_text="Username", corner_radius=12, font=ctk.CTkFont(size=14))
    username_entry.grid(row=1, column=0, padx=15, sticky="we")

    connect_btn = ctk.CTkButton(window, text="Connect", corner_radius=12, command=on_connect_click)
    connect_btn.grid(row=2, column=0, pady=10, padx=15, sticky="we")

    output = ctk.CTkTextbox(
        window,
        state="disabled",
        font=ctk.CTkFont(family="Segoe UI Emoji", size=12),
        corner_radius=12
    )
    output.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 15))

    window.mainloop()

if __name__ == "__main__":
    start_gui()
