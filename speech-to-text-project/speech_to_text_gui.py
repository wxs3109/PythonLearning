#!/usr/bin/env python3
"""
Speech-to-Text GUI Application
A user-friendly interface for speech recognition with start/stop recording.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
import speech_recognition as sr
import os
import wave
import numpy as np
from datetime import datetime
import time
import pyaudio


class SpeechToTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech-to-Text Converter")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio recording
        self.audio_frames = []
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        
        # Recording state
        self.is_recording = False
        self.is_stopping = False
        self.recording_thread = None
        self.timer_thread = None
        self.audio_queue = queue.Queue()
        self.pending_audio = []
        self.audio_buffer = []
        self.processing_finished = False
        
        # Timer variables
        self.timer_duration = 0  # 0 means no timer
        self.timer_start_time = 0
        self.timer_running = False
        
        # Create GUI
        self.create_widgets()
        
        # Adjust for ambient noise on startup
        self.adjust_ambient_noise()
    
    def create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎤 Speech-to-Text Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready to record", 
                                     font=('Arial', 10))
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Timer display
        self.timer_label = ttk.Label(status_frame, text="", font=('Arial', 10, 'bold'))
        self.timer_label.grid(row=0, column=1, sticky=tk.E)
        
        # Timer settings frame
        timer_frame = ttk.LabelFrame(main_frame, text="Timer Settings", padding="10")
        timer_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Timer enable checkbox
        self.timer_enabled_var = tk.BooleanVar(value=False)
        timer_check = ttk.Checkbutton(timer_frame, text="Enable Timer", 
                                     variable=self.timer_enabled_var,
                                     command=self.toggle_timer_settings)
        timer_check.grid(row=0, column=0, padx=(0, 20))
        
        # Timer duration
        ttk.Label(timer_frame, text="Duration (seconds):").grid(row=0, column=1, sticky=tk.W)
        self.timer_duration_var = tk.StringVar(value="60")
        self.timer_spinbox = ttk.Spinbox(timer_frame, from_=10, to=600, 
                                        textvariable=self.timer_duration_var, width=8,
                                        command=self.update_timer_status)
        self.timer_spinbox.grid(row=0, column=2, padx=(10, 20))
        
        # Timer countdown display
        self.countdown_label = ttk.Label(timer_frame, text="", font=('Arial', 12, 'bold'))
        self.countdown_label.grid(row=0, column=3, padx=(20, 0))
        
        # Timer status label
        self.timer_status_label = ttk.Label(timer_frame, text="Timer disabled", font=('Arial', 10))
        self.timer_status_label.grid(row=1, column=0, columnspan=4, pady=(5, 0))
        
        # Initially disable timer settings
        self.toggle_timer_settings()
        
        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=4, pady=(0, 10))
        
        # Start recording button
        self.start_button = ttk.Button(control_frame, text="🎙️ Start Recording", 
                                      command=self.start_recording,
                                      style='Accent.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        # Stop recording button
        self.stop_button = ttk.Button(control_frame, text="⏹️ Stop Recording", 
                                     command=self.stop_recording, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=(0, 10))
        
        # Clear text button
        clear_button = ttk.Button(control_frame, text="🗑️ Clear Text", 
                                 command=self.clear_text)
        clear_button.grid(row=0, column=2, padx=(0, 10))
        
        # Save text button
        save_text_button = ttk.Button(control_frame, text="📝 Save Text", 
                                     command=self.save_text_to_file)
        save_text_button.grid(row=0, column=3, padx=(0, 10))
        
        # Save audio button
        save_audio_button = ttk.Button(control_frame, text="🎵 Save Audio", 
                                      command=self.save_audio_to_file)
        save_audio_button.grid(row=0, column=4, padx=(0, 10))
        
        # Load audio file button
        load_button = ttk.Button(control_frame, text="📁 Load Audio File", 
                                command=self.load_audio_file)
        load_button.grid(row=0, column=5)
        
        # Transcription display
        text_frame = ttk.LabelFrame(main_frame, text="Transcription", padding="10")
        text_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Scrolled text widget for transcription
        self.text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                  font=('Arial', 11), height=15)
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        # Language selection
        ttk.Label(settings_frame, text="Language:").grid(row=0, column=0, sticky=tk.W)
        self.language_var = tk.StringVar(value="en-US")
        language_combo = ttk.Combobox(settings_frame, textvariable=self.language_var, 
                                     values=["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "ja-JP", "ko-KR", "zh-CN"],
                                     width=10)
        language_combo.grid(row=0, column=1, padx=(10, 20))
        
        # Timeout setting
        ttk.Label(settings_frame, text="Timeout (seconds):").grid(row=0, column=2, sticky=tk.W)
        self.timeout_var = tk.StringVar(value="10")
        timeout_spin = ttk.Spinbox(settings_frame, from_=5, to=30, textvariable=self.timeout_var, width=5)
        timeout_spin.grid(row=0, column=3, padx=(10, 20))
        
        # Auto-save checkbox
        self.auto_save_var = tk.BooleanVar(value=True)
        auto_save_check = ttk.Checkbutton(settings_frame, text="Auto-save transcriptions", 
                                         variable=self.auto_save_var)
        auto_save_check.grid(row=0, column=4, padx=(0, 20))
        
        # Auto-save audio checkbox
        self.auto_save_audio_var = tk.BooleanVar(value=True)
        auto_save_audio_check = ttk.Checkbutton(settings_frame, text="Auto-save audio", 
                                               variable=self.auto_save_audio_var)
        auto_save_audio_check.grid(row=0, column=5)
    
    def toggle_timer_settings(self):
        """Enable/disable timer settings based on checkbox."""
        if self.timer_enabled_var.get():
            self.timer_spinbox.config(state='normal')
            duration = self.timer_duration_var.get()
            self.timer_status_label.config(text=f"Timer enabled: {duration} seconds")
        else:
            self.timer_spinbox.config(state='disabled')
            self.countdown_label.config(text="")
            self.timer_status_label.config(text="Timer disabled")
    
    def adjust_ambient_noise(self):
        """Adjust for ambient noise."""
        self.update_status("Adjusting for ambient noise...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.update_status("Ready to record")
        except Exception as e:
            self.update_status(f"Error adjusting noise: {e}")
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def update_timer_display(self, remaining_time):
        """Update timer display."""
        if remaining_time > 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            
            # Color coding based on remaining time
            if remaining_time <= 10:
                # Red for last 10 seconds
                self.countdown_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}", 
                                          foreground="red", font=('Arial', 14, 'bold'))
            elif remaining_time <= 30:
                # Orange for last 30 seconds
                self.countdown_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}", 
                                          foreground="orange", font=('Arial', 12, 'bold'))
            else:
                # Green for normal time
                self.countdown_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}", 
                                          foreground="green", font=('Arial', 12, 'bold'))
        else:
            self.countdown_label.config(text="")
    
    def update_timer_status(self):
        """Update timer status display."""
        if self.timer_enabled_var.get():
            duration = self.timer_duration_var.get()
            self.timer_status_label.config(text=f"Timer enabled: {duration} seconds")
        else:
            self.timer_status_label.config(text="Timer disabled")
    
    def start_recording(self):
        """Start recording audio."""
        if self.is_recording:
            return
        
        # Clear previous audio frames and pending audio
        self.audio_frames = []
        self.pending_audio = []
        
        # Get timer settings
        if self.timer_enabled_var.get():
            try:
                self.timer_duration = int(self.timer_duration_var.get())
                if self.timer_duration <= 0:
                    messagebox.showerror("Error", "Timer duration must be greater than 0")
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid timer duration")
                return
        else:
            self.timer_duration = 0
        
        self.is_recording = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress.start()
        
        # Start timer if enabled
        if self.timer_duration > 0:
            self.timer_start_time = time.time()
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        
        self.update_status("Recording... Speak now!")
        
        # Start recording in a separate thread
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
    
    def run_timer(self):
        """Run the countdown timer."""
        while self.timer_running and self.is_recording:
            elapsed_time = time.time() - self.timer_start_time
            remaining_time = max(0, self.timer_duration - int(elapsed_time))
            
            # Update timer display
            self.root.after(0, lambda: self.update_timer_display(remaining_time))
            
            # Update status with countdown info
            if remaining_time > 0:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                if remaining_time <= 10:
                    self.root.after(0, lambda: self.update_status(f"Recording... ⏰ {minutes:02d}:{seconds:02d} remaining (HURRY!)"))
                elif remaining_time <= 30:
                    self.root.after(0, lambda: self.update_status(f"Recording... ⏰ {minutes:02d}:{seconds:02d} remaining"))
                else:
                    self.root.after(0, lambda: self.update_status(f"Recording... ⏰ {minutes:02d}:{seconds:02d} remaining"))
            
            if remaining_time <= 0:
                # Timer expired, stop recording
                self.root.after(0, lambda: self.update_status("⏰ Timer expired! Stopping recording..."))
                self.root.after(0, self.stop_recording)
                break
            
            time.sleep(1)
        
        # Ensure timer display is cleared
        self.root.after(0, lambda: self.countdown_label.config(text=""))
    
    def stop_recording(self):
        """Stop recording audio immediately but continue processing speech."""
        if not self.is_recording or self.is_stopping:
            return
        
        # Stop recording immediately
        self.is_recording = False
        self.is_stopping = True
        self.timer_running = False
        
        # Update UI immediately
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.countdown_label.config(text="")
        
        self.update_status("⏹️ Recording stopped. Processing remaining speech...")
        
        # Give time for transcription to finish processing remaining audio
        self.root.after(3000, self._complete_stop_recording)
    
    def _complete_stop_recording(self):
        """Complete the stop recording process after processing remaining speech."""
        self.is_stopping = False
        
        self.update_status("✅ Processing complete. Ready to record again.")
        
        # Auto-save if enabled
        if self.auto_save_audio_var.get() and self.audio_frames:
            self.auto_save_audio()
    
    def record_audio(self):
        """Record audio in a separate thread."""
        try:
            # Open audio stream for recording
            stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            # Clear previous audio frames
            self.audio_frames = []
            
            # Start continuous audio recording in a separate thread
            self.continuous_recording_thread = threading.Thread(target=self.continuous_audio_recording, args=(stream,))
            self.continuous_recording_thread.daemon = True
            self.continuous_recording_thread.start()
            
            # Main speech recognition loop
            with self.microphone as source:
                while self.is_recording or self.is_stopping:
                    try:
                        # Listen for audio with timeout
                        timeout = int(self.timeout_var.get())
                        audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
                        
                        if not (self.is_recording or self.is_stopping):
                            break
                        
                        # Add audio to pending queue for processing
                        self.pending_audio.append(audio)
                        
                        # Process the audio for speech recognition
                        self.process_audio(audio)
                        
                    except sr.WaitTimeoutError:
                        if self.is_recording:
                            self.update_status("No speech detected. Still listening...")
                        elif self.is_stopping:
                            # When stopping, try to process any remaining audio
                            self.update_status("Processing remaining speech...")
                            # Give a bit more time for final processing
                            time.sleep(0.5)
                        continue
                    except sr.UnknownValueError:
                        if self.is_recording:
                            self.update_status("Could not understand audio. Still listening...")
                        elif self.is_stopping:
                            self.update_status("Processing remaining speech...")
                        continue
                    except Exception as e:
                        if self.is_recording or self.is_stopping:
                            self.update_status(f"Error: {e}")
                        break
            
            # When stopping, give extra time for final speech processing
            if self.is_stopping:
                self.update_status("Finalizing speech processing...")
                # Process any remaining pending audio
                for audio in self.pending_audio:
                    try:
                        self.process_audio(audio)
                    except:
                        pass
                self.pending_audio.clear()
                
                # Try to capture and process any remaining audio from the microphone
                self.process_remaining_audio_from_microphone()
                time.sleep(2)  # Give 2 seconds for final processing
            
            # Wait for the continuous recording to finish
            if hasattr(self, 'continuous_recording_thread') and self.continuous_recording_thread.is_alive():
                self.continuous_recording_thread.join(timeout=2)
            
            # Close the stream
            stream.stop_stream()
            stream.close()
                        
        except Exception as e:
            self.update_status(f"Recording error: {e}")
        finally:
            # Ensure UI is updated when recording stops
            self.root.after(0, self.recording_finished)
    
    def continuous_audio_recording(self, stream):
        """Continuously record audio data while recording is active."""
        try:
            while self.is_recording:
                # Read audio data in chunks
                data = stream.read(self.chunk, exception_on_overflow=False)
                self.audio_frames.append(data)
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.01)
            
            # Add a small buffer after stopping to capture any final audio
            # Only if we're still processing speech
            if self.is_stopping:
                buffer_time = 0.3  # 300ms buffer
                buffer_chunks = int(buffer_time * self.rate / self.chunk)
                
                for _ in range(buffer_chunks):
                    try:
                        data = stream.read(self.chunk, exception_on_overflow=False)
                        self.audio_frames.append(data)
                    except:
                        break
                    
        except Exception as e:
            print(f"Continuous recording error: {e}")
    
    def recording_finished(self):
        """Called when recording thread finishes."""
        self.is_recording = False
        self.timer_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.progress.stop()
        self.update_status("Ready to record")
    
    def process_audio(self, audio):
        """Process recorded audio and convert to text."""
        try:
            # Get language setting
            language = self.language_var.get()
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=language)
            
            if text.strip():
                # Add timestamp
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_text = f"[{timestamp}] {text}\n\n"
                
                # Update text area in main thread
                self.root.after(0, lambda: self.add_text(formatted_text))
                
                # Auto-save if enabled
                if self.auto_save_var.get():
                    self.root.after(0, self.auto_save_transcription)
                
                if self.is_stopping:
                    self.update_status("Processing remaining speech...")
                else:
                    self.update_status("Speech recognized! Still listening...")
            else:
                if self.is_stopping:
                    self.update_status("Processing remaining speech...")
                else:
                    self.update_status("Empty transcription. Still listening...")
                
        except sr.UnknownValueError:
            if self.is_stopping:
                self.update_status("Processing remaining speech...")
            else:
                self.update_status("Could not understand audio. Still listening...")
        except sr.RequestError as e:
            self.update_status(f"API error: {e}")
        except Exception as e:
            self.update_status(f"Processing error: {e}")
    
    def process_remaining_audio_from_microphone(self):
        """Try to capture and process any remaining audio from the microphone."""
        try:
            with self.microphone as source:
                # Try to listen for any remaining audio with a shorter timeout
                for attempt in range(3):  # Try up to 3 times
                    try:
                        self.update_status(f"Processing remaining audio (attempt {attempt + 1}/3)...")
                        audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=10)
                        self.process_audio(audio)
                        time.sleep(0.5)  # Small delay between attempts
                    except sr.WaitTimeoutError:
                        break  # No more audio to process
                    except sr.UnknownValueError:
                        continue  # Try again
                    except Exception:
                        break  # Stop on other errors
        except Exception as e:
            print(f"Error processing remaining audio: {e}")
    
    def add_text(self, text):
        """Add text to the text area."""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
    
    def clear_text(self):
        """Clear the text area."""
        self.text_area.delete(1.0, tk.END)
        self.audio_frames = []
        self.update_status("Text and audio cleared")
    
    def save_text_to_file(self):
        """Save transcription to a file."""
        try:
            text = self.text_area.get(1.0, tk.END).strip()
            if not text:
                messagebox.showwarning("Warning", "No text to save!")
                return
            
            # Get filename from user
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save Transcription"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.update_status(f"Text saved to: {filename}")
                messagebox.showinfo("Success", f"Transcription saved to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save text file: {e}")
    
    def save_audio_to_file(self):
        """Save recorded audio to a WAV file."""
        try:
            if not self.audio_frames:
                messagebox.showwarning("Warning", "No audio recorded!")
                return
            
            # Get filename from user
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
                title="Save Audio Recording"
            )
            
            if filename:
                # Save audio as WAV file
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
                    wf.setframerate(self.rate)
                    wf.writeframes(b''.join(self.audio_frames))
                
                self.update_status(f"Audio saved to: {filename}")
                messagebox.showinfo("Success", f"Audio recording saved to:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save audio file: {e}")
    
    def auto_save_transcription(self):
        """Auto-save transcription to a timestamped file."""
        try:
            text = self.text_area.get(1.0, tk.END).strip()
            if text:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"transcription_{timestamp}.txt"
                
                # Create transcriptions directory if it doesn't exist
                os.makedirs("transcriptions", exist_ok=True)
                filepath = os.path.join("transcriptions", filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
        except Exception as e:
            print(f"Auto-save error: {e}")
    
    def auto_save_audio(self):
        """Auto-save audio to a timestamped file."""
        try:
            if self.audio_frames:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"audio_{timestamp}.wav"
                
                # Create audio directory if it doesn't exist
                os.makedirs("audio_recordings", exist_ok=True)
                filepath = os.path.join("audio_recordings", filename)
                
                # Save audio as WAV file
                with wave.open(filepath, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
                    wf.setframerate(self.rate)
                    wf.writeframes(b''.join(self.audio_frames))
                    
        except Exception as e:
            print(f"Auto-save audio error: {e}")
    
    def load_audio_file(self):
        """Load and transcribe an audio file."""
        try:
            filename = filedialog.askopenfilename(
                title="Select Audio File",
                filetypes=[
                    ("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a *.aac"),
                    ("WAV files", "*.wav"),
                    ("MP3 files", "*.mp3"),
                    ("All files", "*.*")
                ]
            )
            
            if filename:
                self.update_status(f"Processing audio file: {os.path.basename(filename)}")
                self.progress.start()
                
                # Process file in a separate thread
                threading.Thread(target=self.process_audio_file, args=(filename,), daemon=True).start()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def process_audio_file(self, filename):
        """Process audio file in a separate thread."""
        try:
            with sr.AudioFile(filename) as source:
                audio = self.recognizer.record(source)
            
            # Get language setting
            language = self.language_var.get()
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=language)
            
            if text.strip():
                # Add file info and transcription
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_text = f"[{timestamp}] File: {os.path.basename(filename)}\n{text}\n\n"
                
                # Update UI in main thread
                self.root.after(0, lambda: self.add_text(formatted_text))
                self.root.after(0, lambda: self.update_status(f"File transcribed: {os.path.basename(filename)}"))
                
                # Auto-save if enabled
                if self.auto_save_var.get():
                    self.root.after(0, self.auto_save_transcription)
            else:
                self.root.after(0, lambda: self.update_status("No speech detected in file"))
                
        except sr.UnknownValueError:
            self.root.after(0, lambda: self.update_status("Could not understand audio in file"))
        except sr.RequestError as e:
            self.root.after(0, lambda: self.update_status(f"API error: {e}"))
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"File processing error: {e}"))
        finally:
            self.root.after(0, self.progress.stop)
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        if hasattr(self, 'audio'):
            self.audio.terminate()


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Create and run the application
    app = SpeechToTextGUI(root)
    
    # Handle window closing
    def on_closing():
        if app.is_recording:
            app.stop_recording()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main() 