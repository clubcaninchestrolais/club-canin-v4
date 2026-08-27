import streamlit as st
import segno
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

        qr = segno.make(epc_text)

        buf = BytesIO()
        qr.save(buf, kind="png", scale=8)
        buf.seek(0)

        st.image(buf, caption="QR Code SEPA", use_column_width=True)
        st.success("QR Code généré ! Le membre peut le scanner directement.")
