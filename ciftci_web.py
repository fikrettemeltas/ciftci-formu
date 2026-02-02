import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

# --- MÜHENDİSLİK VERİTABANI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Yonca": {"aralik": 12, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yağmurlama"},
    "Arpa": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

def boru_hesapla():
    try:
        alan = float(entry_alan.get())
        urun = var_urun_liste.get()
        v = BITKI_VERILERI[urun]
        sabit_debi = 72 # 20 L/s = 72 m3/h
        
        if v["tip"] == "Damlama":
            metraj = (1000 / v["aralik"]) * alan
            birim = f"{metraj:,.0f} Metre Damlama Borusu"
        else:
            tabanca = (alan * 1000) / 144
            birim = f"{tabanca:,.0f} Adet Yağmurlama Tabancası"

        gunluk_su = alan * v["su_ihtiyac"]
        sure = gunluk_su / sabit_debi

        rapor = (f"--- TEKNIK ANALIZ ---\n"
                 f"Urun: {urun}\n"
                 f"Ihtiyac: {birim}\n"
                 f"Ana Boru: 110 mm\n"
                 f"Gunluk Su: {gunluk_su:.1f} Ton\n"
                 f"Sulama Suresi: {sure:.1f} Saat\n")
        return rapor
    except:
        return "Lutfen alan bilgisini rakam giriniz."

def whatsapp_gonder():
    isim = entry_isim.get()
    ilce = entry_ilce.get()
    alan = entry_alan.get()
    urun = var_urun_liste.get()
    
    if not isim or not ilce or not alan:
        messagebox.showwarning("Uyari", "Lutfen tum bilgileri doldurun!")
        return

    teknik_not = boru_hesapla()
    # Mesajın başına ve sonuna ismini ekledik
    mesaj = (f"Sayin AHMET FIKRET TEMELTAS,\n\n"
             f"Ben {isim}. {ilce} bolgesindeki {alan} donum {urun} arazim icin teknik destek istiyorum.\n\n"
             f"{teknik_not}\n"
             f"Software Developed by AHMET FIKRET TEMELTAS")
    
    url = f"https://wa.me/905075031990?text={mesaj}"
    webbrowser.open(url)

def belge_sec(belge_turu):
    yol = filedialog.askopenfilename()
    if yol:
        messagebox.showinfo("Basarili", f"{belge_turu} sisteme tanimlandi.")

# --- ARAYUZ ---
root = tk.Tk()
root.title("Ahmet Fikret Temeltas - Sulama Sistemleri")
root.geometry("450x850")

# BASLIK - Emoji kaldırıldı (Hata vermemesi için)
tk.Label(root, text="PROJE GELISTIRICI", font=("Arial", 10, "italic")).pack(pady=2)
tk.Label(root, text="AHMET FIKRET TEMELTAS", font=("Arial", 14, "bold"), fg="#1B5E20").pack(pady=5)

# GIRISLER
tk.Label(root, text="Ciftci Ad Soyad:").pack()
entry_isim = tk.Entry(root, width=40); entry_isim.pack(pady=2)

tk.Label(root, text="Ilce / Koy:").pack()
entry_ilce = tk.Entry(root, width=40); entry_ilce.pack(pady=2)

tk.Label(root, text="Ada No:").pack()
entry_ada = tk.Entry(root, width=40); entry_ada.pack(pady=2)

tk.Label(root, text="Parsel No:").pack()
entry_parsel = tk.Entry(root, width=40); entry_parsel.pack(pady=2)

tk.Label(root, text="\nUrun Secimi:", font=("Arial", 10, "bold")).pack()
var_urun_liste = tk.StringVar(root); var_urun_liste.set("Mısır")
tk.OptionMenu(root, var_urun_liste, *BITKI_VERILERI.keys()).pack()

tk.Label(root, text="Tarla Alani (Donum):").pack()
entry_alan = tk.Entry(root, width=20); entry_alan.pack()

# BELGELER
tk.Label(root, text="\nBELGE YONETIMI", font=("Arial", 10, "bold")).pack()
btn_f = tk.Frame(root); btn_f.pack()
for b in ["CKS", "Ruhsat", "Tapu"]:
    tk.Button(btn_f, text=b, width=10, command=lambda x=b: belge_sec(x)).pack(side=tk.LEFT, padx=2)

# AKSIYON BUTONLARI
tk.Button(root, text="TEKNIK RAPORU GOSTER", bg="#E67E22", fg="white", 
          command=lambda: messagebox.showinfo("Rapor", boru_hesapla())).pack(pady=15)

tk.Button(root, text="WHATSAPP'A GONDER", bg="#25D366", fg="white", 
          font=("Arial", 11, "bold"), height=2, command=whatsapp_gonder).pack(pady=10)

# ALT IMZA
tk.Label(root, text="\n" + "_"*40).pack()
tk.Label(root, text="Copyright 2026 Software Developed by Ahmet Fikret Temeltas", font=("Arial", 8)).pack(pady=10)

root.mainloop()

