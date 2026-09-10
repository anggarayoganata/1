import streamlit as st
import re

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Pemilah Real Food vs Junk Food",
    page_icon="🥗",
    layout="wide"
)

# =============================================================================
# 1. DATABASE KOSAKATA MASTER & POLA REGEX (MULTI-LAYER)
# =============================================================================

# LAPIS 1: Database Kata Kunci Spesifik (NOVA 4)
DATABASE_BTP_NOVA4 = {
    "Antioksidan Sintetis & Pengawet Minyak": {
        "keywords": [
            "tbhq", "tertiary butylhydroquinone", "tersier butil hidrokuinon", "e319",
            "bha", "butylated hydroxyanisole", "butil hidroksi anisol", "e320",
            "bht", "butylated hydroxytoluene", "butil hidroksi toluen", "e321",
            "propil galat", "propyl gallate", "e310", "askorbil palmitat", "ascorbyl palmitate"
        ],
        "fungsi": "Antioksidan Lemak/Minyak Industri",
        "efek": "Beban kerja organ hati, potensi mual/pusing jika sensitif, dan stres oksidatif."
    },
    "Pengawet Sintetis (Benzoat/Sorbat/Sulfit/Propionat)": {
        "keywords": [
            "benzoat", "benzoate", "sodium benzoate", "natrium benzoat", "e211",
            "kalium sorbat", "potassium sorbate", "sorbat", "sorbic acid", "e202", "e200",
            "sulfit", "sulfite", "metabisulfit", "natrium metabisulfit", "e220", "e221", "e223",
            "propionat", "calcium propionate", "kalsium propionat", "e280", "e282", "pengawet"
        ],
        "fungsi": "Pengawet Anti-Jamur & Bakteri Pabrik",
        "efek": "Potensi reaksi alergi, iritasi lambung, dan pemicu hiperaktivitas anak."
    },
    "Pengawet Daging Olahan (Nitrit & Nitrat)": {
        "keywords": [
            "nitrit", "nitrat", "sodium nitrite", "natrium nitrit", "kalium nitrat", "sodium nitrate", "e249", "e250", "e251"
        ],
        "fungsi": "Pengawet & Pewarna Daging Olahan",
        "efek": "Membentuk senyawa nitrosamin yang berpotensi karsinogenik jika dikonsumsi berlebih."
    },
    "Pengembang Kimia & Garam Pabrik": {
        "keywords": [
            "amonium bikarbonat", "ammonium bicarbonate", "amonium hidrogen karbonat", "e503",
            "natrium bikarbonat", "sodium bicarbonate", "e500",
            "natrium asam pirofosfat", "disodium pyrophosphate", "e450",
            "kalsium karbonat", "kalsium fosfat", "trikalsium fosfat", "e341", "e551", "amonium klorida"
        ],
        "fungsi": "Pengembang Kimia & Garam Anorganik Pabrik",
        "efek": "Dapat memicu iritasi saluran cerna ringan bagi lambung sensitif."
    },
    "Penguat Rasa Sintetis (MSG & Nukleotida)": {
        "keywords": [
            "msg", "monosodium", "mononatrium", "glutamat", "monosodium glutamate", "mononatrium glutamat", "e621",
            "disodium inosinate", "dinatrium inosinat", "e631", "dinatrium guanilat", "disodium guanylate", "e627",
            "d-inosinat", "d-guanilat", "e635", "hsv", "hvp", "hidrolisat", "hidrolisa", "protein terhidrolisis",
            "hydrolyzed vegetable protein", "hydrolyzed soy protein", "ekstrak ragi", "yeast extract", "bumbu tabur"
        ],
        "fungsi": "Penguat Rasa Gurih (Umami) Industri",
        "efek": "Pemicu pusing/sakit kepala ringan, leher kaku, dan haus berlebihan pada individu sensitif."
    },
    "Pemanis Buatan & Sugar Alcohol": {
        "keywords": [
            "pemanis buatan", "pemanis sintetik", "pemanis sintetis", "aspartam", "aspartame", "e951",
            "asesulfam", "acesulfame", "acesulfame-k", "e950", "sakarin", "saccharin", "e954",
            "siklamat", "cyclamate", "e952", "sukralosa", "sucralose", "e955", "neotame", "alitame",
            "sorbitol", "maltitol", "mannitol", "xylitol", "isomalt", "lactitol", "erythritol"
        ],
        "fungsi": "Pemanis Sintetis Kimia",
        "efek": "Gangguan toleransi glukosa dan potensi perubahan mikrobioma/bakteri baik di usus."
    },
    "Gula Terolah Tinggi & Sirup Industri": {
        "keywords": [
            "fruktosa", "hfcs", "high fructose corn syrup", "sirup jagung", "sirup glukosa",
            "dekstrosa", "dextrose", "maltodekstrin", "maltodextrin", "gula invert", "sirup invert", "polidextrosa"
        ],
        "fungsi": "Pemanis Industri Terolah Tinggi",
        "efek": "Meningkatkan risiko perlemakan hati (fatty liver), obesitas, dan resistensi insulin."
    },
    "Pewarna Sintetis & Karamel Industri": {
        "keywords": [
            "pewarna sintetik", "pewarna sintetis", "pewarna artifisial", "tartrazin", "tartrazine", "e102",
            "kuning fcf", "sunset yellow", "e110", "merah allura", "allura red", "e129",
            "biru berlian", "brilliant blue", "e133", "karmoisin", "carmoisine", "e122",
            "eritrosin", "erythrosine", "e127", "ponceau 4r", "e124", "karamel iii", "karamel iv", "e150c", "e150d"
        ],
        "fungsi": "Pewarna Makanan Sintetis / Karamel Olahan",
        "efek": "Pemicu reaksi alergi kulit, gatal, asma, dan hiperaktivitas pada anak."
    },
    "Pengemulsi, Penstabil & Pengental Texturizer": {
        "keywords": [
            "pengemulsi", "emulsifier", "penstabil", "stabilizer", "pengental", "thickener",
            "karagenan", "carrageenan", "e407", "xanthan gum", "e415", "guar gum", "e412",
            "gum arab", "karaya gum", "konjac gum", "lesitin", "lecithin", "lesitin kedelai", "soy lecithin", "e322",
            "mono dan digliserida", "mono- and diglycerides", "e471", "polisorbat", "polysorbate", "e433",
            "pati termodifikasi", "modified starch", "modified food starch", "e1422",
            "cmc", "karboksimetil selulosa", "e466", "mikrokristalin selulosa", "propilen glikol"
        ],
        "fungsi": "Pengental, Pengemulsi & Penstabil Tekstur",
        "efek": "Potensi mengganggu keseimbangan pencernaan dan memicu peradangan usus jika berlebih."
    },
    "Minyak Industri & Produk Olahan Pabrik": {
        "keywords": [
            "minyak terhidrogenasi", "hydrogenated oil", "minyak nabati terhidrogenasi", "margarin", "margarine",
            "shortening", "lemak rekonstitusi", "krimer", "krimer kental manis", "krimer nabati", "non-dairy creamer",
            "whey protein isolate", "isolat protein soya", "sosis", "nugget", "kornet", "chiki", "biskuit", "wafer",
            "permen", "marshmallow", "soda", "minuman bersoda", "mi instan", "mie instan"
        ],
        "fungsi": "Lemak Olahan Industri & Produk Ultra-Processed",
        "efek": "Mengandung lemak trans/jenuh yang memicu kenaikan kolesterol jahat (LDL) & penyakit jantung."
    }
}

