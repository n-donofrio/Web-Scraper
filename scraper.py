import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from bs4 import BeautifulSoup
import requests
from nltk import FreqDist, word_tokenize
import nltk
nltk.download('punkt')  # Download the punkt tokenizer data

class WebScrapingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Web Scraping Tool")
        self.root.geometry("800x500")
        self.root.configure(bg="#282c34")

        # Style Configuration
        style = ttk.Style()
        style.configure("TFrame", background="#282c34")
        style.configure("TLabel", background="#282c34", foreground="#61dafb")
        style.configure("TButton", background="#61dafb", foreground="#282c34", padding=(10, 5))
        style.configure("TEntry", fieldbackground="#61dafb", foreground="#282c34")
        style.configure("TScrollbar", troughcolor="#282c34", bordercolor="#282c34", arrowcolor="#61dafb", darkcolor="#61dafb", lightcolor="#61dafb")

        # Frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.configure(style="TFrame")

        # URL Entry
        self.url_label = ttk.Label(self.main_frame, text="Enter URL(s) separated by commas:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.url_entry = ttk.Entry(self.main_frame, width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Scrolled Text for Result
        self.result_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=60, height=10)
        self.result_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Buttons
        self.scrape_button = ttk.Button(self.main_frame, text="Scrape", command=self.scrape_data)
        self.scrape_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.save_button = ttk.Button(self.main_frame, text="Save to File", command=self.save_to_file)
        self.save_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.analyze_button = ttk.Button(self.main_frame, text="Analyze Text", command=self.analyze_text)
        self.analyze_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    def scrape_data(self):
        urls = [url.strip() for url in self.url_entry.get().split(',')]
        self.result_text.delete(1.0, tk.END)

        for url in urls:
            if not url:
                continue

            try:
                response = requests.get(url)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                extracted_data = soup.get_text()

                self.result_text.insert(tk.END, f"Scraped Data from {url}:\n{extracted_data}\n{'='*50}\n")

            except requests.exceptions.RequestException as e:
                self.result_text.insert(tk.END, f"Error for {url}: {e}\n{'='*50}\n")

    def save_to_file(self):
        data_to_save = self.result_text.get(1.0, tk.END)
        if not data_to_save.strip():
            messagebox.showwarning("No Data", "No scraped data to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        if file_path:
            with open(file_path, 'w') as file:
                file.write(data_to_save)
            messagebox.showinfo("Save Successful", "Scraped data saved to file.")

    def analyze_text(self):
        data_to_analyze = self.result_text.get(1.0, tk.END)
        if not data_to_analyze.strip():
            messagebox.showwarning("No Data", "No data to analyze.")
            return

        # Tokenize words
        words = word_tokenize(data_to_analyze)

        # Calculate word frequency
        word_freq = FreqDist(words)

        # Display analysis results
        analysis_result = "Top 10 Most Common Words:\n"
        for word, freq in word_freq.most_common(10):
            analysis_result += f"{word}: {freq}\n"

        messagebox.showinfo("Text Analysis", analysis_result)

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = WebScrapingTool(root)
    root.mainloop()
