import streamlit as st
import qrcode
from io import BytesIO
from supabase_rest import supabase

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement SEPA", page_icon="🔲")

st.title("🔲 Génération QR Paiement SEPA")

# ---------------------------------------------------------
# 🔄 Charger les paramètres depuis Supabase
# ---------------------------------------------------------
params = supabase.table("parametres").select("*").execute().data[0]

beneficiaire_defaut = params.get("nom_beneficiaire", "Club Canin Chestrolais de Neufchâteau")
iban_defaut = params.get("iban_beneficiaire", "BE36068954592181")

# ---------------------------------------------------------
# 📝 Champs de saisie
# ---------------------------------------------------------
beneficiaire = st.text_input("Nom du bénéficiaire", beneficiaire_defaut)
iban = st.text_input("IBAN du bénéficiaire", iban_defaut)
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

# ---------------------------------------------------------
# 🔲 Génération du QR Code
# ---------------------------------------------------------
if st.button("Générer le QR Code"):
    if not beneficiaire or not iban or not montant:
        st.error("Veuillez remplir au minimum : bénéficiaire, IBAN et montant.")
    else:
        epc_text = f"""BCD
001
1
SCT
{beneficiaire}
{iban.replace(" ", "")}
EUR{montant}
{communication}"""

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(epc_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="QR Code SEPA", use_column_width=True)
        st.success("QR Code généré ! Le membre peut le scanner directement.")
