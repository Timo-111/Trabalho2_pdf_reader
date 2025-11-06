import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class HolidayCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de Feriados em PDF")
        self.root.geometry("600x450")

        self.pdf_filepath = tk.StringVar()

        #frame principal
        main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        #seleção de arquivo
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=5)

        select_button = ttk.Button(
            file_frame, 
            text="1. Selecionar PDF", 
            command=self.select_pdf_file
        )
        select_button.pack(side=tk.LEFT, padx=(0, 10))

        file_label = ttk.Label(
            file_frame, 
            textvariable=self.pdf_filepath, 
            font=("Arial", 9, "italic"),
            foreground="gray"
        )
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pdf_filepath.set("Nenhum arquivo selecionado...")

        #botão de verificação
        action_button = ttk.Button(
            main_frame, 
            text="2. Verificar Feriados", 
            command=self.process_pdf_and_find_holidays
        )
        action_button.pack(fill=tk.X, pady=10)

        #saída
        results_frame = ttk.LabelFrame(main_frame, text="Feriados Encontrados")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        #scrollbar caso tenham mais datas do que cabe na tela
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL)
        
        self.results_text = tk.Text(
            results_frame, 
            wrap=tk.WORD, 
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.results_text.yview)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def select_pdf_file(self):
        
        #mostrar apenas arquivos .pdf
        filepath = filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*"))
        )
        
        if filepath:
            self.pdf_filepath.set(filepath)
            self.clear_results()
            print(f"Arquivo selecionado: {filepath}")
        else:
            self.pdf_filepath.set("Nenhum arquivo selecionado...")

    def process_pdf_and_find_holidays(self):
        self.clear_results()
        
        filepath = self.pdf_filepath.get()
        if not filepath or not filepath.endswith(".pdf"):
            messagebox.showwarning("Atenção", "Por favor, selecione um arquivo PDF válido.")
            return


        #Back end começo:

        #Back end fim.

    #funçoes auxiliares

    def add_result(self, text_to_add):
        """Adiciona texto à caixa de resultados."""
        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, text_to_add)
        self.results_text.config(state="disabled")
        self.results_text.see(tk.END)

    def clear_results(self):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    
    style = ttk.Style(root)
    style.theme_use('clam') 
    
    app = HolidayCheckerApp(root)
    
    root.mainloop()