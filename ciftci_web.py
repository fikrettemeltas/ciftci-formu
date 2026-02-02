import streamlit as st

# --- TEKNİK VERİLER ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama", "lateral_max": 100},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama", "lateral_max": 80},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama", "lateral_max": 100},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "tip": "Yağmurlama", "lateral_max": 150},
    "Buğday": {"aralik": 12.0, "su_ihtiyac": 5, "tip": "Yağmurlama", "lateral_max": 150}
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş | Mühendislik", layout="wide")

st.markdown(f"<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>PROJE VE SULAMA SİSTEMLERİ MÜHENDİSLİK HESABI</p>", unsafe_allow_html=True)

st.write("---")

# --- GİRİŞ PANELİ ---
with st.sidebar:
    st.header("📋 Arazi Bilgileri")
    isim = st.text_input("Çiftçi Ad Soyad")
    ilce = st.text_input("İlçe / Köy")
    
    st.header("📐 Tarla Ölçüleri (Metre)")
    tarla_boyu = st.number_input("Ana Boru Hattı Boyu (m)", min_value=1.0, value=100.0)
    tarla_eni = st.number_input("Sıraların Uzunluğu (m)", min_value=1.0, value=100.0)
    
    st.header("💧 Su Kaynağı")
    debi = st.number_input("Su Debisi (L/s)", value=20.0)
    ton_saat = debi * 3.6

# --- HESAPLAMA MOTORU ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("⚙️ Sistem Seçimi")
    sistem_turu = st.radio("Uygulanacak Sistem", ["Damlama Sulama", "Yağmurlama Sulama"])
    urun = st.selectbox("Ekilacak Ürün", list(BITKI_VERILERI.keys()))
    
    st.subheader("📂 Evrak Yönetimi")
    st.file_uploader("ÇKS / Tapu / Ruhsat Yükle", accept_multiple_files=True)

with col2:
    st.subheader("📊 Mühendislik Sonuçları")
    
    # MATEMATİKSEL ANALİZ
    v = BITKI_VERILERI[urun]
    alan_donum = (tarla_boyu * tarla_eni) / 1000
    
    if "Damlama" in sistem_turu:
        # Tarla boyu boyunca kaç sıra lateral boru döşenecek?
        sira_sayisi = tarla_boyu / v["aralik"]
        # Toplam lateral boru = Sıra sayısı * Bir sıranın uzunluğu (tarla eni)
        toplam_lateral = sira_sayisi * tarla_eni
        ana_boru_capi = "110 mm" if ton_saat > 50 else "90 mm"
        sonuc_metni = f"{toplam_lateral:,.0f} Metre Damlama Borusu"
    else:
        # Yağmurlama hesabı (12x12m standart dizilim)
        tabanca_sayisi = (tarla_boyu * tarla_eni) / 144
        ana_boru_capi = "125 mm" if ton_saat > 60 else "110 mm"
        sonuc_metni = f"{int(tabanca_sayisi)} Adet Yağmurlama Tabancası"

    gunluk_su = alan_donum * v["su_ihtiyac"]
    sulama_suresi = gunluk_su / ton_saat

    # SONUÇ TABLOSU
    st.info(f"📍 **Arazi Alanı:** {alan_donum:.2f} Dönüm")
    st.success(f"📦 **Ana Boru İhtiyacı:** {tarla_boyu:.0f} Metre ({ana_boru_capi})")
    st.success(f"🛠️ **Lateral/Ekipman:** {sonuc_metni}")
    st.warning(f"🕒 **Sulama Süresi:** {sulama_suresi:.1f} Saat/Gün")

# --- WHATSAPP GÖNDERİMİ ---
st.write("---")
if st.button("PROJEYİ ONAYLA VE AHMET BEY'E GÖNDER"):
    whatsapp_mesaj = (
        f"Sayın AHMET FİKRET TEMELTAŞ,\n\n"
        f"Ben {isim}. {ilce} bölgesindeki arazim için analiz yaptım.\n"
        f"Tarla: {tarla_boyu}x{tarla_eni}m ({alan_donum:.2f} Dönüm)\n"
        f"Ürün: {urun} | Sistem: {sistem_turu}\n"
        f"Ana Boru: {tarla_boyu}m {ana_boru_capi}\n"
        f"Lateral: {sonuc_metni}\n"
        f"Sulama Süresi: {sulama_suresi:.1f} saat\n\n"
        f"Software Developed by AHMET FİKRET TEMELTAŞ"
    )
    url = f"https://wa.me/905075031990?text={whatsapp_mesaj.replace(' ', '%20').replace('\n', '%0A')}"
    st.markdown(f'<a href="{url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">WhatsApp Mesajını Onayla</a>', unsafe_allow_html=True)

st.write("\n\n")
st.caption("© 2026 Ahmet Fikret Temeltaş - Akıllı Tarım Çözümleri")

