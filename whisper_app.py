import os
import time
import whisper
import customtkinter as ctk
import sounddevice as sd
import wave
import threading
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import pyperclip
from tkinter import filedialog, messagebox



title_no=0
save_directory_label_no = title_no+1
change_directory_button_no= save_directory_label_no+1
select_model_no = change_directory_button_no + 1
record_button_no=select_model_no+1
choose_file_button_no=record_button_no+1
transcription_box_no=choose_file_button_no+1
copy_button_no=transcription_box_no+1
footer_label_no = copy_button_no + 1



# Load the Whisper model
#model = whisper.load_model("medium")

# Global variables
recording = False
paused = False
output_directory = os.getcwd()
audio_file_path = ""
text = None
running = False

# Function to transcribe audio
def transcribe_audio(file_path):
    global running, record_button
    running = True

    try:
        result = model.transcribe(file_path)
        transcription = result["text"]

        # Display the transcription in the text box
        transcription_box.delete("1.0", "end")
        transcription_box.insert("end", transcription)

        # Save the transcription to a text file
        output_file = os.path.join(output_directory, os.path.basename(file_path) + ".txt")
        with open(output_file, "w", encoding="utf-8") as text_file:
            text_file.write(transcription)
        global text

        text = transcription
        #record_button.grid(row=1, column=0, pady=20,) #  sticky="ew") 
        record_button.configure(text="🎤 Record Audio", fg_color="lightblue")
        running = False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while transcribing: {e}\n But yor can find the recorded audio at:{output_directory}")
# Function to select an audio file and transcribe it
def select_audio_file():
    global transcription_box
    transcription_box.delete("1.0", "end")
    file_path = filedialog.askopenfilename(filetypes=[("Model File", "*.pt")])
    if file_path:
        transcribe_audio(file_path)

mload = False

def load_model(model_path):
    global mload, model
    model = whisper.load_model(model_path)
    #mload = True
    messagebox.showinfo("Title", "Model is loaded successfully")
    select_model_button.configure(text ="✔️Change Model", command = select_model)
def select_model():
    global model_path, select_model_button
    model_path = filedialog.askopenfilename(filetypes=[("Model Files", "*.pt")])
    if model_path:
        select_model_button.configure(text = "Loading...", command = None)
        #model = whisper.load_model(model_path)
        threading.Thread(target=load_model , args=(model_path,), daemon=True).start()

# Function to start recording audio
def start_recording():
    global recording, paused, audio_file_path, audio_buffer, button_frame, transcription_box
    recording = True
    paused = False
    audio_buffer = []  # Clear buffer
    #record_button.configure(text="Stop Recording", command=stop_recording, fg_color="red")
    
    transcription_box.delete("1.0", "end")


    record_button.pack_forget()


    button_frame.grid(row=record_button_no, column=0, pady=5 ) #  sticky="ew") 
    sd.sleep(200)
    pause_button.configure(state="normal")  # Enable Pause/Resume button

    # Generate a unique file name for the recording
    file_name = datetime.now().strftime("recording_%Y%m%d_%H%M%S.wav")
    audio_file_path = os.path.join(output_directory, file_name)

    def _record():
        global recording, paused, audio_buffer
        try:
            fs = 48000  # 48 kHz sampling rate
            channels = 1
            dtype = "int16"

            with wave.open(audio_file_path, "wb") as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(2)
                wf.setframerate(fs)

                def callback(indata, frames, time, status):
                    global paused
                    if status:
                        print(f"Recording Error: {status}")
                    
                    if recording:
                        if not paused:
                            wf.writeframes(indata.tobytes())  # Write to file
                        else:
                            audio_buffer.append(indata.copy())  # Store in buffer
                    else:
                        raise sd.CallbackAbort

                with sd.InputStream(samplerate=fs, channels=channels, dtype=dtype, callback=callback):
                    while recording:
                        sd.sleep(100)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while recording: {e}")
        finally:
            button_frame.grid_forget()
            record_button.configure(text="Transcribing...", command=start_recording)
            record_button.grid(row=record_button_no, column=0, pady=5,) #  sticky="ew")
            

    threading.Thread(target=_record, daemon=True).start()

# Function to stop recording
def stop_recording():
    global recording
    recording = False
    sd.stop()
    if os.path.exists(audio_file_path):
        threading.Thread(target=transcribe_audio, args=(audio_file_path,), daemon=True).start()

