import streamlit as st
import base64

st.title("Génération QR Paiement SEPA")

st.write("Encodez les informations du paiement pour générer un QR SEPA scannable par le membre.")

beneficiaire = st.text_input("Nom du bénéficiaire", "")
iban = st.text_input("IBAN du bénéficiaire", "")
montant = st.text_input("Montant (€)", "")
communication = st.text_input("Communication / Libellé", "")

def generate_svg_qr(data):
    import qrcode
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<img src="data:image/png;base64,{b64}" width="300"/>'

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

        try:
            svg = generate_svg_qr(epc_text)
            st.markdown(svg, unsafe_allow_html=True)
            st.success("QR Code généré ! Le membre peut le scanner directement.")
        except Exception as e:
            st.error("Impossible de générer le QR Code dans cet environnement.")
            st.write("Erreur :", e)
