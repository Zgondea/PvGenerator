import os
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

@st.cache_resource
def get_db_connection():
    """Conexiune directă la PostgreSQL (Neon.tech) folosind DATABASE_URL din secrets."""
    db_url = st.secrets.get("DATABASE_URL") or os.getenv("DATABASE_URL")
    
    if not db_url:
        raise ValueError("Lipsește DATABASE_URL din configurare!")
        
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

def get_connection_safe():
    """Verifică starea conexiunii și o reface automat dacă a fost închisă (SSL closed)."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        return conn
    except Exception:
        st.cache_resource.clear()
        return get_db_connection()

def init_db():
    """Creează tabelul 'firme' în Neon dacă acesta nu există deja."""
    try:
        conn = get_connection_safe()
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS firme (
                    nume TEXT PRIMARY KEY,
                    adresa TEXT,
                    pm TEXT,
                    functie TEXT,
                    tip TEXT
                );
            """)
            conn.commit()
    except Exception as e:
        st.error(f"Eroare la inițializarea bazei de date în Neon: {e}")

def get_resource_path(relative_path):
    """Calculează cale absolută pentru resurse din proiect."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_toate_firmele(tip=None):
    """Aduce firmele din baza de date Neon."""
    try:
        conn = get_connection_safe()
        with conn.cursor() as cur:
            if tip:
                cur.execute("SELECT * FROM firme WHERE tip = %s;", (tip,))
            else:
                cur.execute("SELECT * FROM firme;")
            rows = cur.fetchall()

        firme = {}
        for r in rows:
            firme[r["nume"]] = {
                "adresa": r["adresa"] or "",
                "pm": r["pm"] or "",
                "functie": r["functie"] or "",
                "tip": r["tip"]
            }
        return firme
    except Exception as e:
        st.error(f"Eroare la citirea din Neon: {e}")
        return {}

def salveaza_sau_actualizeaza_firma(nume, adresa, pm, functie, tip="CLIENT"):
    """Inserează sau actualizează o firmă în Neon (Upsert)."""
    if not nume or not nume.strip():
        return

    try:
        conn = get_connection_safe()
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO firme (nume, adresa, pm, functie, tip)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (nume) 
                DO UPDATE SET 
                    adresa = EXCLUDED.adresa,
                    pm = EXCLUDED.pm,
                    functie = EXCLUDED.functie,
                    tip = EXCLUDED.tip;
            """, (nume.strip(), adresa.strip() if adresa else "", pm.strip() if pm else "", functie.strip() if functie else "", tip))
            conn.commit()
    except Exception as e:
        st.error(f"Eroare la salvarea în Neon: {e}")

def sterge_firma(nume):
    """Șterge o firmă din Neon după nume."""
    try:
        conn = get_connection_safe()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM firme WHERE nume = %s;", (nume,))
            conn.commit()
    except Exception as e:
        st.error(f"Eroare la ștergerea din Neon: {e}")