def pause_recording():
    global paused
    paused = True
    pause_button.configure(text="Resume", text_color="black", command=resume_recording, fg_color="#33cc00")

# Function to resume recording
def resume_recording():
    global paused, audio_buffer
    paused = False
    pause_button.configure(text="Pause", command=pause_recording, fg_color="yellow")

    if audio_buffer:
        # Read existing data
        with wave.open(audio_file_path, "rb") as wf:
            params = wf.getparams()
            existing_frames = wf.readframes(wf.getnframes())

        # Write back existing + buffered frames
        with wave.open(audio_file_path, "wb") as wf:
            wf.setparams(params)
            wf.writeframes(existing_frames)  # Write existing data
            for frame in audio_buffer:
                wf.writeframes(frame.tobytes())  # Append buffered frames

        audio_buffer = []  # Clear buffer after writing


# Function to change the save directory
def change_save_directory():
    global output_directory
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        output_directory = selected_directory
        save_directory_label.configure(text=f"Save Directory: {output_directory}")

# Function to copy text to clipboard
def copy_text():
    global copy_button
    if text:
        pyperclip.copy(text)
        copy_button.configure(text="Text copied!", fg_color="green")
        copy_button.after(3000, restore_copy_button)
    else:
        messagebox.showerror("Error", "No text to copy.")

def restore_copy_button():
    copy_button.configure(text="Copy text to clipboard", fg_color="#8d3560")

# CustomTkinter GUI
ctk.set_appearance_mode("light")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

root = ctk.CTk()
root.title("Wisper Transcriber")
root.geometry("600x550")
root.grid_columnconfigure(0, weight=1)

# Heading
heading_label = ctk.CTkLabel(root, text="Audio Transcriber", font=ctk.CTkFont(size=18, weight="bold"))
heading_label.grid(row=title_no, column=0, pady=20,) #  sticky="ew")

# Save directory display
save_directory_label = ctk.CTkLabel(root, text=f"Save Directory: {output_directory}", text_color="Black", font=ctk.CTkFont(size=12, slant="italic"))
save_directory_label.grid(row=save_directory_label_no, column=0, pady=5,) #  sticky="ew")

# Change save directory button
change_directory_button = ctk.CTkButton(root, text="Change Save Directory", text_color="Black", command=change_save_directory, fg_color="orange")
change_directory_button.grid(row=change_directory_button_no, column=0, pady=5,) #  sticky="ew") 


select_model_button = ctk.CTkButton(root, text="Select Model", text_color="white",command=select_model, fg_color="purple")
select_model_button.grid(row=select_model_no, column=0, pady=5,) #  sticky="ew") 

# Record button
record_button = ctk.CTkButton(root, text="🎤 Record Audio", command=start_recording, text_color="Black", fg_color="lightblue")
record_button.grid(row=record_button_no, column=0, pady=20,) #  sticky="ew") 

#button1.grid(row=0, column=0, padx=10, pady=20)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

button_frame = ctk.CTkFrame(root, fg_color="transparent")
#button_frame.grid(pady=20, padx=20)

pause_button = ctk.CTkButton(button_frame, text="Pause", command= pause_recording, text_color="Black", fg_color="yellow")
pause_button.grid(row=0, column=0, padx=10, pady=0)

stop_button = ctk.CTkButton(button_frame, text="Stop", command=stop_recording, text_color="White", fg_color="#be2200")
stop_button.grid(row=0, column=1, padx=10, pady=0)
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# Choose file button
choose_file_button = ctk.CTkButton(root, text="📂 Choose Audio File", text_color="Black",command=select_audio_file, fg_color="lightgreen")
choose_file_button.grid(row=choose_file_button_no, column=0, pady=5,) #  sticky="ew") 

# Transcription box
transcription_box = ctk.CTkTextbox(root, wrap="word", height=150, width=500)
transcription_box.grid(row=transcription_box_no, column=0, pady=5,) #  sticky="ew") 

# Copy text button
copy_button = ctk.CTkButton(root, text="Copy text to clipboard",text_color="White", command=copy_text, fg_color="#8d3560")
copy_button.grid(row=copy_button_no, column=0, pady=5,) #  sticky="ew") 

# Footer
footer_label = ctk.CTkLabel(root, text="Transcription will automatically be saved as a .txt file.", font=ctk.CTkFont(size=10, slant="italic"))
footer_label.grid(row=footer_label_no, column=0, pady=5,) #  sticky="ew") 

# Run the CustomTkinter event loop
root.mainloop()