# DATABASE NOVA 3 (Olahan Dapur)
KATA_NOVA3 = [
    "garam", "gula", "gula pasir", "gula jawa", "gula merah", "gula aren", "minyak goreng", "minyak kelapa",
    "minyak zaitun", "mentega", "keju", "cuka", "ragi", "ikan kaleng", "sardines", "sardin", "manisan buah",
    "ikan asin tradisional", "telur asin", "roti tawar rumahan", "tauco", "terasi", "kecap manis", "kecap asin",
    "bubuk kecap", "serpihan kentang", "tepung tapioka", "tapioka"
]

# DATABASE NOVA 1 (Bahan Alami)
KATA_NOVA1_ALAMI = [
    "bayam", "kangkung", "sawi", "kubis", "kol", "brokoli", "wortel", "buncis", "kacang panjang", "terong",
    "oyong", "labu", "daun singkong", "seledri", "tomat", "timun", "jamur", "rumput laut", "kurkumin",
    "apel", "pisang", "jeruk", "mangga", "alpukat", "pepaya", "nanas", "semangka", "melon", "anggur",
    "stroberi", "buah naga", "durian", "salak", "kelapa", "lemon", "singkong", "ubi", "kentang", "talas",
    "beras", "ketan", "jagung", "gandum utuh", "oat", "sagu", "telur", "daging sapi", "daging ayam",
    "ikan", "udang", "cumi", "susu murni", "kedelai", "kacang tanah", "kacang hijau", "almond", "segar", "murni"
]

