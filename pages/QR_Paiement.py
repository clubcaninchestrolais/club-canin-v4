import streamlit as st
import qrcode
from io import BytesIO

st.title("Génération QR Paiement SEPA")

st.write("Encodez les informations du paiement pour générer un QR SEPA scannable par le membre.")

# Champs libres
beneficiaire = st.text_input("Nom du bénéficiaire", "")
iban = st.text_input("IBAN du bénéficiaire", "")
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

if st.button("Générer le QR Code"):
    if not beneficiaire or not iban or not montant:
        st.error("Veuillez remplir au minimum : bénéficiaire, IBAN et montant.")
    else:
        # Construction du texte SEPA EPC
        epc_text = f"""BCD
001
1
SCT
{beneficiaire}
{iban.replace(" ", "")}
EUR{montant}
{communication}"""

        # Génération du QR
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(epc_text)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        # Affichage
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="QR Code SEPA", use_column_width=True)

        st.success("QR Code généré ! Le membre peut le scanner directement.")
