import streamlit as st
import qrcode
from io import BytesIO
from supabase_rest import supabase
import unicodedata
import re

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement SEPA", page_icon="🔲")

st.title("🔲 Génération QR Paiement SEPA")

# Charger paramètres
params = supabase.table("parametres").select("*").execute().data[0]

beneficiaire_defaut = params.get("nom_beneficiaire") or "Club Canin Chestrolais de Neufchâteau"
iban_defaut = params.get("iban_beneficiaire") or "BE36068954592181"

# Fonction pour enlever accents
def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Fonction pour nettoyer communication (EPC strict)
def clean_text(text):
    text = remove_accents(text)
    text = re.sub(r"[^A-Za-z0-9 ]", "", text)  # EPC : lettres, chiffres, espaces
    return text.strip()

# Champs
beneficiaire = st.text_input("Nom du bénéficiaire", beneficiaire_defaut)
iban = st.text_input("IBAN du bénéficiaire", iban_defaut)
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

# Génération QR
if st.button("Générer le QR Code"):
    try:
        # Nettoyage EPC obligatoire
        beneficiaire_clean = clean_text(beneficiaire)
        iban_clean = iban.replace(" ", "").strip()

        # Format montant EPC : toujours 2 décimales
        montant_clean = montant.replace(",", ".").strip()
        if "." not in montant_clean:
            montant_clean += ".00"
        else:
            # Forcer deux décimales
            parts = montant_clean.split(".")
            if len(parts[1]) == 1:
                montant_clean += "0"

        communication_clean = clean_text(communication)

        # Format EPC strict
        epc_text = f"""BCD
001
1
SCT
{beneficiaire_clean}
{iban_clean}
EUR{montant_clean}
{communication_clean}"""

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=4,
        )
        qr.add_data(epc_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="QR Code SEPA", use_container_width=False)
        st.success("QR Code SEPA généré et conforme EPC.")

    except Exception as e:
        st.error("Erreur lors de la génération du QR Code.")
        st.write(e)
