import streamlit as st
from database import (
    init_db, 
    get_toate_firmele, 
    salveaza_sau_actualizeaza_firma, 
    sterge_firma
)

# 1. Configurare pagină
st.set_page_config(
    page_title="Generator PV & Documente",
    page_icon="📄",
    layout="wide"
)

# 2. Inițializarea bazei de date la pornire
@st.cache_resource
def startup_db():
    init_db()

startup_db()

# 3. Interfața principală a aplicației
st.title("📄 Generator de Procese Verbale și Documente")
st.write("Aplicație colaborativă pentru gestionarea firmelor și generarea automată de documente.")

# Meniu lateral pentru navigare / secțiuni
meniu = st.sidebar.selectbox("Navigare", ["Generare Document", "Gestionare Firme"])

if meniu == "Gestionare Firme":
    st.header("🏢 Gestionare Firme (Baza de date Neon)")
    
    # Formular adăugare / editare firmă
    with st.form("form_firma"):
        st.subheader("Adaugă sau Actualizează Firmă")
        nume_input = st.text_input("Nume Firmă")
        adresa_input = st.text_input("Adresă Sediu")
        pm_input = st.text_input("Project Manager (PM)")
        functie_input = st.text_input("Funcție / Detalii")
        tip_input = st.selectbox("Tip", ["CLIENT", "PARTENER", "FURNIZOR"])
        
        submitted = st.form_submit_button("Salvează în Cloud")
        if submitted:
            if nume_input.strip():
                salveaza_sau_actualizeaza_firma(
                    nume=nume_input,
                    adresa=adresa_input,
                    pm=pm_input,
                    functie=functie_input,
                    tip=tip_input
                )
                st.success(f"Firma **{nume_input}** a fost salvată cu succes în Neon!")
                st.rerun()
            else:
                st.error("Numele firmei este obligatoriu!")

    st.divider()
    
    # Afișarea firmelor existente din baza de date
    st.subheader("📋 Firme Salvate în Sistem")
    firmele_existente = get_toate_firmele()
    
    if firmele_existente:
        for nume, info in firmele_existente.items():
            col1, col2, col3 = st.columns([3, 4, 1])
            with col1:
                st.write(f"**{nume}** ({info['tip']})")
                st.caption(f"Adresă: {info['adresa']}")
            with col2:
                st.write(f"PM: {info['pm']} | Funcție: {info['functie']}")
            with col3:
                if st.button("Șterge", key=f"del_{nume}"):
                    sterge_firma(nume)
                    st.warning(f"S-a șters firma {nume}")
                    st.rerun()
    else:
        st.info("Nu există firme salvate momentan în baza de date.")

elif meniu == "Generare Document":
    st.header("⚙️ Generare Proces Verbal")
    
    firmele_existente = get_toate_firmele()
    nume_firme = list(firmele_existente.keys())
    
    if not nume_firme:
        st.warning("Te rog să adaugi cel puțin o firmă în secțiunea 'Gestionare Firme' înainte de a genera un document.")
    else:
        firma_selectata = st.selectbox("Selectează Firma", nume_firme)
        
        if firma_selectata:
            detalii_firma = firmele_existente[firma_selectata]
            st.write("Detalii firmă selectată:")
            st.json(detalii_firma)
            
            # Aici poți adăuga logica ta cu docxtpl pentru generarea propriu-zisă
            if st.button("Generează Document Word"):
                st.info("Logica de generare docxtpl rulează aici...")
