import streamlit as st
from PIL import Image
import qrcode
from io import BytesIO

st.title("Génération QR Paiement SEPA")

st.write("Encodez les informations du paiement pour générer un QR SEPA scannable par le membre.")

beneficiaire = st.text_input("Nom du bénéficiaire", "")
iban = st.text_input("IBAN du bénéficiaire", "")
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

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

        # Génération du QR via PIL (aucune dépendance externe)
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

        st.image(buf, caption="QR Code SEPA", width=300)
        st.success("QR Code généré ! Le membre peut le scanner directement.")
