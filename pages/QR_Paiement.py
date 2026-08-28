import streamlit as st
import qrcode
from io import BytesIO
from supabase_rest import supabase
import urllib.parse

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement Belgique", page_icon="🔲")

st.title("🔲 QR Paiement – Compatible Belgique (QR Texte)")

# Charger paramètres
params = supabase.table("parametres").select("*").execute().data[0]

beneficiaire_defaut = params.get("nom_beneficiaire") or "Club Canin Chestrolais de Neufchâteau"
iban_defaut = params.get("iban_beneficiaire") or "BE36068954592181"

# Champs
beneficiaire = st.text_input("Nom du bénéficiaire", beneficiaire_defaut)
iban = st.text_input("IBAN du bénéficiaire", iban_defaut)
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

if st.button("Générer le QR Code"):
    try:
        iban_clean = iban.replace(" ", "").strip()
        communication_clean = urllib.parse.quote(communication.strip())
        montant_clean = montant.strip()

        # QR TEXTE compatible Belgique
        # Le montant est inclus mais ignoré par les banques (normal)
        url = (
            f"banktransfer://?"
            f"iban={iban_clean}"
            f"&message={communication_clean}"
            f"&amount={montant_clean}"
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=6,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="QR Paiement (Texte – Compatible Belgique)", use_container_width=False)
        st.success("QR texte généré. Compatible Belfius / CBC / ING / BNP / Hello Bank.")

    except Exception as e:
        st.error("Erreur lors de la génération du QR.")
        st.write(e)