# =============================================================================
# 2. FUNGSI DETEKSI LAPISAN REGEX (LAPIS 2 & LAPIS 3)
# =============================================================================
def deteksi_pola_regex(teks):
    temuan_pola = []
    
    # LAPIS 2: Deteksi Pola Kode Angka (CI / E-Number)
    pola_ci = re.findall(r'\bci\.?\s*(?:no\.?)?\s*\d{5}\b', teks)
    pola_e_num = re.findall(r'\be\d{3}[a-z]?\b', teks)
    
    if pola_ci:
        temuan_pola.append({
            "nama": "Pewarna Kode CI (International Color Index)",
            "kata_kunci": ", ".join(set(pola_ci)),
            "fungsi": "Pewarna Makanan Industri (Kode Standar)",
            "efek": "Berpotensi memicu reaksi alergi kulit, gatal, atau hiperaktivitas jika berlebih."
        })
        
    if pola_e_num:
        temuan_pola.append({
            "nama": "BTP Kode E-Number (Standar Internasional Codex)",
            "kata_kunci": ", ".join(set(pola_e_num)),
            "fungsi": "Bahan Tambahan Pangan Sintetis Terdaftar",
            "efek": "Indikasi bahan aditif olahan pabrik berstandar industri."
        })
        
    # LAPIS 3: Deteksi Awalan/Akhiran Istilah Kimia
    pola_awalan_kimia = re.findall(r'\b(dinatrium|mononatrium|kalium|kalsium|amonium|natrium)\s+[a-z]+\b', teks)
    pola_sintetik = re.findall(r'\b[a-z]+ (sintetis|sintetik|artifisial)\b', teks)
    
    if pola_awalan_kimia and not pola_e_num:
        temuan_pola.append({
            "nama": "Senyawa Garam/Anorganik Industri",
            "kata_kunci": ", ".join(set(pola_awalan_kimia)),
            "fungsi": "Penguat Rasa / Pengemulsi / Penstabil Kimia",
            "efek": "Konsumsi berlebih dapat memicu iritasi pencernaan atau beban ginjal."
        })
        
    if pola_sintetik:
        temuan_pola.append({
            "nama": "Perisa / Pewarna Sintetis Tambahan",
            "kata_kunci": ", ".join(set(pola_sintetik)),
            "fungsi": "Perisa/Pewarna Artifisial Pabrik",
            "efek": "Pemicu sensitivitas dan reaksi alergi pada sebagian individu."
        })
        
    return temuan_pola

# =============================================================================
# 3. SIDEBAR & INTERFACE
# =============================================================================
with st.sidebar:
    st.header("💡 Panduan Skala NOVA")
    st.markdown("""
    Sistem klasifikasi pangan internasional **WHO/FAO**:
    * 🟢 **NOVA 1 (Real Food):** Murni alami / minimal olahan.
    * 🟡 **NOVA 3 (Processed):** Olahan dapur umum (garam/gula/minyak).
    * 🔴 **NOVA 4 (Ultra-Processed):** Produk pabrikasi beraditif sintetis (Junk Food).
    """)
    st.divider()
    st.subheader("🧪 Contoh Teks Demo")
    if st.button("📌 Contoh Snack Rumput Laut (Foto)"):
        st.session_state["input_teks"] = "Minyak nabati (mengandung Antioksidan TBHQ), Tepung terigu, Tepung Tapioka, Serpihan Kentang, Antioksidan Askorbil Palmitat, Pewarna Alami Kurkumin CI. No. 75300, Dinatrium Inosinat, Dinatrium Guanilat, Pewarna Karamel III E150c, Penstabil Kalsium Karbonat, Mononatrium Glutamat, Pewarna Sintetik Kuning FCF CI. No. 15985."
    if st.button("📌 Contoh Buah Segar (NOVA 1)"):
        st.session_state["input_teks"] = "Apel fuji segar, pisang raja murni, alpukat mentah, dan air kelapa murni tanpa gula."

st.title("🥗 Pemilah Real Food vs Junk Food")
st.write("Aplikasi cerdas berbasis **Sistem Deteksi 3 Lapis (Keywords + E-Number + Pattern Regex)** untuk memilah makanan secara presisi.")

tab1, tab2 = st.tabs(["📝 Input Teks / Komposisi", "📷 Upload Foto Kemasan (OCR)"])

teks_analisis = ""

with tab1:
    default_val = st.session_state.get("input_teks", "")
    teks_input = st.text_area(
        "Ketik atau tempelkan teks komposisi makanan di sini:",
        value=default_val,
        height=180,
        placeholder="Contoh: Tepung terigu, gula, minyak nabati, pengembang amonium bikarbonat, perisa sintetis vanila..."
    )
    if teks_input:
        teks_analisis = teks_input

with tab2:
    uploaded_file = st.file_uploader("Upload Foto Kemasan Makanan (.jpg / .png)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Foto Kemasan yang Diupload", use_container_width=True)
        try:
            import easyocr
            from PIL import Image
            import numpy as np

            st.info("🔄 Membaca teks dari foto (OCR)...")
            reader = easyocr.Reader(['id', 'en'], gpu=False)
            image = Image.open(uploaded_file)
            results = reader.readtext(np.array(image), detail=0)
            teks_analisis = " ".join(results)
            st.success("✅ Teks berhasil diekstrak dari gambar!")
            st.text_area("Hasil Pembacaan Teks:", value=teks_analisis, height=120)
        except ImportError:
            st.warning("⚠️ Pustaka EasyOCR belum terpasang di server. Gunakan tab 'Input Teks / Komposisi' untuk menganalisis.")

