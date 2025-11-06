import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import sys
import re
import requests
import fitz

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

        self.action_button = ttk.Button(
            main_frame, 
            text="2. Verificar Feriados", 
            command=self.process_pdf_and_find_holidays
        )
        self.action_button.pack(fill=tk.X, pady=10)

        #saída
        results_frame = ttk.LabelFrame(main_frame, text="Feriados Encontrados")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        #scrollbar
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
        else:
            self.pdf_filepath.set("Nenhum arquivo selecionado...")
            
    def process_pdf_and_find_holidays(self):
        self.clear_results() #esta chamada foi mantida
        
        filepath = self.pdf_filepath.get()
        if not filepath or not filepath.endswith(".pdf"):
            messagebox.showwarning("Atenção", "Por favor, selecione um arquivo PDF válido.")
            return

        self.clear_results()
        self.add_result("Iniciando processamento... A interface pode travar.\n")
        self.action_button.config(state="disabled", text="Processando...")
        self.root.update_idletasks() 

        try:
            self.add_result("Extraindo texto do PDF...\n")
            
            all_text = ""
            with fitz.open(filepath) as doc:
                for page in doc:
                    all_text += page.get_text()
            
            date_regex = r'\d{4}-\d{2}-\d{2}'
            dates_in_pdf = set(re.findall(date_regex, all_text))

            if not dates_in_pdf:
                self.add_result("Nenhuma data (YYYY-MM-DD) encontrada no PDF.\n")
                return

            self.add_result(f"Encontradas {len(dates_in_pdf)} datas únicas no PDF.\n")

            years_in_pdf = sorted(list(set([date.split('-')[0] for date in dates_in_pdf])))
            
            api_holidays = {} 

            for year in years_in_pdf:
                self.add_result(f"Consultando API de feriados para o ano {year}...\n")
                try:
                    api_url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/BR"
                    response = requests.get(api_url, timeout=10) 
                    response.raise_for_status() 
                    
                    holidays_data = response.json()
                    for holiday in holidays_data:
                        api_holidays[holiday['date']] = holiday['localName']

                except requests.exceptions.RequestException as e:
                    raise Exception(f"Falha ao consultar API para o ano {year}. Erro: {e}")

            self.add_result("Comparando datas...\n")

            found_holidays = []
            for pdf_date in sorted(list(dates_in_pdf)): 
                if pdf_date in api_holidays:
                    holiday_name = api_holidays[pdf_date]
                    found_holidays.append((pdf_date, holiday_name))
            
            self.add_result("\n--- Processamento Concluído ---\n")
            if not found_holidays:
                self.add_result("Nenhum feriado encontrado nas datas do PDF.\n")
            else:
                self.add_result(f"Total de {len(found_holidays)} feriados encontrados:\n")
                for date, name in found_holidays:
                    self.add_result(f"  - {date}: {name}\n")

        except Exception as e:
            self.add_result(f"\nERRO: {str(e)}\n")
            messagebox.showerror("Erro no Processamento", str(e))
        
        finally:
            self.action_button.config(state="normal", text="2. Verificar Feriados")

    def add_result(self, text_to_add):
        """Adiciona texto na caixa de resultado"""
        self.results_text.config(state="normal")
        self.results_text.insert(tk.END, text_to_add)
        self.results_text.config(state="disabled")
        self.results_text.see(tk.END) 
        self.root.update_idletasks() 

    def clear_results(self):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state="disabled")
        self.root.update_idletasks() 


def main_app():
    root = tk.Tk()
    
    style = ttk.Style(root)
    style.theme_use('clam') 
    
    app = HolidayCheckerApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main_app()