import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Pemilah Real Food vs Junk Food",
    page_icon="🥗",
    layout="wide"
)

# =============================================================================
# 1. DATABASE KOSAKATA MASTER TERLENGKAP
# =============================================================================

# A. DATABASE NOVA 4 (Ultra-Processed / Aditif Sintetis & Industri)
DATABASE_BTP_NOVA4 = {
    "Antioksidan Sintetis & Pengawet Minyak": {
        "keywords": [
            "tbhq", "tertiary butylhydroquinone", "tersier butil hidrokuinon", "e319",
            "bha", "butylated hydroxyanisole", "butil hidroksi anisol", "e320",
            "bht", "butylated hydroxytoluene", "butil hidroksi toluen", "e321",
            "propil galat", "propyl gallate", "e310", "tokoferol campuran pekat"
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
            "amonium bikarbonat", "ammonium bicarbonate", "amonium hidrogen karbonat", "e503", "e503(i)", "e503(ii)",
            "natrium bikarbonat", "sodium bicarbonate", "e500", "e500(i)", "e500(ii)",
            "natrium asam pirofosfat", "disodium pyrophosphate", "e450", "e450(i)",
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
            "sorbitol", "maltitol", "mannitol", "xylitol", "isomalt", "lactitol", "erythritol",
            "e965", "e967", "e968"
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
    "Pewarna Sintetis (Nama & Kode CI / E-Number)": {
        "keywords": [
            "pewarna sintetik", "pewarna sintetis", "pewarna artifisial", "tartrazin", "tartrazine", "e102", "ci 19140",
            "kuning fcf", "sunset yellow", "e110", "ci 15985", "merah allura", "allura red", "e129", "ci 16035",
            "biru berlian", "brilliant blue", "e133", "ci 42090", "karmoisin", "carmoisine", "e122", "ci 14720",
            "eritrosin", "erythrosine", "e127", "ci 45430", "ponceau 4r", "e124", "ci 16255",
            "indigotin", "indigo carmine", "e132", "ci 73015", "fast green fcf"
        ],
        "fungsi": "Pewarna Makanan Sintetis Industri",
        "efek": "Pemicu reaksi alergi kulit, gatal, asma, dan hiperaktivitas pada anak."
    },
    "Pengemulsi, Penstabil & Pengental Texturizer": {
        "keywords": [
            "pengemulsi", "emulsifier", "penstabil", "stabilizer", "pengental", "thickener",
            "karagenan", "carrageenan", "e407", "xanthan gum", "e415", "guar gum", "e412",
            "gum arab", "karaya gum", "konjac gum", "lesitin", "lecithin", "lesitin kedelai", "soy lecithin", "e322",
            "mono dan digliserida", "mono- and diglycerides", "e471", "polisorbat", "polysorbate", "e433",
            "pati termodifikasi", "modified starch", "modified food starch", "e1422",
            "cmc", "carboxymethyl cellulose", "karboksimetil selulosa", "e466",
            "mikrokristalin selulosa", "microcrystalline cellulose", "propilen glikol", "gliserol", "triasetin"
        ],
        "fungsi": "Pengental, Pengemulsi & Penstabil Tekstur",
        "efek": "Potensi mengganggu keseimbangan pencernaan dan memicu peradangan usus halus jika berlebih."
    },
    "Minyak Industri & Produk Olahan Pabrik": {
        "keywords": [
            "minyak terhidrogenasi", "hydrogenated oil", "minyak nabati terhidrogenasi", "margarin", "margarine",
            "shortening", "lemak rekonstitusi", "interesterifikasi", "krimer", "krimer kental manis",
            "krimer nabati", "non-dairy creamer", "whey protein isolate", "konsentrat protein", "isolat protein soya",
            "sosis", "nugget", "kornet", "chiki", "snack kemasan", "biskuit", "wafer", "permen", "marshmallow",
            "soda", "minuman bersoda", "soft drink", "sirup kemasan", "mi instan", "mie instan"
        ],
        "fungsi": "Lemak Olahan Industri & Produk Ultra-Processed",
        "efek": "Mengandung lemak trans/jenuh yang memicu kenaikan kolesterol jahat (LDL) & penyakit kardiovaskular."
    }
}

# B. DATABASE NOVA 3 (Processed Food / Olahan Dapur Umum)
KATA_NOVA3 = [
    "garam", "gula", "gula pasir", "gula jawa", "gula merah", "gula aren", "minyak goreng", "minyak kelapa",
    "minyak zaitun", "mentega", "keju", "keju cheddar", "cuka", "ragi", "ikan kaleng", "sardines", "sardin",
    "kornet daging dapur", "manisan buah", "ikan asin tradisional", "telur asin", "roti tawar rumahan",
    "kacang sangrai", "kacang asin", "jamu tradisional", "tauco", "terasi", "kecap manis", "kecap asin"
]

# C. DATABASE NOVA 1 (Real Food / Makanan Alami)
KATA_NOVA1_ALAMI = [
    # Sayur & Dedaunan
    "bayam", "bayam hijau", "bayam merah", "kangkung", "sawi", "sawi hijau", "sawi putih", "pokcoy", "pakcoy", 
    "kubis", "kol", "brokoli", "kembang kol", "wortel", "buncis", "kacang panjang", "kapri", "terong", "gambas", 
    "oyong", "labu siam", "labu kuning", "waluh", "daun singkong", "daun pepaya", "daun katuk", "daun kelor", 
    "daun kemangi", "daun seledri", "daun bawang", "prei", "seledri", "caisim", "kale", "asparagus", "lobak", 
    "bit", "genjer", "pakis", "kecipir", "pare", "rebung", "tauge", "taoge", "kecambah", "leunca", "kenikir", 
    "pohpohan", "jamur tiram", "jamur kancing", "jamur kuping", "jamur enoki", "jamur shiitake", "jamur merang",
    
    # Buah-Buahan
    "apel", "pisang", "jeruk", "mangga", "alpukat", "pepaya", "nanas", "semangka", "melon", "anggur", 
    "stroberi", "strawberry", "buah naga", "durian", "rambutan", "duku", "kelengkeng", "lengkeng", "jambu", 
    "salak", "srikaya", "sirsak", "manggis", "sawo", "kedondong", "kiwi", "pir", "pear", "delima", "kurma", 
    "zaitun", "plum", "ceri", "cherry", "blueberry", "raspberry", "blackberry", "markisa", "belimbing", 
    "mentimun", "timun", "tomat", "lemon", "jeruk nipis", "jeruk purut", "jeruk limau", "kelapa", "daging kelapa", "air kelapa",
    
    # Umbi & Karbohidrat Alami
    "singkong", "ubi", "ubi jalar", "ubi ungu", "ubi cilembu", "ubi kayu", "ketela", "talas", "kentang", 
    "gembili", "garut", "ganyong", "bentul", "porang", "konjac", "suweg", "beras", "beras putih", "beras merah", 
    "beras hitam", "beras cokelat", "ketan", "ketan hitam", "jagung", "jagung manis", "gandum utuh", "oat", 
    "oatmeal", "jelai", "barley", "quinoa", "sagu", "sorghum", "sorgum", "chia seed", "kuaci", "wijen",
    
    # Protein & Lauk Segar
    "telur", "telur ayam", "telur bebek", "telur puyuh", "daging", "daging sapi", "daging kambing", "daging domba", 
    "daging ayam", "daging bebek", "iga", "hati", "ampela", "paru", "babat", "kikil", "ikan", "ikan lele", 
    "ikan gurame", "ikan nila", "ikan mas", "ikan bandeng", "ikan tongkol", "ikan cakalang", "ikan tuna", 
    "ikan kembung", "ikan teri", "salmon", "udang", "cumi", "kepiting", "kerang", "gurita", "lobster", 
    "susu", "susu murni", "susu segar", "kedelai", "kacang tanah", "kacang hijau", "kacang merah", "kacang mede", 
    "kacang mente", "kacang almond", "walnut", "pistachio", "segar", "mentah", "murni"
]

# =============================================================================
# 2. SIDEBAR INTERAKTIF
# =============================================================================
with st.sidebar:
    st.header("💡 Panduan Skala NOVA")
    st.markdown("""
    Sistem klasifikasi pangan internasional yang diakui **WHO/FAO**:
    * 🟢 **NOVA 1 (Real Food):** Bahan alami murni / minimal olahan.
    * 🟡 **NOVA 3 (Processed):** Olahan dapur umum (garam/gula/minyak).
    * 🔴 **NOVA 4 (Ultra-Processed):** Produk pabrikasi dengan bahan aditif sintetis (Junk Food).
    """)
    st.divider()
    st.subheader("🧪 Contoh Teks Demo")
    if st.button("📌 Contoh Mi Instan (NOVA 4)"):
        st.session_state["input_teks"] = "Tepung terigu, minyak kelapa sawit (mengandung antioksidan TBHQ), garam, penguat rasa monosodium glutamat (MSG), natrium benzoat, pengembang amonium bikarbonat, pewarna sintetis tartrazin CI 19140."
    if st.button("📌 Contoh Ikan Kaleng (NOVA 3)"):
        st.session_state["input_teks"] = "Ikan sarden segar, air, tomat, garam, gula, dan minyak kelapa."
    if st.button("📌 Contoh Buah Segar (NOVA 1)"):
        st.session_state["input_teks"] = "Apel fuji segar, pisang raja murni, alpukat mentah, dan air kelapa murni tanpa gula."

# =============================================================================
# 3. HALAMAN UTAMA & INPUT
# =============================================================================
st.title("🥗 Pemilah Real Food vs Junk Food")
st.write("Aplikasi cerdas berbasis analisis teks & OCR untuk memilah makanan berdasarkan skala NOVA 1, 3, dan 4.")

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
# 4. PROSES ANALISIS & HASIL
# =============================================================================
if st.button("🔍 Analisis Makanan Ini", type="primary"):
    if not teks_analisis.strip():
        st.warning("⚠️ Harap masukkan teks komposisi atau upload foto kemasan terlebih dahulu, Cak!")
    else:
        st.divider()
        teks_lower = teks_analisis.lower()

        # 1. Deteksi BTP (NOVA 4)
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
                skor_kesehatan -= 15  # Penalti BTP sintetis

        # 2. Deteksi Bahan NOVA 3 & NOVA 1
        nova3_terdeteksi = list(set([kata for kata in KATA_NOVA3 if kata in teks_lower]))
        nova1_terdeteksi = list(set([kata for kata in KATA_NOVA1_ALAMI if kata in teks_lower]))

        # Penyesuaian Skor NOVA 3
        if nova3_terdeteksi and not btp_terdeteksi:
            skor_kesehatan = 75  # Skor standar makanan olahan dapur

        # Proteksi Batas Skor
        skor_kesehatan = max(0, min(100, skor_kesehatan))

        # 3. Tampilan Skor Kesehatan & Status
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(label="📊 Skor Kesehatan Makanan", value=f"{skor_kesehatan} / 100")
            st.progress(skor_kesehatan / 100)

        with col2:
            # Keputusan Logika NOVA
            if btp_terdeteksi or skor_kesehatan < 60:
                st.error("🔴 **Kategori: NOVA 4 — Ultra-Processed Food (Junk Food)**")
                st.write("**Kesimpulan:** Makanan ini mengandung aditif buatan pabrik dan telah melalui pengolahan industri tinggi.")
                st.warning("💡 **Saran:** Batasi konsumsi! Maksimal 1–2 kali seminggu.")
            
            elif nova3_terdeteksi and not btp_terdeteksi:
                st.warning("🟡 **Kategori: NOVA 3 — Processed Food (Olahan Sederhana)**")
                st.write(f"**Bahan Olahan Dapur Terdeteksi:** `{', '.join(nova3_terdeteksi)}`")
                st.write("**Kesimpulan:** Makanan diolah dengan bahan dasar dapur umum (garam/gula/minyak) tanpa aditif buatan pabrik.")
                st.info("💡 **Saran:** Aman dikonsumsi wajar sebagai lauk harian.")
                
            elif nova1_terdeteksi and not btp_terdeteksi and not nova3_terdeteksi:
                st.success("🟢 **Kategori: NOVA 1 — Real Food (Makanan Alami)**")
                st.write(f"**Bahan Alami Terdeteksi:** `{', '.join(nova1_terdeteksi)}`")
                st.write("**Kesimpulan:** Makanan terbuat dari bahan alami murni tanpa aditif atau olahan berat.")
                st.info("💡 **Saran:** Sangat sehat untuk dikonsumsi harian!")
                
            else:
                st.info("🟡 **Kategori: NOVA 3 / Uncategorized (Olahan Sedang)**")
                st.write("**Kesimpulan:** Tidak terdeteksi aditif berat, kemungkinan makanan olahan biasa.")

        # 4. Tabel Ringkas Efek Samping (Hanya Muncul Jika Ada BTP NOVA 4)
        if btp_terdeteksi:
            st.subheader("⚠️ Rincian Bahan Aditif Terdeteksi & Catatan Kesehatan")
            
            tabel_md = "| Kelompok BTP | Kata Kunci Terdeteksi | Jenis / Fungsi BTP | Potensi Efek Samping (Jika Berlebihan) |\n"
            tabel_md += "| :--- | :--- | :--- | :--- |\n"
            for btp in btp_terdeteksi:
                tabel_md += f"| **{btp['nama']}** | `{btp['kata_kunci']}` | {btp['fungsi']} | {btp['efek']} |\n"
            
            st.markdown(tabel_md)