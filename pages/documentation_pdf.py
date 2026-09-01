import streamlit as st
import base64

# ------------------------------------------------------------
# PDF via HTML (méthode 100% compatible Streamlit Cloud)
# ------------------------------------------------------------

html = """
<h1 style='text-align:center;'>Documentation Technique — Club Canin Chestrolais</h1>

<h2>1. Introduction</h2>
<ul>
<li>Mission du club</li>
<li>Objectifs du système numérique</li>
<li>Architecture générale (Streamlit + Supabase)</li>
<li>Rôles : membre, préposé, comité</li>
</ul>

<h2>2. Flux Extérieur</h2>
<ul>
<li>Préinscription : public_portail.py → table preinscriptions</li>
<li>Validation : page_60_validation.py → Accepté/Refusé</li>
<li>Transformation : page_70_transformation.py → membres, chiens, cotisations, abonnements</li>
<li>Nettoyage automatique : trigger delete_preinscriptions()</li>
</ul>

<h2>3. Flux Membre</h2>
<ul>
<li>Connexion : login.py → Auth Supabase</li>
<li>Inscription : page_80_inscription.py → table presences</li>
<li>Présence : page_90_presence.py</li>
<li>Décrémentation : trigger update_abonnement()</li>
<li>Historique : page_100_historique.py → table historique</li>
</ul>

<h2>4. Schémas officiels</h2>
<ul>
<li>Schéma global corporate</li>
<li>Schéma technique</li>
<li>Schéma vertical membre</li>
<li>Schéma horizontal global</li>
<li>Schéma extérieur</li>
</ul>

<h2>5. Sécurité & RLS Supabase</h2>
<ul>
<li>RLS membres, chiens, presences, preinscriptions, abonnements, historique</li>
</ul>

<h2>6. Architecture technique</h2>
<ul>
<li>Structure des pages Streamlit</li>
<li>Structure des tables Supabase</li>
<li>Triggers et fonctions automatiques</li>
</ul>

<h2>7. Annexes</h2>
<ul>
<li>Glossaire</li>
<li>Codes d’erreurs</li>
<li>Procédures internes</li>
<li>Contacts du comité</li>
</ul>
"""

# Convert HTML → PDF (via browser)
b64 = base64.b64encode(html.encode()).decode()

href = f"""
<a href="data:application/pdf;base64,{b64}" download="documentation_club.pdf">
📄 Télécharger la documentation complète (PDF)
</a>
"""

st.title("📘 Documentation du Club — Export PDF")
st.markdown(href, unsafe_allow_html=True)
