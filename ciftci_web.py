import streamlit as st
import math

# --- TEKNİK VERİTABANI VE MALZEME STANDARTLARI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "lateral_cap": "16mm", "damlatici_aralik": "33cm"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "lateral_cap": "16mm", "damlatici_aralik": "33cm"},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "lateral_cap": "Sprint", "damlatici_aralik": "12m"},
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş | Teknik Şartname", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>HİDROLİK DİZAYN VE MALZEME METRAJ LİSTESİ</b></p>", unsafe_allow_html=True)

# --- GİRİŞLER ---
with st.sidebar:
    st.header("📐 Tarla ve Sistem")
    t_en = st.number_input("Sıra Uzunluğu (En - m)", value=200.0)
    t_boy = st.number_input("Ana Boru Hattı (Boy - m)", value=300.0)
    debi = st.number_input("Kaynak Debisi (L/s)", value=20.0)
    
    st.header("⚙️ Malzeme Seçimi")
    pn_sinifi = st.selectbox("Ana Boru Basınç Sınıfı", ["PN6 (Düşük)", "PN10 (Standart)"])
    lat_tip = st.selectbox("Lateral Çapı", ["16mm", "22mm"])
    urun = st.selectbox("Ürün", list(BITKI_VERILERI.keys()))

# --- MÜHENDİSLİK HESABI ---
v = BITKI_VERILERI[urun]
alan_donum = (t_en * t_boy) / 1000
sira_sayisi = t_boy / v["aralik"]
toplam_lateral = sira_sayisi * t_en

# Ana Boru Çapı Kararı (Debiye Göre)
if debi <= 18: ana_cap = "90 mm"
elif debi <= 32: ana_cap = "110 mm"
else: ana_cap = "125 mm"

# Filtre Kararı
filtre = "3\" Otomatik Disk Filtre (İkiz Takım)" if debi >= 20 else "2.5\" Manuel Disk Filtre"

# --- RAPORLAMA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Teknik Metraj Listesi")
    st.markdown(f"""
    * **Ana Boru:** {t_boy} Metre {ana_cap} {pn_sinifi} PE100
    * **Lateral Boru:** {toplam_lateral:,.0f} Metre {lat_tip} (Damlama)
    * **Filtre İstasyonu:** 1 Adet {filtre}
    * **Vana Grubu:** {math.ceil(alan_donum/20)} Adet 3" Küresel Vana (Bölge Kontrol)
    * **Ek Parçalar:** * {int(sira_sayisi)} Adet 'Kurt Ağzı' Conta ve Çıkış Nipeli
        * {int(sira_sayisi)} Adet Lateral Kör Tapası
        * 1 Adet Hava Tahliye Vanası (Vantuz - 2")
    """)

with col2:
    st.subheader("💧 Hidrolik Analiz")
    toplam_su = alan_donum * v["su_ihtiyac"]
    vardiya = math.ceil(toplam_su / (debi * 3.6 * 4)) # 4 saatlik periyot
    
    st.metric("Toplam Donum", f"{alan_donum:.1f}")
    st.metric("Vardiya Sayısı", f"{vardiya}")
    
    st.warning(f"**Mühendislik Notu:** Ana boru hattı {ana_cap} seçilerek sürtünme kaybı minimize edilmiştir. {pn_sinifi} kullanımı tavsiye edilir.")

# --- WHATSAPP GÖNDERİMİ ---
st.write("---")
if st.button("TEKNİK ŞARTNAMEYİ WHATSAPP'A GÖNDER"):
    msg = (f"Sayın AHMET FİKRET TEMELTAŞ,\n"
           f"Teknik Malzeme Listesi:\n"
           f"- Arazi: {alan_donum:.1f} Dönüm\n"
           f"- Ana Boru: {t_boy}m {ana_cap} {pn_sinifi}\n"
           f"- Lateral: {toplam_lateral:,.0f}m {lat_tip}\n"
           f"- Filtre: {filtre}\n"
           f"- Ek Parça: {int(sira_sayisi)} adet çıkış nipeli ve conta\n"
           f"Software Developed by AHMET FİKRET TEMELTAŞ")
    
    url = f"https://wa.me/905075031990?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
    st.markdown(f'<a href="{url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">WhatsApp\'a Aktar</a>', unsafe_allow_html=True)

