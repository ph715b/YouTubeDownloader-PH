import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from pytube import YouTube

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube to MP4 Converter')

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choose a built-in theme like 'clam', 'default', 'vista'

        self.create_widgets()

    def create_widgets(self):
        self.create_url_section()
        self.create_path_section()
        self.create_buttons()

    def create_url_section(self):
        self.url_label = ttk.Label(self.root, text='Enter YouTube URL:')
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(self.root, width=40)
        self.url_entry.pack()

    def create_path_section(self):
        self.path_label = ttk.Label(self.root, text='Select Path:')
        self.path_label.pack(pady=5)

        self.path_entry = ttk.Entry(self.root, width=40)
        self.path_entry.pack()

        self.browse_button = ttk.Button(self.root, text='Browse', command=self.browse_path)
        self.browse_button.pack(pady=5)
    
    def create_buttons(self):
        self.download_button = ttk.Button(self.root, text='Download', command=self.download_video)
        self.download_button.pack(pady=10)

    def browse_path(self):
        chosen_path = filedialog.askdirectory()
        if chosen_path:
            self.path_entry.delete(0, tk.END)  # Clear previous path
            self.path_entry.insert(0, chosen_path)

    def download_video(self):
        url = self.url_entry.get()
        download_path = self.path_entry.get()

        if not download_path:
            download_path = 'downloads'

        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()

            if not os.path.exists(download_path):
                os.makedirs(download_path)

            #Performing the download in a separate thread
            download_thread = Thread(target=self.download_video_thread, args=(video, download_path))
            download_thread.start()
        except Exception as e:
            messagebox.showerror('Error', f'An error occured: {e}')

    def download_video_thread(self, video, download_path):
        try:
            video.download(output_path=download_path)
            self.root.after(0, lambda: messagebox.showinfo('Success', 'Video downloaded successfully!'))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror('Error', f'An error occurred: {e}'))

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
