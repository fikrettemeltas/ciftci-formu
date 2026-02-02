import streamlit as st
import math

# --- GENİŞLETİLMİŞ MÜHENDİSLİK VERİTABANI ---
# su_ihtiyac_aylik: Nisan, Mayıs, Haziran, Temmuz, Ağustos, Eylül (mm/gün ortalama)
BITKI_VERILERI = {
    "Mısır": {
        "aralik": 0.70, "tip": "Damlama", 
        "takvim": {"Nisan": 3, "Mayıs": 5, "Haziran": 8, "Temmuz": 10, "Ağustos": 9, "Eylül": 4}
    },
    "Pancar": {
        "aralik": 0.45, "tip": "Damlama", 
        "takvim": {"Nisan": 2, "Mayıs": 4, "Haziran": 7, "Temmuz": 9, "Ağustos": 8, "Eylül": 5}
    },
    "Ayçiçeği": {
        "aralik": 0.70, "tip": "Damlama", 
        "takvim": {"Nisan": 2, "Mayıs": 4, "Haziran": 6, "Temmuz": 8, "Ağustos": 6, "Eylül": 3}
    },
    "Yonca": {
        "aralik": 12.0, "tip": "Yağmurlama", 
        "takvim": {"Nisan": 4, "Mayıs": 6, "Haziran": 9, "Temmuz": 11, "Ağustos": 10, "Eylül": 7}
    }
}

st.set_page_config(page_title="Ahmet Fikret Temeltaş | Akıllı Sulama", layout="wide")

# Başlık Paneli
st.markdown("<h1 style='text-align: center; color: #1B5E20;'>AHMET FİKRET TEMELTAŞ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold;'>PROFESYONEL PROJELENDİRME VE SULAMA TAKVİMİ SİSTEMİ</p>", unsafe_allow_html=True)
st.write("---")

# --- GİRİŞLER ---
with st.sidebar:
    st.header("📐 Arazi ve Su")
    tarla_eni = st.number_input("Sıra Uzunluğu / Tarla Eni (m)", value=200.0)
    tarla_boyu = st.number_input("Ana Boru Hattı / Tarla Boyu (m)", value=300.0)
    debi_ls = st.number_input("Mevcut Debi (L/s)", value=20.0)
    saatlik_ton = debi_ls * 3.6

    st.header("🌾 Ürün Seçimi")
    urun = st.selectbox("Ekilacak Ürün", list(BITKI_VERILERI.keys()))
    sistem = st.radio("Sistem", ["Damlama", "Yağmurlama"])

# --- MÜHENDİSLİK HESAPLARI ---
alan_donum = (tarla_eni * tarla_boyu) / 1000
v = BITKI_VERILERI[urun]

# 1. Boru ve Ekipman Hesabı
if sistem == "Damlama":
    sira_sayisi = tarla_boyu / v["aralik"]
    toplam_lateral = sira_sayisi * tarla_eni
    ekipman_notu = f"{toplam_lateral:,.0f} Metre Damlama Borusu"
    ana_cap = "90 mm" if debi_ls <= 22 else "110 mm"
else:
    tabanca_sayisi = (tarla_eni * tarla_boyu) / 144
    ekipman_notu = f"{int(tabanca_sayisi)} Adet Yağmurlama Tabancası"
    ana_cap = "110 mm" if debi_ls <= 25 else "125 mm"

# --- EKRAN TASARIMI ---
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📊 Sistem Analiz Raporu")
    st.success(f"📍 **Arazi:** {alan_donum:.1f} Dönüm")
    st.info(f"🏗️ **Ana Boru:** {tarla_boyu} Metre ({ana_cap})")
    st.info(f"🛠️ **Lateral:** {ekipman_notu}")
    
    # Vardiya Hesabı (En sıcak ay olan Temmuz'a göre)
    max_ihtiyac = v["takvim"]["Temmuz"]
    toplam_su_temmuz = alan_donum * max_ihtiyac
    vardiya_sayisi = math.ceil(toplam_su_temmuz / (saatlik_ton * 5)) # Günde 5 saat sulama varsayımıyla
    
    if vardiya_sayisi > 1:
        st.warning(f"⚠️ **DİKKAT:** Bu tarla tek seferde sulanamaz. Temmuz ayında tarlayı **{vardiya_sayisi} vardiyaya** bölmeniz gerekir.")
    else:
        st.success("✅ Mevcut debi tüm arazi için yeterlidir.")

with col2:
    st.subheader("📅 Aylık Sulama Takvimi")
    st.write("Aylara göre günlük çalışma süreleri (Tüm tarla için toplam):")
    
    # Takvim Tablosu Oluşturma
    takvim_data = []
    for ay, gunluk_mm in v["takvim"].items():
        gunluk_toplam_ton = alan_donum * gunluk_mm
        calisma_suresi = gunluk_toplam_ton / saatlik_ton
        # 3 günde bir sulama yapıldığı varsayımıyla periyot hesabı
        periyot_saati = calisma_suresi * 3
        takvim_data.append({"Ay": ay, "Günlük Su (Ton)": f"{gunluk_toplam_ton:.1f}", "Günlük Çalışma (Saat)": f"{calisma_suresi:.1f}"})
    
    st.table(takvim_data)
    st.caption("Not: Hesaplamalar bitkinin o aydaki ortalama su tüketimine göre yapılmıştır.")

# --- WHATSAPP GÖNDERİMİ ---
st.write("---")
if st.button("PROJEYİ VE TAKVİMİ WHATSAPP'A GÖNDER"):
    takvim_ozet = "\n".join([f"- {d['Ay']}: {d['Günlük Çalışma (Saat)']} sa/gün" for d in takvim_data])
    msg = (f"Sayın AHMET FİKRET TEMELTAŞ,\n\n"
           f"Analiz Sonucu:\n"
           f"Tarla: {alan_donum:.1f} Dönüm {urun}\n"
           f"Sistem: {sistem} / Ana Boru: {tarla_boyu}m {ana_cap}\n"
           f"Ekipman: {ekipman_notu}\n"
           f"Vardiya: {vardiya_sayisi}\n\n"
           f"SULAMA TAKVİMİ:\n{takvim_ozet}\n\n"
           f"Software Developed by AHMET FİKRET TEMELTAŞ")
    
    url = f"https://wa.me/905075031990?text={msg.replace(' ', '%20').replace('\n', '%0A')}"
    st.markdown(f'<a href="{url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: bold;">Projeyi WhatsApp Mesajı Olarak Onayla</a>', unsafe_allow_html=True)

st.write("\n\n")
st.markdown("---")
st.markdown("<p style='text-align: center;'>© 2026 Ahmet Fikret Temeltaş - Mühendislik Yazılımları</p>", unsafe_allow_html=True)

