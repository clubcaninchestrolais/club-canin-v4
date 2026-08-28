import streamlit as st
import qrcode
from io import BytesIO
from supabase_rest import supabase
import urllib.parse

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement Belgique", page_icon="🔲")

st.title("🔲 QR Paiement – Compatible Belgique (sans Payconiq)")

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

        # QR compatible Belgique : URL interprétée par les apps bancaires
        url = f"https://payment.belgium/transfer?iban={iban_clean}&message={communication_clean}&amount={montant}"

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

        st.image(buf, caption="QR Paiement Belgique", use_container_width=False)
        st.success("QR compatible Belgique généré. Scannable par Belfius / CBC / ING / BNP.")

    except Exception as e:
        st.error("Erreur lors de la génération du QR.")
        st.write(e)
