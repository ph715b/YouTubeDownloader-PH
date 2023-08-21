import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
from ttkthemes import ThemedStyle

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title('YouTube to MP4 Converter')
        self.root.configure(bg = '#1E1E1E')
        # self.style.set_theme('clam')  # Choose a built-in theme like 'clam', 'default', 'vista'

        self.create_widgets()
        self.video_links = []

    def create_widgets(self):
        self.create_url_section()
        self.create_path_section()
        self.create_buttons()

    def create_url_section(self):
        self.url_label = ttk.Label(self.root, text='Enter YouTube URL:', foreground = 'white', background = '#1E1E1E')
        self.url_label.pack(pady=10)

        self.url_entry = ttk.Entry(self.root, width=40)
        self.url_entry.pack()

    def create_path_section(self):
        self.path_label = ttk.Label(self.root, text='Select Path:', foreground = 'white', background = '#1E1E1E')
        self.path_label.pack(pady=5)

        self.path_entry = ttk.Entry(self.root, width=40)
        self.path_entry.pack()

        self.browse_button = ttk.Button(self.root, text='Browse', command=self.browse_path)
        self.browse_button.pack(pady=5)
    
    def create_buttons(self):
        self.download_button = ttk.Button(self.root, text='Download', command=self.download_videos)
        self.download_button.pack(pady=10)

    def browse_path(self):
        chosen_path = filedialog.askdirectory()
        if chosen_path:
            self.path_entry.delete(0, tk.END)  # Clear previous path
            self.path_entry.insert(0, chosen_path)

    def download_videos(self):
        urls = self.url_entry.get()
        download_path = self.path_entry.get()

        if not download_path:
            download_path = 'downloads'

        self.video_links = [url.strip() for url in urls.split(',')]

        if not self.video_links:
            messagebox.showerror('Error', 'No valid URLs entered.')
            return

        successful_downloads = 0
    
        def download_thread(url):
            nonlocal successful_downloads
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()

                if not os.path.exists(download_path):
                    os.makedirs(download_path)

                    video.download(output_path=download_path)
                successful_downloads += 1
            except Exception as e:
                error_messages.append(f"Error downloading {url}: {e}")

            if successful_downloads > 0:
                messagebox.showinfo('Success', f'{successful_downloads} video(s) downloaded successfully!')
            else:
                messagebox.showerror('Error', 'No videos could be downloaded.')

        error_messages = []
        threads = []

        for url in self.video_links:
            thread = threading.Thread(target=download_thread, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for error_message in error_messages:
            messagebox.showerror('Error', error_message)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
