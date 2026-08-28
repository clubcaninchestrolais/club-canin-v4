import streamlit as st

# --- SÉCURITÉ ---
if "connected" not in st.session_state or not st.session_state["connected"]:
    st.switch_page("pages/login.py")

st.set_page_config(page_title="QR Paiement", page_icon="🔲")

st.title("🔲 QR Paiement")

st.info("""
### Fonction momentanément indisponible

La génération d’un QR bancaire compatible avec les banques belges
(Belfius, CBC/KBC, ING, BNP, Hello Bank…) nécessite l’utilisation du
standard **WERO / Payconiq**, qui n’est pas encore intégré dans l’application.

Le club décidera prochainement s’il souhaite activer une solution
compatible (Payconiq Merchant / QR WERO).

En attendant, cette page reste présente mais la fonction n’est pas opérationnelle.
""")

st.write("Merci pour votre compréhension.")