# =============================================================================
# 4. ESEKUSI PEMILAHAN 3 LAPIS
# =============================================================================
if st.button("🔍 Analisis Makanan Ini", type="primary"):
    if not teks_analisis.strip():
        st.warning("⚠️ Harap masukkan teks komposisi atau upload foto kemasan terlebih dahulu, Cak!")
    else:
        st.divider()
        teks_lower = teks_analisis.lower()

        # LAPIS 1: Deteksi Keyword Spesifik
        btp_terdeteksi = []
        skor_kesehatan = 100

        for nama_btp, detail in DATABASE_BTP_NOVA4.items():
            terdeteksi = [kw for kw in detail["keywords"] if kw in teks_lower]
            if terdeteksi:
                btp_terdeteksi.append({
                    "nama": nama_btp,
                    "kata_kunci": ", ".join(list(set(terdeteksi))),
                    "fungsi": detail["fungsi"],
                    "efek": detail["efek"]
                })
                skor_kesehatan -= 15

        # LAPIS 2 & 3: Deteksi Regex Pattern (E-Number, CI, Awalan Kimia)
        temuan_regex = deteksi_pola_regex(teks_lower)
        for temuan in temuan_regex:
            # Cegah duplikasi jika sudah terdeteksi di Lapis 1
            if not any(t["nama"] == temuan["nama"] for t in btp_terdeteksi):
                btp_terdeteksi.append(temuan)
                skor_kesehatan -= 10

        # Deteksi Bahan NOVA 3 & NOVA 1
        nova3_terdeteksi = list(set([kata for kata in KATA_NOVA3 if kata in teks_lower]))
        nova1_terdeteksi = list(set([kata for kata in KATA_NOVA1_ALAMI if kata in teks_lower]))

        if nova3_terdeteksi and not btp_terdeteksi:
            skor_kesehatan = 75

        skor_kesehatan = max(0, min(100, skor_kesehatan))

        # Tampilan Hasil
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(label="📊 Skor Kesehatan Makanan", value=f"{skor_kesehatan} / 100")
            st.progress(skor_kesehatan / 100)

        with col2:
            if btp_terdeteksi or skor_kesehatan < 60:
                st.error("🔴 **Kategori: NOVA 4 — Ultra-Processed Food (Junk Food)**")
                st.write("**Kesimpulan:** Makanan ini mengandung aditif buatan pabrik dan telah melalui pengolahan industri tinggi.")
                st.warning("💡 **Saran:** Batasi konsumsi! Maksimal 1–2 kali seminggu.")
            elif nova3_terdeteksi and not btp_terdeteksi:
                st.warning("🟡 **Kategori: NOVA 3 — Processed Food (Olahan Sederhana)**")
                st.write(f"**Bahan Olahan Terdeteksi:** `{', '.join(nova3_terdeteksi)}`")
                st.write("**Kesimpulan:** Makanan diolah dengan bahan dasar dapur umum tanpa aditif buatan pabrik.")
                st.info("💡 **Saran:** Aman dikonsumsi wajar sebagai lauk harian.")
            elif nova1_terdeteksi and not btp_terdeteksi and not nova3_terdeteksi:
                st.success("🟢 **Kategori: NOVA 1 — Real Food (Makanan Alami)**")
                st.write(f"**Bahan Alami Terdeteksi:** `{', '.join(nova1_terdeteksi)}`")
                st.write("**Kesimpulan:** Makanan terbuat dari bahan alami murni tanpa aditif buatan.")
                st.info("💡 **Saran:** Sangat sehat untuk dikonsumsi harian!")
            else:
                st.info("🟡 **Kategori: NOVA 3 / Uncategorized (Olahan Sedang)**")
                st.write("**Kesimpulan:** Tidak terdeteksi aditif berat, kemungkinan makanan olahan biasa.")

        # Tabel Efek Samping
        if btp_terdeteksi:
            st.subheader("⚠️ Rincian Bahan Aditif Terdeteksi & Catatan Kesehatan")
            tabel_md = "| Kelompok / Jenis BTP | Kata Kunci / Kode Terdeteksi | Fungsi Industri | Potensi Efek Samping (Jika Berlebihan) |\n"
            tabel_md += "| :--- | :--- | :--- | :--- |\n"
            for btp in btp_terdeteksi:
                tabel_md += f"| **{btp['nama']}** | `{btp['kata_kunci']}` | {btp['fungsi']} | {btp['efek']} |\n"
            st.markdown(tabel_md)