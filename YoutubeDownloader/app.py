import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pytube import YouTube

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube to MP4 Converter')

        self.create_widgets()
    
    def create_widgets(self):
        self.url