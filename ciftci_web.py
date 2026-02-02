import streamlit as st
import webbrowser

# --- BITKI VE MUHENDISLIK VERILERI ---
BITKI_VERILERI = {
    "Misir": {"aralik": 0.70, "su_ihtiyac": 8, "tip": "Damlama"},
    "Aycicegi": {"aralik": 0.70, "su_ihtiyac": 6, "tip": "Damlama"},
    "Pancar": {"aralik": 0.45, "su_ihtiyac": 7, "tip": "Damlama"},
    "Yonca": {"aralik": 12, "su_ihtiyac": 9, "tip": "Yagmurlama"},
    "Bugday": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yagmurlama"},
    "Arpa": {"aralik": 12, "su_ihtiyac": 5, "tip": "Yagmurlama"}
}

# --- WEB ARAYUZU (STREAMLIT) ---
st.set_page_config(page_title="Ahmet Fikret Temeltas - Proje", page_icon="💧")

st.title("AHMET FIKRET TEMELTAS")
st.subheader("Akilli Sulama Proje Formu")

# Girdiler
isim = st.text_input("Ciftci Ad Soyad")
ilce = st.text_input("Ilce / Koy")
urun = st.selectbox("Ekilecek Urun", list(BITKI_VERILERI.keys()))
alan = st.number_input("Tarla Alani (Donum)", min_value=1.0, step=1.0)

# Belge Yukleme (Web uyumlu)
st.write("### Evrak Yukleme")
col1, col2, col3 = st.columns(3)
with col1: st.file_uploader("CKS Belgesi", type=['pdf', 'jpg', 'png'])
with col2: st.file_uploader("Kuyu Ruhsati", type=['pdf', 'jpg', 'png'])
with col3: st.file_uploader("Tapu Fotokopisi", type=['pdf', 'jpg', 'png'])

# Hesaplama Motoru
if alan > 0:
    v = BITKI_VERILERI[urun]
    sabit_debi = 72 # 20 L/s
    
    # Boru Hesabi
    if v["tip"] == "Damlama":
        metraj = (1000 / v["aralik"]) * alan
        birim = f"{metraj:,.0f} Metre Damlama Borusu"
    else:
        tabanca = (alan * 1000) / 144
        birim = f"{tabanca:,.0f} Adet Yagmurlama Tabancasi"
    
    # Su Hesabi
    gunluk_su = alan * v["su_ihtiyac"]
    sure = gunluk_su / sabit_debi

    st.info(f"""
    **TEKNIK ANALIZ RAPORU**
    * **Urun:** {urun}
    * **Sistem:** {v['tip']}
    * **Ihtiyac:** {birim}
    * **Gunluk Su Tuketimi:** {gunluk_su:.1f} Ton
    * **Sulama Suresi:** {sure:.1f} Saat (20 L/s debi ile)
    """)

    # WhatsApp Butonu
    mesaj = (f"Sayin AHMET FIKRET TEMELTAS,\n\n"
             f"Ben {isim}. {ilce} bolgesindeki {alan} donum {urun} arazim icin destek istiyorum.\n\n"
             f"Analiz: {birim}, {gunluk_su} ton su ihtiyaci.\n\n"
             f"Software Developed by AHMET FIKRET TEMELTAS")
    
    whatsapp_url = f"https://wa.me/905075031990?text={mesaj.replace(' ', '%20')}"
    
    if st.button("PROJEYI WHATSAPP'A GONDER"):
        st.markdown(f'<a href="{whatsapp_url}" target="_blank">Buraya tiklayarak WhatsApp mesajini gonderin</a>', unsafe_allow_html=True)

# Alt Bilgi
st.markdown("---")
st.caption("Software Developed by Ahmet Fikret Temeltas")

