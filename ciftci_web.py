Haklısın moruk, heyecandan adını soyadını kodun en üstüne, başköşeye koymayı unuttuk! Hemen düzelttim.

Şimdi bu kod; senin gönderdiğin orijinal dosyadaki belge yükleme (ÇKS, Tapu vb.) özelliklerini de koruyor, üzerine bu konuştuğumuz akıllı boru ve su hesabı motorunu ekliyor. En önemlisi, her şeyin başında ve sonunda senin ismin var.

🚀 Ahmet Fikret Temeltaş - Akıllı Sulama Proje Kodları
Python
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

        rapor = (f"--- TEKNİK ANALİZ ---\n"
                 f"📍 Ürün: {urun}\n"
                 f"📏 İhtiyaç: {birim}\n"
                 f"🏗️ Ana Boru: 110 mm\n"
                 f"💧 Günlük Su: {gunluk_su:.1f} Ton\n"
                 f"⏰ Sulama Süresi: {sure:.1f} Saat\n")
        return rapor
    except:
        return "Lütfen alan bilgisini rakam giriniz."

def whatsapp_gonder():
    isim = entry_isim.get()
    ilce = entry_ilce.get()
    alan = entry_alan.get()
    urun = var_urun_liste.get()
    
    if not isim or not ilce or not alan:
        messagebox.showwarning("Uyarı", "Lütfen tüm bilgileri doldurun!")
        return

    teknik_not = boru_hesapla()
    mesaj = (f"Sayın AHMET FİKRET TEMELTAŞ,\n\n"
             f"Ben {isim}. {ilce} bölgesindeki {alan} dönüm {urun} arazim için teknik destek istiyorum.\n\n"
             f"{teknik_not}\n"
             f"Software Developed by AHMET FİKRET TEMELTAŞ")
    
    url = f"https://wa.me/905075031990?text={mesaj}"
    webbrowser.open(url)

def belge_sec(belge_turu):
    yol = filedialog.askopenfilename()
    if yol:
        messagebox.showinfo("Başarılı", f"{belge_turu} sisteme tanımlandı.")

# --- ARAYÜZ ---
root = tk.Tk()
root.title("Ahmet Fikret Temeltaş - Sulama Sistemleri")
root.geometry("450x850")

# BAŞLIK
tk.Label(root, text="PROJE GELİŞTİRİCİ", font=("Arial", 10, "italic")).pack(pady=2)
tk.Label(root, text="AHMET FİKRET TEMELTAŞ", font=("Arial", 14, "bold"), fg="#1B5E20").pack(pady=5)

# GİRİŞLER
fields = [("Çiftçi Ad Soyad:", "isim"), ("İlçe / Köy:", "ilce"), ("Ada No:", "ada"), ("Parsel No:", "parsel")]
entries = {}
for lbl, key in fields:
    tk.Label(root, text=lbl).pack()
    ent = tk.Entry(root, width=40)
    ent.pack(pady=2)
    entries[key] = ent

entry_isim, entry_ilce, entry_ada, entry_parsel = entries.values()

tk.Label(root, text="\nÜrün Seçimi:", font=("Arial", 10, "bold")).pack()
var_urun_liste = tk.StringVar(root); var_urun_liste.set("Mısır")
tk.OptionMenu(root, var_urun_liste, *BITKI_VERILERI.keys()).pack()

tk.Label(root, text="Tarla Alanı (Dönüm):").pack()
entry_alan = tk.Entry(root, width=20); entry_alan.pack()

# BELGELER
tk.Label(root, text="\nBELGE YÖNETİMİ", font=("Arial", 10, "bold")).pack()
btn_f = tk.Frame(root); btn_f.pack()
for b in ["ÇKS", "Ruhsat", "Tapu"]:
    tk.Button(btn_f, text=b, width=10, command=lambda x=b: belge_sec(x)).pack(side=tk.LEFT, padx=2)

# AKSİYON BUTONLARI
tk.Button(root, text="TEKNİK RAPORU GÖSTER", bg="#E67E22", fg="white", 
          command=lambda: messagebox.showinfo("Rapor", boru_hesapla())).pack(pady=15)

tk.Button(root, text="WHATSAPP'A GÖNDER", bg="#25D366", fg="white", 
          font=("Arial", 11, "bold"), height=2, command=whatsapp_gonder).pack(pady=10)

# ALT İMZA
tk.Label(root, text="\n" + "_"*40).pack()
tk.Label(root, text="© 2024 Software Developed by Ahmet Fikret Temeltaş", font=("Arial", 8)).pack(pady=10)

root.mainloop()

