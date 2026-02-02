import streamlit as st
import math

# --- TEKNİK PARAMETRELER ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12.0, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş - Hidrolik Dizayn", layout="wide")

st.markdown("<h1 style='text-align: center; color: #004D40;'>PROFESYONEL SULAMA PROJELENDİRME</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2E7D32;'>Software Developed by AHMET FİKRET TEMELTAŞ</h3>", unsafe_allow_html=True)

st.write("---")

# --- GİRİŞ PANELİ ---
with st.sidebar:
    st.header("📐 Arazi Boyutları")
    tarla_eni = st.number_input("Tarla Eni (m) - [Lateral Yönü]", min_value=1.0, value=200.0)
    tarla_boyu = st.number_input("Tarla Boyu (m) - [Ana Boru Hattı]", min_value=1.0, value=300.0)
    
    st.header("💧 Hidrolik Kapasite")
    debi_ls = st.number_input("Mevcut Debi (L/s)", min_value=1.0, value=20.0)
    saatlik_kapasite = debi_ls * 3.6 # Ton/Saat

# --- HESAPLAMA MANTIĞI ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Proje Parametreleri")
    urun = st.selectbox("Ekilacak Ürün", list(BITKI_VERILERI.keys()))
    sistem = st.radio("Sistem Tipi", ["Damlama", "Yağmurlama"])
    
    # Alan Hesabı
    alan_m2 = tarla_eni * tarla_boyu
    alan_donum = alan_m2 / 1000
    
    v = BITKI_VERILERI[urun]
    
    st.subheader("📂 Evrak Yönetimi")
    st.file_uploader("Belgeleri Buraya Sürükleyin (ÇKS, Tapu, Ruhsat)", accept_multiple_files=True)

with col2:
    st.subheader("🏗️ Mühendislik Çıktıları")
    
    # 1. Metraj Hesabı
    if sistem == "Damlama":
        sira_sayisi = tarla_boyu / v["aralik"]
        toplam_lateral = sira_sayisi * tarla_eni
        ekipman_notu = f"{toplam_lateral:,.0f} m Damlama Borusu"
    else:
        tabanca_sayisi = alan_m2 / 144
        ekipman_notu = f"{int(tabanca_sayisi)} Adet Yağmurlama Tabancası"

    # 2. Vardiya (Bölme) Hesabı
    # Toplam su ihtiyacını (mm/gün) karşılamak için gereken anlık debi
    toplam_gunluk_su = alan_donum * v["su_ihtiyac"]
    
    # Kritik mühendislik: Tarlayı kaça bölmeliyiz?
    # Bir vardiyada sulanabilecek max alan = (Debi / Bitki Su İhtiyacı Katsayısı) bazlı karmaşık hesap yerine basitleştirilmiş:
    vardiya_sayisi = math.ceil(toplam_gunluk_su / (saatlik_kapasite * 4)) # Bir vardiya ortalama 4 saat varsayılırsa
    
    # 3. Ana Boru Çapı (Hız limitine göre 1.5 m/s varsayımıyla)
    if debi_ls <= 10: ana_cap = "75 mm"
    elif debi_ls <= 20: ana_cap = "90 mm"
    elif debi_ls <= 35: ana_cap = "110 mm"
    else: ana_cap = "125 mm veya üstü"

    # GÖSTERGE PANELI
    st.metric("Toplam Arazi", f"{alan_donum:.1f} Dönüm")
    st.info(f"📏 **Ana Boru Hattı:** {tarla_boyu} Metre - **Çap:** {ana_cap}")
    st.info(f"🛠️ **Lateral Hattı:** {ekipman_notu}")
    
    if vardiya_sayisi > 1:
        st.error(f"⚠️ **Sistem Bölünmeli:** Tarlayı en az **{vardiya_sayisi} vardiya (parça)** halinde sulamalısınız.")
    else:
        st.success("✅ **Tek Sefer:** Mevcut debi ile tarlanın tamamı tek seferde sulanabilir.")

# --- WHATSAPP VE İMZA ---
st.write("---")
if st.button("PROJE DETAYLARINI WHATSAPP İLE GÖNDER"):
    msg = (f"Sayın AHMET FİKRET TEMELTAŞ,\n\n"
           f"Yeni Proje Analizi:\n"
           f"Arazi: {tarla_eni}m x {tarla_boyu}m ({alan_donum:.1f} Dönüm)\n"
           f"Ürün: {urun} / {sistem}\n"
           f"Ana Boru: {tarla_boyu}m ({ana_cap})\n"
           f"İhtiyaç: {ekipman_notu}\n"
           f"Vardiya Sayısı: {vardiya_sayisi}\n"
           f"Su Kaynağı: {debi_ls} L/s\n\n"
           f"Software Developed by AHMET FİKRET TEMELTAŞ")
    
    url = f"https://wa.me/905075031990?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
    st.markdown(f'<a href="{url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">WhatsApp Mesajını Onayla</a>', unsafe_allow_html=True)

st.write("\n\n")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2026 Ahmet Fikret Temeltaş | Hidrolik Analiz Yazılımı v2.0</p>", unsafe_allow_html=True)


