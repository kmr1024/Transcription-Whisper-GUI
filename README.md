# **Whisper App – GUI Version**  

A simple transcription GUI built with **Python** and **CustomTkinter**, integrating OpenAI’s Whisper model for high-quality speech-to-text conversion.  

## **Features**  

✔ **AI Model Selection** – Choose from different Whisper models for transcription.  
✔ **Record & Transcribe** – Record audio and get real-time transcription.  
✔ **Pause & Resume** – Pause and resume recordings seamlessly.  
✔ **Save Recordings** – Audio files are saved for future transcription.  
✔ **Transcribe Existing Audio** – Upload and transcribe pre-recorded audio files.  
✔ **Auto-Save Transcriptions** – All transcribed text is saved for later use.  

## **Installation and Setup**  

### **Step 1: Install Necessary Modules**  
Ensure you have Python installed, then run the following command in the terminal or command prompt:  

```sh
pip install os time openai-whisper customtkinter sounddevice wave pydub pyperclip
```
_(This will install only the missing dependencies.)_  

### **Step 2: Download the Whisper Model**  
In a Python environment, run the following lines to download the required model:  

```python
import whisper
model = whisper.load_model("medium")
```  

By default, this will download the model file **`medium.pt`** to:  
📂 `C:/Users/<your_name>/.cache/whisper/`  
_(Note: This folder may be hidden. Enable "Show Hidden Files" in Windows Explorer to access it.)_  

### **Step 3: Run the Application**  
Execute the GUI application by running:  
```sh
python whisper_app.py
```

### **Step 4: Transcribe Audio**  
- Select a Whisper model from the **Step 2** folder (`.cache/whisper/`).  
- Use the **Record Audio** button to start recording.  
- **Pause/Resume** functionality allows flexible recording control.  
- Audio recordings are saved for future transcription.  
- Select an **existing audio file** to transcribe.  
- All transcribed text is **automatically saved** for later use.  

✅ **That's it! Your transcription will be displayed in the app.**  
