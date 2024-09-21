import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from datetime import datetime

class EditorImmagini:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor di Immagini per Digital Forensics")
        #self.root.iconbitmap("./icona.ico")

        # Variabili per l'immagine
        self.immagine_originale = None
        self.immagine_processata = None
        self.immagine_anteprima = None

        # Creazione dell'interfaccia (pulsanti e slider con relativa impostazione in grid)
        self.interfaccia()

    def interfaccia(self):
       # Frame per caricamento immagine
        load_frame = ttk.LabelFrame(self.root, text="Caricamento Immagine", padding=10)
        load_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        # Pulsante per caricare l'immagine
        load_button = tk.Button(load_frame, text="Carica Immagine", command=self.carica_immagine)
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        # Pulsante per reset
        reset_button = tk.Button(load_frame, text="Reset", command=self.reset_immagine)
        reset_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame per filtro Laplaciano
        laplacian_frame = ttk.LabelFrame(self.root, text="Filtro Laplaciano", padding=10)
        laplacian_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        # Pulsante per applicare il filtro Laplaciano
        laplacian_button = tk.Button(laplacian_frame, text="Applica Filtro Laplaciano", command=self.filtro_laplaciano)
        laplacian_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame per contrasto e luminosità
        contrast_brightness_frame = ttk.LabelFrame(self.root, text="Contrasto e Luminosità", padding=10)
        contrast_brightness_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        # Slider per contrasto
        contrast_label = tk.Label(contrast_brightness_frame, text="Contrasto:")
        contrast_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.contrast_slider = tk.Scale(contrast_brightness_frame, from_=0, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_slider.set(1.0)  # Valore di default
        self.contrast_slider.pack(side=tk.LEFT, padx=5, pady=5)
        # Slider per luminosità
        brightness_label = tk.Label(contrast_brightness_frame, text="Luminosità:")
        brightness_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.brightness_slider = tk.Scale(contrast_brightness_frame, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.brightness_slider.set(0)  # Valore di default
        self.brightness_slider.pack(side=tk.LEFT, padx=5, pady=5)
        # Pulsante per applicare contrasto e luminosità
        contrast_brightness_button = tk.Button(contrast_brightness_frame, text="Applica", command=self.filtro_contrasto_luminosita_cv)
        contrast_brightness_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Frame per salvataggio immagine
        save_frame = ttk.LabelFrame(self.root, text="Salvataggio Immagine", padding=10)
        save_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        # Slider per Quality Factor
        qf_label = tk.Label(save_frame, text="Quality Factor (QF):")
        qf_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.qf_slider = tk.Scale(save_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.qf_slider.set(100)  # Valore di default
        self.qf_slider.pack(side=tk.LEFT, padx=5, pady=5)
        # Pulsante per salvare l'immagine
        save_button = tk.Button(save_frame, text="Salva Immagine", command=self.salva_immagine)
        save_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Area per visualizzare l'anteprima dell'immagine
        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Frame per il log delle operazioni
        log_frame = ttk.LabelFrame(self.root, text="Log Operazioni", padding=10)
        log_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Text box per visualizzare il log
        self.log_text = tk.Text(log_frame, width=50, height=20)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Pulsante per salvare il log come file
        save_log_button = tk.Button(log_frame, text="Salva Log", command=self.salva_log)
        save_log_button.pack(pady=5)

    # Funzione per il caricamento dell'immagine 
    def carica_immagine(self):
        percorso_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if percorso_file:
            immagine = cv2.imread(percorso_file)
            if immagine is None:
                messagebox.showerror("Errore", "Impossibile caricare l'immagine.")
                return
            self.immagine_originale = immagine
            self.immagine_processata = immagine.copy()
            self.mostra_anteprima(self.immagine_processata)
            self.scrivi_log(f"Immagine caricata da {percorso_file}")

    # Utilizzo di PIL per mostrare l'anteprima dell'immagine dentro Tkinter
    def mostra_anteprima(self, immagine):
        immagine_rgb = cv2.cvtColor(immagine, cv2.COLOR_BGR2RGB) # OpenCV utilizza la codifica BGR invece della RGB
        immagine_pil = Image.fromarray(immagine_rgb)
        immagine_pil = self.ridimensiona_immagine(immagine_pil, max_size=(800, 600)) # L'immagine è ridimensionata per evitare che fuoriesca dalla schermata del programma
        self.immagine_anteprima = ImageTk.PhotoImage(immagine_pil)
        self.image_label.config(image=self.immagine_anteprima)

    # Funzione per il resize dell'anteprima dell'immagine
    def ridimensiona_immagine(self, immagine_pil, max_size=(800, 600)):
        immagine_pil.thumbnail(max_size, Image.Resampling.LANCZOS)
        return immagine_pil

    # Funzione per scrivere nel log
    def scrivi_log(self, messaggio):
        self.log_text.config(state=tk.NORMAL)
        orario_corrente = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"->[{orario_corrente}] - {messaggio}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    # Funzione per l'applicazione del filtro laplaciano
    # https://docs.opencv.org/4.x/d5/db5/tutorial_laplace_operator.html
    def filtro_laplaciano(self):
        if self.immagine_processata is None:
            messagebox.showwarning("Avviso", "Caricare un'immagine prima di applicare il filtro.")
            self.scrivi_log("Errore: nessuna immagine caricata su cui applicare il filtro Laplaciano.")
            return
        immagine_grigio = cv2.cvtColor(self.immagine_processata, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(immagine_grigio, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        laplacian_bgr = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)
        self.immagine_processata = laplacian_bgr
        self.mostra_anteprima(self.immagine_processata)
        self.scrivi_log("Filtro Laplaciano applicato.")

    # Funzione per la modifica di contrasto e luminosità
    # L'idea di base è la stessa, andare a modificare il pixel come pixel = pixel * contrasto + luminosità
    # Nella seconda implementazione viene usata la libreria openCV
    def filtro_contrasto_luminosita(self, event=None):
        if self.immagine_processata is None:
            messagebox.showwarning("Avviso", "Caricare un'immagine prima di regolare contrasto e luminosità.")
            self.scrivi_log("Errore: nessuna immagine caricata su cui modificare contrasto e luminosità.")
            return
        contrasto = self.contrast_slider.get()
        luminosita = self.brightness_slider.get()
        image = self.immagine_processata.astype(np.float32)
        # Applico contrasto e luminosità
        image = image * contrasto + luminosita
        # Controllo che i valori siano compresi tra 0 e 255 per rispettare la codifica a 8 bit per pixel
        image = np.clip(image, 0, 255)
        # Riconverto a uint8
        self.immagine_processata = image.astype(np.uint8)
        self.mostra_anteprima(self.immagine_processata)
        self.scrivi_log(f"Applicati contrasto ({contrasto}) e luminosità ({luminosita}).")
        self.brightness_slider.set(0)  # Ripristino al valore di default
        self.contrast_slider.set(1.0)  # Ripristino al valore di default

    # https://www.geeksforgeeks.org/image-enhancement-techniques-using-opencv-python/
    def filtro_contrasto_luminosita_cv(self):
        if self.immagine_processata is None:
            messagebox.showwarning("Avviso", "Caricare un'immagine prima di regolare contrasto e luminosità.")
            self.scrivi_log("Errore: nessuna immagine caricata su cui modificare contrasto e luminosità.")
            return
        contrasto = self.contrast_slider.get()
        luminosita = self.brightness_slider.get()
        # Applico la modifica del contrasto e luminosità
        self.immagine_processata = cv2.convertScaleAbs(self.immagine_processata, alpha=contrasto, beta=luminosita)
        # Aggiorno l'immagine processata e mostra l'anteprima
        self.mostra_anteprima(self.immagine_processata)
        self.scrivi_log(f"Applicati contrasto ({contrasto}) e luminosità ({luminosita}).")
        self.brightness_slider.set(0)  # Ripristino al valore di default
        self.contrast_slider.set(1.0)  # Ripristino al valore di default

    
    # Funzione per il salvataggio dell'immagine
    #https://www.geeksforgeeks.org/python-opencv-cv2-imwrite-method/
    def salva_immagine(self):
        percorso_file = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
        if percorso_file:
            qf = self.qf_slider.get()
            cv2.imwrite(percorso_file, self.immagine_processata, [cv2.IMWRITE_JPEG_QUALITY, qf])
            self.scrivi_log(f"Immagine salvata in: {percorso_file}, Quality Factor: {qf}")


    def reset_immagine(self):
        if self.immagine_originale is None:
            messagebox.showwarning("Avviso", "Nessuna immagine da ripristinare.")
            self.scrivi_log("Errore: nessuna immagine da ripristinare.")
            return
        # Ripristino l'immagine originale e i vari slider
        self.immagine_processata = self.immagine_originale.copy()
        self.mostra_anteprima(self.immagine_processata)
        self.scrivi_log("Immagine ripristinata allo stato originale.")
        self.brightness_slider.set(0)  # Ripristino al valore di default
        self.contrast_slider.set(1.0)  # Ripristino al valore di default
        # Ripristino il log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    # Funzione per salvare il log come file .txt
    def salva_log(self):
        percorso_log = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if percorso_log:
            try:
                with open(percorso_log, "w") as file_log:
                    self.scrivi_log(f"Log salvato in {percorso_log}.")
                    contenuto_log = self.log_text.get(1.0, tk.END)
                    file_log.write(contenuto_log)
                
            except Exception as e:
                self.scrivi_log(f"Errore nel salvataggio del log: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EditorImmagini(root)
    root.mainloop()