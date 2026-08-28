import streamlit as st
import qrcode
from io import BytesIO
from supabase_rest import supabase
import unicodedata
import re

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement SEPA (Belgique)", page_icon="🔲")

st.title("🔲 QR Paiement SEPA – Version Belgique")

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

        # Si pas de décimales → ajouter .00
        if "." not in montant_clean:
            montant_clean = montant_clean + ".00"
        else:
            # Forcer deux décimales
            parts = montant_clean.split(".")
            if len(parts[1]) == 1:
                montant_clean = montant_clean + "0"
            elif len(parts[1]) > 2:
                montant_clean = parts[0] + "." + parts[1][:2]

        communication_clean = clean_text(communication)

        # Format SEPA BELGIQUE (ligne 2 = 002)
        epc_text = (
            "BCD\n"
            "002\n"          # <-- VERSION BELGE
            "1\n"
            "SCT\n"
            f"{beneficiaire_clean}\n"
            f"{iban_clean}\n"
            f"EUR{montant_clean}\n"
            f"{communication_clean}"
        )

        # Encodage ISO-8859-1 obligatoire pour la Belgique
        epc_bytes = epc_text.encode("iso-8859-1")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=4,
        )
        qr.add_data(epc_bytes)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="QR Code SEPA (Belgique)", use_container_width=False)
        st.success("QR SEPA BELGE généré et compatible Belfius / CBC / ING / BNP.")

    except Exception as e:
        st.error("Erreur lors de la génération du QR Code.")
        st.write(e)
