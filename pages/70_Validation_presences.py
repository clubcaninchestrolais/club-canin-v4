# Bouton de validation
if st.button(f"Valider présence — {membre_nom}"):

    # ---------------------------------------------------------
    # 1) Vérification cotisation
    # ---------------------------------------------------------
    cot = (
        supabase.table("cotisations")
        .select("*")
        .eq("membre_id", membre["id"])
        .execute()
        .data
    )

    cotisation_ok = True

    if not cot:
        st.error("❌ Ce membre n'a pas de cotisation.")
        cotisation_ok = False
    else:
        cot = cot[0]

        if cot["statut"] != "active":
            st.error("❌ Cotisation non active.")
            cotisation_ok = False

        if cot["date_expiration"] and cot["date_expiration"] < date.today().isoformat():
            st.error("❌ Cotisation expirée.")
            cotisation_ok = False

    # ---------------------------------------------------------
    # 2) Vérification abonnement
    # ---------------------------------------------------------
    abo = (
        supabase.table("abonnements")
        .select("*")
        .eq("membre_id", membre["id"])
        .execute()
        .data
    )

    abonnement_ok = True

    if not abo:
        st.error("❌ Ce membre n'a pas d'abonnement.")
        abonnement_ok = False
    else:
        abo = abo[0]

        if abo["statut"] != "active":
            st.error("❌ Abonnement non actif.")
            abonnement_ok = False

        if abo["date_expiration"] and abo["date_expiration"] < date.today().isoformat():
            st.error("❌ Abonnement expiré.")
            abonnement_ok = False

        # Séances restantes (si la colonne existe)
        if "seances_restantes" in abo:
            if abo["seances_restantes"] == 0:
                st.error("❌ Abonnement épuisé : aucune séance restante.")
                abonnement_ok = False

    # ---------------------------------------------------------
    # 3) Si problème → message visible mais validation possible
    # ---------------------------------------------------------
    if not cotisation_ok or not abonnement_ok:
        st.warning("⚠️ Le membre n'est pas en ordre. Le préposé doit vérifier avec lui.")
        # On continue quand même la validation de présence
        # (si tu veux bloquer, je peux activer un blocage strict)

    # ---------------------------------------------------------
    # 4) Enregistrer présence
    # ---------------------------------------------------------
    supabase.table("cours_presences").insert({
        "membre_id": membre["id"],
        "chien_id": ins["chien_id"],
        "seance_id": seance_id,
        "present": True,
        "date_presence": date.today().isoformat()
    }).execute()

    # ---------------------------------------------------------
    # 5) Décrémenter l'abonnement (sauf bénévoles)
    # ---------------------------------------------------------
    if abo and "seances_restantes" in abo:

        # Ne pas décrémenter bénévoles
        if abo["seances_restantes"] != -1:

            # Décrémentation uniquement si abonnement OK
            if abonnement_ok:
                reste = abo["seances_restantes"] - 1

                supabase.table("abonnements").update({
                    "seances_restantes": reste,
                    "actif": reste > 0
                }).eq("id", abo["id"]).execute()

    st.success("Présence validée")
    st.rerun()
