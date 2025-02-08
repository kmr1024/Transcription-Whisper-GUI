# Transcription-Whisper-GUI
A simple transcription GUI with Python and Customtkinter module
1) Functionality:
   Choice for selecting the AI-models for transcription
   Record audio and provide transcribed text
   features:
       Record/Pause Functionality
       Recordings are saved as files for future transcription
   Transcribe From an audio file

   All transcribed text will be saves as text

# **Whisper App – GUI Version**  

Whisper App is a simple GUI-based tool for recording and transcribing audio using OpenAI's Whisper model. Follow the steps below to install and run the application.  

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
_(Note: This folder may be hidden. You can enable "Show Hidden Files" in Windows Explorer to view it.)_  

### **Step 3: Run the Application**  
Execute the GUI application by running:  
```sh
python whisper_app.py
```

### **Step 4: Transcribe Audio**  
- Select a model file from the folder found in **Step 2** (`.cache/whisper/` directory).  
- Use the **Record Audio** button to capture audio. The recorded file will be saved in the chosen directory.  
- Alternatively, you can **select an existing audio file** to transcribe.  

✅ **That's it! Your transcription will be displayed in the app.**  

