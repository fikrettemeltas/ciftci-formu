import streamlit as st
import urllib.parse

# SAYFA AYARLARI
st.set_page_config(page_title="Çiftçi Destek Sistemi", page_icon="🚜")

st.title("🚜 Çiftçi Proje Destek Formu")
st.write("Bilgileri doldurun, WhatsApp üzerinden size dönüş yapalım.")

# FORM ALANLARI
isim = st.text_input("Ad Soyad")
ilce = st.text_input("İlçe / Köy")
ada = st.text_input("Ada")
parsel = st.text_input("Parsel")
urun = st.text_input("Ekili Ürün")
sulama = st.selectbox("İstenen Sulama Sistemi", ["Damlama", "Yağmurlama", "Pivot", "Güneş Enerjisi"])

# GÖNDERME BUTONU
if st.button("BİLGİLERİ GÖNDER VE SORU SOR"):
    if isim and ilce:
        # Mesajı hazırlıyoruz
        mesaj = (f"Merhaba, ben {isim}. {ilce} ilçesi, {ada} ada, {parsel} parseldeki yerim için "
                 f"{urun} ekimi ve {sulama} sistemi hakkında bilgi almak istiyorum.")
        
        # BURAYI KENDİ NUMARANLA DEĞİŞTİR (Başına 90 koy, boşluk bırakma)
        tel = "905075031990" 
        
        # WhatsApp Linkini oluşturuyoruz
        mesaj_kodlu = urllib.parse.quote(mesaj)
        wa_link = f"https://wa.me/{tel}?text={mesaj_kodlu}"
        
        # Kullanıcıya yönlendirme mesajı veriyoruz
        st.success("Bilgiler hazırlandı! WhatsApp'a yönlendiriliyorsunuz...")
        
        # Linki şık bir buton şeklinde gösteriyoruz
        st.markdown(f'''
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #25D366; color: white; padding: 10px 20px; text-align: center; border-radius: 5px; font-weight: bold;">
                    WhatsApp'ı Aç ve Mesajı Gönder
                </div>
            </a>
            ''', unsafe_allow_html=True)
    else:
        st.error("Lütfen en azından İsim ve İlçe bölümlerini doldurun!")

