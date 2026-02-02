# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

# --- MUHENDISLIK VERITABANI ---
BITKI_VERILERI = {
    "Misir": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Aycicegi": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Yonca": {"aralik": 12, "su_ihtiyac": 9, "tip": "Yagmurlama"},
    "Bugday": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yagmurlama"},
    "Arpa": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yagmurlama"}
}

def boru_hesapla():
    try:
        alan_metin = entry_alan.get()
        if not alan_metin:
            return "Alan girilmedi."
        alan = float(alan_metin)
        urun = var_urun_liste.get()
        v = BITKI_VERILERI[urun]
        sabit_debi = 72 # 20 L/s = 72 m3/h
        
        if v["tip"] == "Damlama":
            metraj = (1000 / v["aralik"]) * alan
            birim = f"{metraj:,.0f} Metre Damlama Borusu"
        else:
            tabanca = (alan * 1000) / 144
            birim = f"{tabanca:,.0f} Adet Yagmurlama Tabancasi"

        gunluk_su = alan * v["su_ihtiyac"]
        sure = gunluk_su / sabit_debi

        rapor = (f"Urun: {urun}\n"
                 f"Ihtiyac: {birim}\n"
                 f"Ana Boru: 110 mm\n"
                 f"Gunluk Su: {gunluk_su:.1f} Ton\n"
                 f"Sure: {sure:.1f} Saat\n")
        return rapor
    except ValueError:
        return "HATA: Alan kismina sadece rakam giriniz."

def whatsapp_gonder():
    isim = entry_isim.get()
    ilce = entry_ilce.get()
    alan = entry_alan.get()
    urun = var_urun_liste.get()
    
    if not isim or not ilce or not alan:
        messagebox.showwarning("Uyari", "Lutfen alanlari doldurun!")
        return

    teknik_not = boru_hesapla()
    
    mesaj = (f"Sayin AHMET FIKRET TEMELTAS,\n\n"
             f"Ben {isim}. {ilce} bolgesindeki {alan} donum {urun} arazim icin destek istiyorum.\n\n"
             f"{teknik_not}\n"
             f"Software Developed by AHMET FIKRET TEMELTAS")
    
    # Senin numaran
    url = f"https://wa.me/905075031990?text={mesaj}"
    webbrowser.open(url)

def belge_sec(belge_turu):
    yol = filedialog.askopenfilename()
    if yol:
        messagebox.showinfo("Basarili", f"{belge_turu} secildi.")

# --- ARAYUZ ---
root = tk.Tk()
root.title("Ahmet Fikret Temeltas - Sulama Sistemleri")
root.geometry("450x750")

# BASLIK
tk.Label(root, text="PROJE GELISTIRICI", font=("Arial", 10, "italic")).pack(pady=5)
tk.Label(root, text="AHMET FIKRET TEMELTAS", font=("Arial", 14, "bold"), fg="darkgreen").pack(pady=5)

# GIRIS ALANLARI
tk.Label(root, text="Ciftci Ad Soyad:").pack()
entry_isim = tk.Entry(root, width=35); entry_isim.pack(pady=2)

tk.Label(root, text="Ilce / Koy:").pack()
entry_ilce = tk.Entry(root, width=35); entry_ilce.pack(pady=2)

tk.Label(root, text="\nUrun Secimi:", font=("Arial", 10, "bold")).pack()
var_urun_liste = tk.StringVar(root)
var_urun_liste.set("Misir")
tk.OptionMenu(root, var_urun_liste, *BITKI_VERILERI.keys()).pack()

tk.Label(root, text="Tarla Alani (Donum):").pack()
entry_alan = tk.Entry(root, width=15); entry_alan.pack()

# BELGE BUTONLARI
tk.Label(root, text="\nEVRAK YUKLEME", font=("Arial", 10, "bold")).pack()
f_btn = tk.Frame(root); f_btn.pack()
for b in ["CKS", "Ruhsat", "Tapu"]:
    tk.Button(f_btn, text=b, width=8, command=lambda x=b: belge_sec(x)).pack(side=tk.LEFT, padx=2)

# ISLEM BUTONLARI
tk.Button(root, text="TEKNIK HESAPLA", bg="orange", fg="white", 
          command=lambda: messagebox.showinfo("Teknik Rapor", boru_hesapla())).pack(pady=20)

tk.Button(root, text="WHATSAPP GONDER", bg="green", fg="white", 
          font=("Arial", 12, "bold"), height=2, command=whatsapp_gonder).pack(pady=5)

# IMZA
tk.Label(root, text="\n" + "-"*35).pack()
tk.Label(root, text="Software Developed by", font=("Arial", 8)).pack()
tk.Label(root, text="Ahmet Fikret Temeltas", font=("Arial", 10, "bold")).pack()

root.mainloop()

