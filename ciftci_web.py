import streamlit as st
import math
import urllib.parse

# --- BITKI VERİTABANI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12.0, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

# Sayfa Ayarları
st.set_page_config(page_title="Ahmet Fikret Temeltaş | Sulama", layout="wide")

# Başlıklar
st.markdown("<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>PROFESYONEL SULAMA PROJELENDİRME SİSTEMİ</p>", unsafe_allow_html=True)
st.write("---")

# --- 1. BÖLÜM: KİMLİK BİLGİLERİ ---
st.subheader("👤 Müşteri ve Arazi Bilgileri")
c1, c2, c3 = st.columns(3)
with c1:
    ad_soyad = st.text_input("Müşteri Ad Soyad", value="")
    ilce = st.text_input("İlçe", value="")
with c2:
    koy = st.text_input("Köy / Mahalle", value="")
    ada = st.text_input("Ada No", value="")
with c3:
    parsel = st.text_input("Parsel No", value="")
    telefon = st.text_input("WhatsApp No (Örn: 905075031990)", value="905075031990")

st.write("---")

# --- 2. BÖLÜM: TEKNİK VERİLER ---
st.subheader("⚙️ Teknik Sistem Verileri")
t1, t2, t3 = st.columns(3)
with t1:
    sistem_turu = st.radio("Sistem Tipi", ["Damlama Sulama", "Yağmurlama Sulama"])
    urun = st.selectbox("Ekilcek Ürün", list(BITKI_VERILERI.keys()))
with t2:
    t_en = st.number_input("Sıra Uzunluğu (m)", value=200.0)
    t_boy = st.number_input("Ana Boru Hattı (m)", value=300.0)
with t3:
    debi = st.number_input("Su Kaynağı Debisi (L/s)", value=20.0)
    pn_sinifi = st.selectbox("Basınç Sınıfı", ["PN6", "PN10"])

# --- MÜHENDİSLİK HESAPLARI ---
v = BITKI_VERILERI[urun]
alan_donum = (t_en * t_boy) / 1000
saatlik_ton = debi * 3.6

# Ana Boru Çapı
if debi <= 18: 
    ana_cap = "90 mm"
elif debi <= 32: 
    ana_cap = "110 mm"
else: 
    ana_cap = "125 mm"

# Malzeme Metrajı
if "Damlama" in sistem_turu:
    sira_sayisi = t_boy / v["aralik"]
    metraj = sira_sayisi * t_en
    ekipman_adi = f"{metraj:,.0f} Metre Damlama Borusu"
    ek_parca = f"{int(sira_sayisi)} Adet Conta ve Nipel"
    filtre_tipi = "3\" Otomatik Disk Filtre Sistemi"
else:
    tabanca_sayisi = (t_en * t_boy) / 144
    ekipman_adi = f"{int(tabanca_sayisi)} Adet Yağmurlama Tabancası"
    ek_parca = f"{int(t_boy/6)} Adet 6m Boru ve Abot"
    filtre_tipi = "3\" Hidrosiklonlu Filtre Grubu"

# --- ÖZET TABLO ---
st.write("### 📋 Proje Özeti")
o1, o2, o3 = st.columns(3)
o1.metric("Toplam Alan", f"{alan_donum:.1f} Dönüm")
o2.metric("Ana Boru", f"{ana_cap}")
o3.metric("Filtre", "3 İnç")

# --- WHATSAPP MESAJ HAZIRLAMA ---
msg = (
    f"*SULAMA PROJESİ TEKNİK ŞARTNAMESİ*\n"
    f"------------------------------------\n"
    f"*Müşteri:* {ad_soyad}\n"
    f"*Konum:* {ilce} / {koy}\n"
    f"*Tapu:* Ada {ada} / Parsel {parsel}\n"
    f"------------------------------------\n"
    f"*PROJE DETAYLARI:*\n"
    f"- Alan: {alan_donum:.1f} Dönüm\n"
    f"- Ürün: {urun}\n"
    f"- Sistem: {sistem_turu}\n\n"
    f"*MALZEME LİSTESİ:*\n"
    f"- Ana Boru: {t_boy}m {ana_cap} {pn_sinifi}\n"
    f"- Lateral: {ekipman_adi}\n"
    f"- Filtre: {filtre_tipi}\n"
    f"- Ek Parçalar: {ek_parca}\n"
    f"------------------------------------\n"
    f"*Mühendis:* Ahmet Fikret Temeltaş"
)

# URL Güvenliği için encode
encoded_msg = urllib.parse.quote(msg)
wa_link = f"https://wa.me/{telefon}?text={encoded_msg}"

st.write("---")
# Şık bir buton tasarımı
st.markdown(f"""
    <div style="display: flex; justify-content: center;">
        <a href="{wa_link}" target="_blank" style="
            background-color: #25D366;
            color: white;
            padding: 18px 50px;
            text-decoration: none;
            font-size: 20px;
            font-weight: bold;
            border-radius: 15px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        ">
            🚀 TEKNİK ŞARTNAMEYİ WHATSAPP'A GÖNDER
        </a>
    </div>
    """, unsafe_allow_html=True)

st.write("\n\n")
st.caption("© 2026 Ahmet Fikret Temeltaş")



