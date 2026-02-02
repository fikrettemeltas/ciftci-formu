import streamlit as st
import math

# --- BITKI VERİTABANI ---
BITKI_VERILERI = {
    "Mısır": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Ayçiçeği": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Yonca": {"aralik": 12.0, "su_ihtiyac": 9, "tip": "Yağmurlama"},
    "Buğday": {"aralik": 12.0, "su_ihtiyac": 5, "tip": "Yağmurlama"}
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş | Profesyonel Proje", layout="wide")

# Marka ve Başlık
st.markdown("<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>SULAMA PROJELENDİRME VE TEKNİK ŞARTNAME SİSTEMİ</p>", unsafe_allow_html=True)
st.write("---")

# --- 1. BÖLÜM: KİMLİK VE KONUM BİLGİLERİ ---
st.subheader("👤 Müşteri ve Arazi Bilgileri")
col_kimlik1, col_kimlik2, col_kimlik3 = st.columns(3)

with col_kimlik1:
    ad_soyad = st.text_input("Ad Soyad")
    ilce = st.text_input("İlçe")

with col_kimlik2:
    koy = st.text_input("Köy / Mahalle")
    ada = st.text_input("Ada No")

with col_kimlik3:
    parsel = st.text_input("Parsel No")
    telefon = st.text_input("WhatsApp No (Örn: 905075031990)", value="905075031990")

st.write("---")

# --- 2. BÖLÜM: TEKNİK GİRİŞLER ---
st.subheader("⚙️ Sistem ve Arazi Ölçüleri")
col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    sistem_turu = st.radio("Uygulanacak Sistem", ["Damlama Sulama", "Yağmurlama Sulama"])
    urun = st.selectbox("Ekilecek Ürün", list(BITKI_VERILERI.keys()))

with col_input2:
    t_en = st.number_input("Sıra Uzunluğu (Tarla Eni - m)", value=200.0)
    t_boy = st.number_input("Ana Boru Hattı (Tarla Boyu - m)", value=300.0)

with col_input3:
    debi = st.number_input("Su Kaynağı Debisi (L/s)", value=20.0)
    pn_sinifi = st.selectbox("Boru Basınç Sınıfı", ["PN6", "PN10"])

# --- HESAPLAMA MOTORU ---
v = BITKI_VERILERI[urun]
alan_donum = (t_en * t_boy) / 1000
saatlik_ton = debi * 3.6

# Ana Boru Çapı Kararı
if debi <= 18: ana_cap = "90 mm"
elif debi <= 32: ana_cap = "110 mm"
else: ana_cap = "125 mm"

# Sistem Detayları
if "Damlama" in sistem_turu:
    sira_sayisi = t_boy / v["aralik"]
    lateral_metraj = sira_sayisi * t_en
    ekipman = f"{lateral_metraj:,.0f} Metre Damlama Borusu"
    ek_parca = f"{int(sira_sayisi)} Adet Çıkış Nipeli ve Conta"
    filtre = "3\" Otomatik Disk Filtre"
else:
    tabanca = (t_en * t_boy) / 144
    ekipman = f"{int(tabanca)} Adet Yağmurlama Tabancası"
    ek_parca = f"{int(t_boy/6)} Adet 6m Boru ve Abot"
    filtre = "3\" Hidrosiklon + Disk Filtre"

# --- 3. BÖLÜM: SONUÇLAR VE WHATSAPP ---
st.write("---")
st.subheader("📋 Teknik Şartname Özeti")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.info(f"📍 **Konum:** {ilce} / {koy} (Ada: {ada}, Parsel: {parsel})")
    st.write(f"🚜 **Alan:** {alan_donum:.1f} Dönüm")
    st.write(f"🏗️ **Ana Hat:** {t_boy}m {ana_cap} {pn_sinifi}")

with res_col2:
    st.success(f"🛠️ **Malzeme:** {ekipman}")
    st.write(f"🔩 **Ek Parça:** {ek_parca}")
    st.write(f"🧪 **Filtre:** {filtre}")

# --- WHATSAPP MESAJ OLUŞTURUCU ---
whatsapp_mesaji = (
    f"*SULAMA PROJESİ TEKNİK ŞARTNAMESİ*\n"
    f"------------------------------------\n"
    f"*MÜŞTERİ:* {ad_soyad}\n"
    f"*KONUM:* {ilce} / {koy}\n"
    f"*TAPU:* Ada: {ada} / Parsel: {parsel}\n"
    f"------------------------------------\n"
    f"*ARAZİ DETAYI:*\n"
    f"- Alan: {alan_donum:.1f} Dönüm\n"
    f"- Ürün: {urun}\n"
    f"- Sistem: {sistem_turu}\n\n"
    f"*MALZEME LİSTESİ:*\n"
    f"- Ana Boru: {t_boy}m {ana_cap} {pn_sinifi}\n"
    f"- Lateral: {ekipman}\n"
    f"- Filtre: {filtre}\n"
    f"- Ek Parçalar: {ek_parca}\n"
    f"------------------------------------\n"
    f"*Software Developed by Ahmet Fikret Temeltaş*"
)

# Link oluşturma
encoded_msg = whatsapp_mesaji.replace('\n', '%0A').replace(' ', '%20').replace('*', '%2A')
wa_url = f"https://wa.me/{telefon}?text={encoded_msg}"

st.write("\n")
st.markdown(f'''
    <a href="{wa_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #25D366; color: white; padding: 18px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 20px;">
            🚀 PROJEYİ VE ŞARTNAMEYİ WHATSAPP'A GÖNDER
        </div>
    </a>
''', unsafe_allow_html=True)

st.write("\n\n")
st.caption("© 2026 Ahmet Fikret Temeltaş | Tüm Hakları Saklıdır.")
