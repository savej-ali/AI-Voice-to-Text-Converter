import tkinter as tk
from tkinter import filedialog, messagebox
import os
from utils import prepare_audio, generate_transcription  

selected_audio = None  # Holds uploaded audio file path

def browse_audio():
    global selected_audio
    selected_audio = filedialog.askopenfilename(
        title="Choose an audio file",
        filetypes=[("WAV Audio", "*.wav"), ("All Files", "*.*")]
    )
    if selected_audio:
        filename_display = os.path.basename(selected_audio)
        status_msg.config(text=f"📂 Loaded: {filename_display}", fg="#0066cc")

        transcript_box.config(state='normal')
        transcript_box.delete("1.0", tk.END)
        transcript_box.config(state='disabled')

def process_transcription():
    global selected_audio
    if not selected_audio:
        messagebox.showinfo("No File Chosen", "Please select a WAV file before transcribing.")
        return
    try:
        status_msg.config(text="🧠 Processing transcription...", fg="#444")
        app.update()

        formatted_audio = prepare_audio(selected_audio)
        output_text = generate_transcription(formatted_audio)

        transcript_box.config(state='normal')
        transcript_box.delete("1.0", tk.END)
        transcript_box.insert(tk.END, output_text)
        transcript_box.config(state='disabled')

        status_msg.config(text="✅ Done! Transcription is ready.", fg="green")
    except Exception as err:
        messagebox.showerror("Transcription Error", str(err))
        status_msg.config(text="❌ Error during transcription.", fg="red")

# ------------------ GUI Setup ------------------
app = tk.Tk()
app.title("🎧 Voice-to-Text AI Converter")
app.geometry("700x520")
app.configure(bg="#ffffff")

# Header Label
header = tk.Label(app, text="Voice to Text Transcriber", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#222")
header.pack(pady=(20, 8))

# Frame for buttons and output
container = tk.Frame(app, bg="#ffffff")
container.pack(padx=20, pady=10, fill="both", expand=True)

# Upload Button
upload_button = tk.Button(
    container, text="🔍 Select WAV File", command=browse_audio,
    font=("Segoe UI", 12), bg="#1e88e5", fg="white",
    activebackground="#1976d2", padx=12, pady=6, relief="flat", cursor="hand2"
)
upload_button.pack(pady=8)

# Transcription Button
run_button = tk.Button(
    container, text="▶️ Start Transcription", command=process_transcription,
    font=("Segoe UI", 12), bg="#43a047", fg="white",
    activebackground="#388e3c", padx=12, pady=6, relief="flat", cursor="hand2"
)
run_button.pack(pady=8)

# Output Text Box
transcript_box = tk.Text(container, wrap="word", height=10, font=("Segoe UI", 11), padx=10, pady=10, relief="solid", bd=1)
transcript_box.pack(fill="both", expand=True, padx=10, pady=10)
transcript_box.config(state='disabled')

# Status Label
status_msg = tk.Label(app, text="", font=("Segoe UI", 10), bg="#ffffff", fg="#555")
status_msg.pack(pady=6)

# Footer
credit = tk.Label(app, text="Crafted by Savej Ali", font=("Segoe UI", 9), bg="#ffffff", fg="gray")
credit.pack(side="bottom", pady=10)

app.mainloop()
