import streamlit as st

# --- MÜHENDİSLİK VERİTABANI ---
# Aralik: Lateral borular arası mesafe (metre)
# Su İhtiyacı: mm/gün
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Yonca": {"aralik": 12, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş - Mühendislik", layout="wide")

# --- BAŞLIK VE İMZA ---
st.markdown("<h1 style='text-align: center; color: #2E7D32;'>SULAMA PROJE VE ANALİZ SİSTEMİ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Software Developed by AHMET FİKRET TEMELTAŞ</b></p>", unsafe_allow_html=True)
st.write("---")

# --- SOL PANEL: GİRİŞLER ---
with st.sidebar:
    st.header("📍 Arazi Bilgileri")
    isim = st.text_input("Çiftçi Ad Soyad")
    ilce = st.text_input("İlçe / Köy")
    ada_parsel = st.text_input("Ada / Parsel No")
    
    st.header("💧 Su Kaynağı")
    debi = st.number_input("Su Debisi (Litre/Saniye)", value=20.0) # Senin 20 L/s sabitin
    saatlik_ton = debi * 3.6 # L/s'den Ton/Saat'e çevrim
    st.info(f"Kapasiteniz: {saatlik_ton:.1f} Ton/Saat")

# --- ANA PANEL ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌾 Ürün ve Alan")
    urun = st.selectbox("Ekilacak Ürün", list(BITKI_VERILERI.keys()))
    alan = st.number_input("Tarla Alanı (Dönüm)", min_value=1.0, step=1.0)
    
    st.subheader("📂 Belge Yükleme")
    cks = st.file_uploader("ÇKS Belgesi", type=['pdf', 'jpg', 'png'])
    tapu = st.file_uploader("Tapu / Kira Sözleşmesi", type=['pdf', 'jpg', 'png'])
    ruhsat = st.file_uploader("Kuyu Ruhsatı", type=['pdf', 'jpg', 'png'])

with col2:
    st.subheader("📏 Mühendislik Hesaplamaları")
    if alan > 0:
        v = BITKI_VERILERI[urun]
        
        # 1. BORU HESABI (Metraj)
        # Formül: (1000 / Sıra Arası) * Alan (Dönüm)
        if v["tip"] == "Damlama":
            boru_metraj = (1000 / v["aralik"]) * alan
            sonuc_ekipman = f"{boru_metraj:,.0f} Metre Damlama Borusu"
        else:
            # Yağmurlama için 12x12 dizilimde tabanca sayısı
            tabanca_sayisi = (alan * 1000) / 144
            sonuc_ekipman = f"{int(tabanca_sayisi)} Adet Yağmurlama Tabancası"

        # 2. SU İHTİYACI VE ZAMAN HESABI
        gunluk_ihtiyac_ton = alan * v["su_ihtiyac"]
        sulama_suresi = gunluk_ihtiyac_ton / saatlik_ton

        st.metric("Gereken Boru / Ekipman", sonuc_ekipman)
        st.metric("Günlük Toplam Su İhtiyacı", f"{gunluk_ihtiyac_ton:.1f} Ton")
        st.warning(f"🕒 Bu tarlayı günde **{sulama_suresi:.1f} saat** sulamanız gerekmektedir.")
        
        st.write("---")
        # WhatsApp Mesajı Oluşturma
        mesaj = (f"Sayın AHMET FİKRET TEMELTAŞ,\n\n"
                 f"Ben {isim}. {ilce} bölgesindeki {alan} dönüm {urun} arazim için analiz yaptım.\n"
                 f"Sonuç: {sonuc_ekipman} ihtiyacım var.\n"
                 f"Günlük {gunluk_ihtiyac_ton} ton su gerekiyor. {debi} L/s su ile {sulama_suresi:.1f} saat sulama yapacağım.\n\n"
                 f"Ada/Parsel: {ada_parsel}")
        
        whatsapp_url = f"https://wa.me/905075031990?text={mesaj.replace(' ', '%20').replace('\n', '%0A')}"
        
        if st.button("HESAPLAMALARI ONAYLA VE WHATSAPP'A GÖNDER"):
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none; background-color: #25D366; color: white; padding: 10px 20px; border-radius: 5px;">WhatsApp Mesajını Başlat</a>', unsafe_allow_html=True)

st.write("---")
st.caption("© 2026 - Tüm Hakları Saklıdır. Ahmet Fikret Temeltaş Mühendislik Çözümleri.")


