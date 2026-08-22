import streamlit as st

st.set_page_config(page_title="Test séance", page_icon="🟢")
st.title("🟢 Test sélection séance")

# Initialiser
if "seance_detail" not in st.session_state:
    st.session_state["seance_detail"] = None

# Simuler des séances
seances = [
    {"id": 1, "date_seance": "2026-08-30", "nom": "chiots 9h"},
    {"id": 2, "date_seance": "2026-08-30", "nom": "intermédiaires 9h"},
]

# Si une séance est sélectionnée
if st.session_state["seance_detail"]:
    s = st.session_state["seance_detail"]
    st.success(f"Séance sélectionnée : {s['nom']} — {s['date_seance']}")
    st.stop()

# Liste des séances
st.subheader("Séances actives")

for s in seances:
    col1, col2 = st.columns([3,1])
    col1.write(f"{s['date_seance']} — {s['nom']}")
    if col2.button("Valider", key=f"voir_{s['id']}"):
        st.session_state["seance_detail"] = s
        st.rerun()
