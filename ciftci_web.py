import tkinter as tk
from tkinter import messagebox
import webbrowser
from datetime import date

# --- 1. MALZEME BİRİM FİYATLARI (Buradan Güncelleyebilirsin) ---
BIRIM_FIYATLAR = {
    "Damlama_Boru_Metre": 5.50,    # TL
    "Yagmurlama_Tabanca": 950.0,   # TL
    "Ana_Boru_110mm": 350.0,       # TL
    "Filtre_Gubre_Sistemi": 18000  # TL (Paket)
}

# --- 2. MÜHENDİSLİK VERİTABANI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "tip": "Damlama"},
    "Yonca": {"aralik": 12, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12, "tip": "Yağmurlama"},
    "Arpa": {"aralik": 12, "tip": "Yağmurlama"}
}

def teklif_olustur():
    try:
        alan = float(entry_alan.get())
        urun = var_urun_liste.get()
        v = BITKI_VERILERI[urun]
        
        # Malzeme Miktarı ve Maliyet Hesabı
        if v["tip"] == "Damlama":
            metraj = (1000 / v["aralik"]) * alan
            malzeme_maliyet = metraj * BIRIM_FIYATLAR["Damlama_Boru_Metre"]
            detay = f"{metraj:,.0f} Metre Damlama Borusu"
        else:
            adet = (alan * 1000) / 144
            malzeme_maliyet = adet * BIRIM_FIYATLAR["Yagmurlama_Tabanca"]
            detay = f"{adet:,.0f} Adet Yağmurlama Tabancası"

        ana_boru_maliyet = (alan * 20) * BIRIM_FIYATLAR["Ana_Boru_110mm"]
        toplam = malzeme_maliyet + ana_boru_maliyet + BIRIM_FIYATLAR["Filtre_Gubre_Sistemi"]

        return detay, malzeme_maliyet, ana_boru_maliyet, toplam
    except:
        return None

def whatsapp_gonder():
    veriler = teklif_olustur()
    if not veriler:
        messagebox.showerror("Hata", "Lütfen alan bilgisini sayı olarak girin!")
        return

    detay, mat_mlyt, ana_mlyt, toplam = veriler
    isim = entry_isim.get()
    ilce = entry_ilce.get()

    mesaj = (
        f"*SULAMA SİSTEMİ MALİYET TEKLİFİ*\\n"
        f"---------------------------\\n"
        f"👤 *Müşteri:* {isim if isim else 'Sayın Çiftçimiz'} / {ilce}\\n"
        f"🌾 *Ürün:* {var_urun_liste.get()} ({entry_alan.get()} Dönüm)\\n"
        f"---------------------------\\n"
        f"📦 *Malzeme Listesi:*\\n"
        f"• {detay}: {mat_mlyt:,.0f} TL\\n"
        f"• Ana Boru Hattı: {ana_mlyt:,.0f} TL\\n"
        f"• Filtre & Gübreleme: {BIRIM_FIYATLAR['Filtre_Gubre_Sistemi']:,} TL\\n"
        f"💰 *TOPLAM:* {toplam:,.0f} TL\\n"
        f"---------------------------\\n"
        f"*Güneşle Gelen Bereket*\\n"
        f"*Ahmet Fikret Temeltaş*\\n"
        f"📞 0507 503 19 90"
    )
    
    url = f"https://wa.me/905075031990?text={mesaj}"
    webbrowser.open(url)

# --- ARAYÜZ ---
root = tk.Tk()
root.title("Ahmet Fikret Temeltaş - Sulama Proje")
root.geometry("400x700")

tk.Label(root, text="SULAMA MALİYET HESAPLAYICI", font=("Arial", 12, "bold"), fg="#1B5E20").pack(pady=10)
tk.Label(root, text="\"Toprağınız Suya, Cebiniz Rahata Kavuşsun\"", font=("Arial", 9, "italic")).pack()

# Giriş Alanları
tk.Label(root, text="\nÇiftçi Adı:").pack()
entry_isim = tk.Entry(root, width=35); entry_isim.pack()

tk.Label(root, text="İlçe / Köy:").pack()
entry_ilce = tk.Entry(root, width=35); entry_ilce.pack()

tk.Label(root, text="Tarla Alanı (Dönüm):").pack()
entry_alan = tk.Entry(root, width=15); entry_alan.pack()

tk.Label(root, text="\nÜrün Seçimi:").pack()
var_urun_liste = tk.StringVar(root); var_urun_liste.set("Mısır")
tk.OptionMenu(root, var_urun_liste, *BITKI_VERILERI.keys()).pack()

# Butonlar
tk.Button(root, text="MALZEME VE FİYAT LİSTESİ OLUŞTUR", bg="#2E7D32", fg="white", 
          font=("Arial", 10, "bold"), command=lambda: messagebox.showinfo("Teklif Özeti", 
          f"Tahmini Toplam Maliyet: {teklif_olustur()[3]:,.0f} TL" if teklif_olustur() else "Hata!")).pack(pady=20)

tk.Button(root, text="TEKLİFİ WHATSAPP'A GÖNDER", bg="#25D366", fg="white", 
          font=("Arial", 10, "bold"), command=whatsapp_gonder).pack(pady=5)

# Alt Bilgi
tk.Label(root, text=f"\n{date.today().strftime('%d.%m.%Y')}\nAhmet Fikret Temeltaş\n0507 503 19 90").pack()

root.mainloop()

