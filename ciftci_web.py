import streamlit as st
from datetime import date
import urllib.parse

# --- 1. MALZEME BİRİM FİYATLARI ---
BIRIM_FIYATLAR = {
    "Damlama_Boru_Metre": 5.50,
    "Yagmurlama_Tabanca": 950.0,
    "Ana_Boru_110mm": 350.0,
    "Filtre_Gubre_Sistemi": 18000
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

# --- ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Temel Mühendislik", page_icon="🚜")

st.title("🚜 SULAMA MALİYET HESAPLAYICI")
st.caption('"Toprağınız Suya, Cebiniz Rahata Kavuşsun"')
st.divider()

# --- GİRİŞ ALANLARI ---
col1, col2 = st.columns(2)

with col1:
    isim = st.text_input("Çiftçi Adı")
    ilce = st.text_input("İlçe / Köy")

with col2:
    alan = st.number_input("Tarla Alanı (Dönüm)", min_value=0.0, step=1.0)
    urun = st.selectbox("Ürün Seçimi", list(BITKI_VERILERI.keys()))

# --- BELGE YÜKLEME (Yeni Eklenen Kısım) ---
st.subheader("📁 Gerekli Belgeler")
st.file_uploader("ÇKS Belgesi Yükle", type=['pdf', 'jpg', 'png'])
st.file_uploader("Kuyu Ruhsatı / Tapu Yükle", type=['pdf', 'jpg', 'png'])

# --- HESAPLAMA MANTIĞI ---
def teklif_olustur():
    if alan <= 0:
        return None
    
    v = BITKI_VERILERI[urun]
    if v["tip"] == "Damlama":
        metraj = (1000 / v["aralik"]) * alan
        malzeme_maliyet = metraj * BIRIM_FIYATLAR["Damlama_Boru_Metre"]
        detay = f"{metraj:,.0f} Metre Damlama Borusu"
    else:
        adet = (alan * 1000) / 144
        malzeme_maliyet = adet * BIRIM_FIYATLAR["Yagmurlama_Tabanca"]
        detay = f"{adet:,.0f} Adet Yağmurlama Tabancası"
        
    ana_mlyt = (alan * 20) * BIRIM_FIYATLAR["Ana_Boru_110mm"]
    toplam = malzeme_maliyet + ana_mlyt + BIRIM_FIYATLAR["Filtre_Gubre_Sistemi"]
    
    return detay, malzeme_maliyet, ana_mlyt, toplam

# --- SONUÇ VE WHATSAPP ---
veriler = teklif_olustur()

if st.button("HESAPLA VE TEKLİF OLUŞTUR", use_container_width=True):
    if veriler:
        detay, mat_mlyt, ana_mlyt, toplam = veriler
        st.success(f"### Tahmini Toplam: {toplam:,.0f} TL")
        
        # WhatsApp Mesaj Hazırlama
        mesaj = (
            f"*SULAMA SİSTEMİ MALİYET TEKLİFİ*\n"
            f"---------------------------\n"
            f"👤 *Müşteri:* {isim if isim else 'Sayın Çiftçimiz'} / {ilce}\n"
            f"🌾 *Ürün:* {urun} ({alan} Dönüm)\n"
            f"---------------------------\n"
            f"📦 *Malzeme Listesi:*\n"
            f"• {detay}: {mat_mlyt:,.0f} TL\n"
            f"• Ana Boru Hattı: {ana_mlyt:,.0f} TL\n"
            f"• Filtre & Gübreleme: {BIRIM_FIYATLAR['Filtre_Gubre_Sistemi']:,} TL\n"
            f"💰 *TOPLAM:* {toplam:,.0f} TL\n"
            f"---------------------------\n"
            f"*Güneşle Gelen Bereket*\n"
            f"Ahmet Fikret Temeltaş\n"
            f"📞 0507 503 19 90"
        )
        
        # WhatsApp Linki
        encoded_mesaj = urllib.parse.quote(mesaj)
        wa_url = f"https://wa.me/905075031990?text={encoded_mesaj}"
        
        st.link_button("TEKLİFİ WHATSAPP'A GÖNDER", wa_url, type="primary", use_container_width=True)
    else:
        st.error("Lütfen alan bilgisini giriniz!")

# --- ALT BİLGİ ---
st.divider()
st.write(f"📅 Tarih: {date.today().strftime('%d.%m.%Y')}")
st.write("Ahmet Fikret Temeltaş | 0507 503 19 90")

