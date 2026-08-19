import streamlit as st
import os
import database as db
import document_generator as doc_gen
import styles
from three_bg import render_3d_background

# 1. Configurare Pagina Streamlit
st.set_page_config(
    page_title="PV GENERATOR // INDUSTRIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injectare Fundal 3D Metallic & CSS Dark
render_3d_background()
st.markdown(styles.load_css(), unsafe_allow_html=True)

# 3. Inițializare Bază de Date SQLite
db.init_db()

# 4. Înregistrare Session State
if "numar_randuri_aplicatii" not in st.session_state:
    st.session_state.numar_randuri_aplicatii = 1
if "numar_randuri_persoane" not in st.session_state:
    st.session_state.numar_randuri_persoane = 1

# --- SIDEBAR ---
st.sidebar.markdown("### ȘABLOANE / TEMPLATES")
dict_templates = doc_gen.get_available_templates()

sabloane_selectate = st.sidebar.multiselect(
    "Selectează șabloane:",
    options=list(dict_templates.keys()),
    default=list(dict_templates.keys())[:1] if dict_templates else []
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ÎNCARCĂ ȘABLON (.DOCX)")
uploaded_template = st.sidebar.file_uploader("Upload Word Doc", type=["docx"])
if uploaded_template is not None:
    save_path = os.path.join(doc_gen.TEMPLATES_DIR, uploaded_template.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_template.getbuffer())
    st.sidebar.success(f"Adăugat: {uploaded_template.name}")
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### IDENTITATE VIZUALĂ")
optiune_sigla = st.sidebar.selectbox("Siglă Proiect", ["Integrisoft", "Sud-Vest Oltenia"])
inaltime_sigla = st.sidebar.slider("Înălțime siglă (mm)", min_value=10, max_value=30, value=16)

mapare_sigle = {
    "Integrisoft": os.path.join("assets", "Integrisoft.jpg"),
    "Sud-Vest Oltenia": os.path.join("assets", "Sud_Vest_Oltenia.jpg")
}
cale_sigla_selectata = db.get_resource_path(mapare_sigle[optiune_sigla])

if not os.path.exists(cale_sigla_selectata):
    st.sidebar.warning(f"⚠️ Lipsă imagine: `{cale_sigla_selectata}`")

st.sidebar.markdown("---")
st.sidebar.markdown("### BAZĂ DE DATE FIRME")
firme_existente = db.get_toate_firmele()
if firme_existente:
    firma_de_sters = st.sidebar.selectbox("Șterge o firmă:", ["-- Selectează --"] + list(firme_existente.keys()))
    if firma_de_sters != "-- Selectează --":
        if st.sidebar.button("🗑️ ȘTERGE FIRMA"):
            db.sterge_firma(firma_de_sters)
            st.sidebar.success(f"Șters: '{firma_de_sters}'")
            st.rerun()

# --- FORMULAR PRINCIPAL ---
st.title("GENERATOR PROCESE VERBALE")

# SECTION 01: Date Generale
with st.container():
    st.subheader("01 // DATE GENERALE & CONTRACT")
    c1, c2, c3 = st.columns(3)
    with c1:
        data_incheiere = st.date_input("Data Încheiere PV", key="data_incheiere")
        data_anexa = st.date_input("Data Anexă", key="data_anexa")
        paragraf_numeProiect = st.text_input("Nume Proiect", key="paragraf_numeProiect")
    with c2:
        numar_contract = st.text_input("Număr Contract", key="numar_contract")
        data_contract = st.date_input("Data Contract", key="data_contract")
    with c3:
        anunt_participare = st.text_input("Anunț Participare", key="anunt_participare")
        data_anuntParticipare = st.date_input("Data Anunț Participare", key="data_anuntParticipare")

# SECTION 02: Părți Contractante + AUTOFILL
with st.container():
    st.subheader("02 // PĂRȚI CONTRACTANTE")
    col_cl1, col_cl2 = st.columns(2)
    
    dict_clienti = db.get_toate_firmele(tip="CLIENT")
    dict_prestatori = db.get_toate_firmele(tip="PRESTATOR")

    with col_cl1:
        st.markdown("**CLIENT / BENEFICIAR**")
        opțiuni_client = ["-- Nou / Manual --"] + list(dict_clienti.keys())
        client_selectat = st.selectbox("⚡ Istoric Client:", opțiuni_client, key="select_client")

        val_nume_c, val_adr_c, val_pm_c, val_fnc_c = "", "", "", ""
        if client_selectat != "-- Nou / Manual --":
            val_nume_c = client_selectat
            val_adr_c = dict_clienti[client_selectat]["adresa"]
            val_pm_c = dict_clienti[client_selectat]["pm"]
            val_fnc_c = dict_clienti[client_selectat]["functie"]

        nume_client = st.text_input("Nume Client", value=val_nume_c, key="nume_client")
        adresa_client = st.text_input("Adresă Client", value=val_adr_c, key="adresa_client")
        pm_client = st.text_input("PM Client", value=val_pm_c, key="pm_client")
        functie_client = st.text_input("Funcție Client", value=val_fnc_c, key="functie_client")

    with col_cl2:
        st.markdown("**PRESTATOR / FIRMĂ**")
        opțiuni_prestator = ["-- Nou / Manual --"] + list(dict_prestatori.keys())
        prestator_selectat = st.selectbox("⚡ Istoric Prestator:", opțiuni_prestator, key="select_prestator")

        val_nume_p, val_adr_p, val_pm_p = "", "", ""
        if prestator_selectat != "-- Nou / Manual --":
            val_nume_p = prestator_selectat
            val_adr_p = dict_prestatori[prestator_selectat]["adresa"]
            val_pm_p = dict_prestatori[prestator_selectat]["pm"]

        numeFirma_participanta = st.text_input("Nume Firmă", value=val_nume_p, key="numeFirma_participanta")
        adresa_firmaParticipanta = st.text_input("Adresă Firmă", value=val_adr_p, key="adresa_firmaParticipanta")
        numePM_firmaParticipanta = st.text_input("PM Firmă", value=val_pm_p, key="numePM_firmaParticipanta")

    if st.button("💾 SALVEAZĂ FIRMELE ÎN DB"):
        if nume_client:
            db.salveaza_sau_actualizeaza_firma(nume_client, adresa_client, pm_client, functie_client, tip="CLIENT")
        if numeFirma_participanta:
            db.salveaza_sau_actualizeaza_firma(numeFirma_participanta, adresa_firmaParticipanta, numePM_firmaParticipanta, "", tip="PRESTATOR")
        st.success("Salvat!")
        st.rerun()

# SECTION 03: Detalii Instruire
with st.container():
    st.subheader("03 // DETALII PROGRAM INSTRUIRE")
    c_ins1, c_ins2 = st.columns(2)
    with c_ins1:
        locul_de_instruire = st.text_input("Locul de instruire", key="locul_de_instruire")
        nr_zile_instruire = st.text_input("Nr. zile instruire", key="nr_zile_instruire")
        responsabil_instruire = st.text_input("Responsabilități instruire", key="responsabil_instruire")
        program_de_instruire = st.text_input("Program de instruire", key="program_de_instruire")
    with c_ins2:
        nr_zile_proiectare = st.text_input("Nr. zile necesar proiector", key="nr_zile_proiectare")
        responsabil_proiector = st.text_input("Responsabilități proiector", key="responsabil_proiector")

# SECTION 04: Tabel Aplicații
with st.container():
    st.subheader("04 // TABEL APLICAȚII / MODULE")
    lista_aplicatii = []
    for i in range(st.session_state.numar_randuri_aplicatii):
        ac1, ac2 = st.columns(2)
        with ac1:
            cs = st.text_input(f"Aplicație CS #{i+1}", key=f"cs_{i}")
        with ac2:
            iss = st.text_input(f"Aplicație ISS #{i+1}", key=f"iss_{i}")
        lista_aplicatii.append({"caiet_sarcini": cs, "iss": iss})

    btn1, btn2, _ = st.columns([1.5, 1.5, 4])
    with btn1:
        if st.button("➕ ADAUGĂ APLICAȚIE"):
            st.session_state.numar_randuri_aplicatii += 1
            st.rerun()
    with btn2:
        if st.button("➖ ȘTERGE APLICAȚIE"):
            if st.session_state.numar_randuri_aplicatii > 1:
                st.session_state.numar_randuri_aplicatii -= 1
                st.rerun()

# SECTION 05: Tabel Persoane
with st.container():
    st.subheader("05 // TABEL PERSOANE INSTRUITE")
    lista_persoane = []
    for i in range(st.session_state.numar_randuri_persoane):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            nume_p = st.text_input(f"Nume #{i+1}", key=f"nume_p_{i}")
        with col_p2:
            dept_p = st.text_input(f"Departament #{i+1}", key=f"dept_p_{i}")
        lista_persoane.append({"nume": nume_p, "departament": dept_p})

    p_btn1, p_btn2, _ = st.columns([1.5, 1.5, 4])
    with p_btn1:
        if st.button("➕ ADAUGĂ PERSOANĂ"):
            st.session_state.numar_randuri_persoane += 1
            st.rerun()
    with p_btn2:
        if st.button("➖ ȘTERGE PERSOANĂ"):
            if st.session_state.numar_randuri_persoane > 1:
                st.session_state.numar_randuri_persoane -= 1
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# GENERARE DOCUMENT
if st.button("🚀 GENEREAZĂ DOCUMENTELE", type="primary"):
    if not sabloane_selectate:
        st.error("Selectează cel puțin un șablon!")
    else:
        if nume_client:
            db.salveaza_sau_actualizeaza_firma(nume_client, adresa_client, pm_client, functie_client, tip="CLIENT")
        if numeFirma_participanta:
            db.salveaza_sau_actualizeaza_firma(numeFirma_participanta, adresa_firmaParticipanta, numePM_firmaParticipanta, "", tip="PRESTATOR")

        context_baza = {
            'data_incheiere': data_incheiere.strftime("%d.%m.%Y") if data_incheiere else "",
            'data_anexa': data_anexa.strftime("%d.%m.%Y") if data_anexa else "",
            'nume_client': nume_client,
            'adresa_client': adresa_client,
            'pm_client': pm_client,
            'functie_client': functie_client,
            'numeFirma_participanta': numeFirma_participanta,
            'nume_firmaParticipanta': numeFirma_participanta,
            'adresa_firmaParticipanta': adresa_firmaParticipanta,
            'numePM_firmaParticipanta': numePM_firmaParticipanta,
            'paragraf_numeProiect': paragraf_numeProiect,
            'Paragraf_numeProiect': paragraf_numeProiect,
            'anunt_participare': anunt_participare,
            'data_anuntParticipare': data_anuntParticipare.strftime("%d.%m.%Y") if data_anuntParticipare else "",
            'numar_contract': numar_contract,
            'data_contract': data_contract.strftime("%d.%m.%Y") if data_contract else "",
            'locul_de_instruire': locul_de_instruire,
            'nr_zile_instruire': nr_zile_instruire,
            'responsabil_instruire': responsabil_instruire,
            'nr_zile_proiectare': nr_zile_proiectare,
            'responsabil_proiector': responsabil_proiector,
            'program_de_instruire': program_de_instruire,
            'aplicatii': [a for a in lista_aplicatii if a["caiet_sarcini"] or a["iss"]],
            'persoane': [p for p in lista_persoane if p["nume"] or p["departament"]]
        }

        fisiere = doc_gen.genereaza_documente(
            sabloane_selectate, 
            dict_templates, 
            context_baza, 
            cale_sigla_selectata, 
            inaltime_sigla=inaltime_sigla
        )

        if len(fisiere) == 1:
            filename, buf = fisiere[0]
            st.download_button(f"⬇️ DESCARCĂ {filename}", buf, file_name=filename)
        elif len(fisiere) > 1:
            zip_buf = doc_gen.creeaza_arhiva_zip(fisiere)
            st.download_button("📦 DESCARCĂ ARHIVA ZIP", zip_buf, file_name="Procese_Verbale.zip")