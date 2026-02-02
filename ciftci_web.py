import streamlit as st
import math
import urllib.parse

# --- BİTKİ VERİTABANI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12.0, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş | Sulama", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>KOLAY SULAMA HESAPLAMA VE MALZEME LİSTESİ</p>", unsafe_allow_html=True)
st.write("---")

# --- 1. BÖLÜM: KİMLİK ---
st.subheader("👤 Çiftçi ve Arazi Bilgileri")
c1, c2, c3 = st.columns(3)
with c1:
    ad_soyad = st.text_input("Adınız Soyadınız")
    ilce = st.text_input("İlçe")
with c2:
    koy = st.text_input("Köy / Mahalle")
    ada = st.text_input("Ada No")
with c3:
    parsel = st.text_input("Parsel No")
    telefon = st.text_input("WhatsApp Numaranız", value="905075031990")

st.write("---")

# --- 2. BÖLÜM: ANLAŞILIR GİRİŞLER ---
st.subheader("🚜 Tarla Ölçüleri ve Su Durumu")
t1, t2, t3 = st.columns(3)
with t1:
    sistem_turu = st.radio("Nasıl Sulayacaksınız?", ["Damlama (Hortumla)", "Yağmurlama (Tabancayla)"])
    urun = st.selectbox("Ne Ekeceksiniz?", list(BITKI_VERILERI.keys()))
with t2:
    t_en = st.number_input("Hortum Serilecek Mesafe (Tarla Eni - m)", value=200.0, help="Damlama hortumlarının boyu kaç metre olacak?")
    t_boy = st.number_input("Su Borusunun Gideceği Yol (Tarla Boyu - m)", value=300.0, help="Kuyudan tarlanın sonuna giden ana boru kaç metre?")
with t3:
    debi = st.number_input("Saniyede Akan Su Miktarı (Litre/Saniye)", value=20.0, help="Kuyunuz saniyede kaç litre su veriyor?")
    pn_sinifi = st.selectbox("Boru Dayanıklılığı (Basınç)", ["PN6 (Normal)", "PN10 (Yüksek Basınç)"])

# --- HESAPLAMA ---
v = BITKI_VERILERI[urun]
alan_donum = (t_en * t_boy) / 1000

if debi <= 18: 
    ana_cap = "90'lık (90 mm)"
elif debi <= 32: 
    ana_cap = "110'luk (110 mm)"
else: 
    ana_cap = "125'lik (125 mm)"

if "Damlama" in sistem_turu:
    sira_sayisi = t_boy / v["aralik"]
    metraj = sira_sayisi * t_en
    ekipman_adi = f"{metraj:,.0f} Metre Damlama Hortumu"
    ek_parca = f"{int(sira_sayisi)} Takım Musluk, Conta ve Tapa"
    filtre_notu = "Büyük Boy (3 inç) Pislik Tutucu Otomatik Filtre"
else:
    tabanca_sayisi = (t_en * t_boy) / 144
    ekipman_adi = f"{int(tabanca_sayisi)} Adet Sulama Tabancası"
    ek_parca = f"{int(t_boy/6)} Adet Mandal boru ve Abot Takımı"
    filtre_notu = "3 inç Kum Ayırıcı (Hidrosiklon) Filtre Seti"

# --- SONUÇ PANELİ ---
st.write("---")
st.subheader("📋 Gereken Malzeme Listesi")
res1, res2 = st.columns(2)

with res1:
    st.info(f"📍 **Arazi:** {alan_donum:.1f} Dönüm {urun} tarlası")
    st.write(f"✅ **Ana Boru Hattı:** {t_boy} Metre {ana_cap} boru")
    st.write(f"✅ **Sulama Boruları:** {ekipman_adi}")

with res2:
    st.success(f"✅ **Filtre Sistemi:** {filtre_notu}")
    st.write(f"✅ **Bağlantı Parçaları:** {ek_parca}")
    st.write(f"⚠️ **Not:** {pn_sinifi} boru kullanılması tavsiye edilir.")

# --- WHATSAPP MESAJI ---
msg = (
    f"*SULAMA SİSTEMİ MALZEME LİSTESİ*\n"
    f"------------------------------------\n"
    f"*Çiftçi:* {ad_soyad}\n"
    f"*Yer:* {ilce} / {koy}\n"
    f"*Tapu:* Ada {ada} / Parsel {parsel}\n"
    f"------------------------------------\n"
    f"*TARLA BİLGİSİ:*\n"
    f"- Toplam Alan: {alan_donum:.1f} Dönüm\n"
    f"- Ekilen Ürün: {urun}\n"
    f"- Sulama Tipi: {sistem_turu}\n\n"
    f"*ALINACAK MALZEMELER:*\n"
    f"- Ana Boru: {t_boy}m {ana_cap} {pn_sinifi}\n"
    f"- Sulama Borusu: {ekipman_adi}\n"
    f"- Filtre: {filtre_notu}\n"
    f"- Ek Parçalar: {ek_parca}\n"
    f"------------------------------------\n"
    f"Hazırlayan: Ahmet Fikret Temeltaş"
)

encoded_msg = urllib.parse.quote(msg)
wa_link = f"https://wa.me/{telefon}?text={encoded_msg}"

st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-top: 20px;">
        <a href="{wa_link}" target="_blank" style="
            background-color: #25D366; color: white; padding: 20px 60px;
            text-decoration: none; font-size: 22px; font-weight: bold;
            border-radius: 15px; box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
        ">
            📩 LİSTEYİ WHATSAPP'TAN BİZE GÖNDER
        </a>
    </div>
    """, unsafe_allow_html=True)

st.write("\n\n")
st.caption("© 2026 Ahmet Fikret Temeltaş - Güvenilir Mühendislik")
