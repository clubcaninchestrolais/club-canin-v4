import customtkinter as ctk
from tkinter import messagebox

# Import du module Membres V2
from members_interface import MembersInterface

# Import des fonctions existantes
from supabase_rest import (
    list_auth_users,
    get_profiles,
    delete_auth_user,
    delete_profile
)

from modules.admin_user_manager import create_user_with_profile


class AdminInterface(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_user_id = None

        ctk.CTkLabel(self, text="Interface Administrateur", font=("Arial", 22, "bold")).pack(pady=10)

        # ------------------------------
        # Boutons du panneau admin
        # ------------------------------
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Utilisateurs", command=self.show_users).grid(row=0, column=0, padx=10)
        ctk.CTkButton(btn_frame, text="Membres", command=self.open_members).grid(row=0, column=1, padx=10)
        ctk.CTkButton(btn_frame, text="Rafraîchir", command=self.load_users).grid(row=0, column=2, padx=10)

        # ------------------------------
        # Zone du tableau
        # ------------------------------
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True)

        self.show_users()

    # ---------------------------------------------------------
    # AFFICHAGE DES UTILISATEURS
    # ---------------------------------------------------------
    def show_users(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        self.load_users()

    def load_users(self):
        for w in self.table_frame.winfo_children():
            w.destroy()

        auth_users = list_auth_users()
        profiles = get_profiles()
        roles = {p["id"]: p.get("role", "non défini") for p in profiles}

        table = ctk.CTkScrollableFrame(self.table_frame)
        table.pack(fill="both", expand=True)

        for user in auth_users:
            uid = user["id"]
            email = user.get("email", "")
            role = roles.get(uid, "non défini")

            row = ctk.CTkFrame(table)
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=email, width=250).pack(side="left")
            ctk.CTkLabel(row, text=role, width=150).pack(side="left")

            row.bind("<Button-1>", lambda e, u=uid: self.select_user(u))

        self.selected_user_id = None

    def select_user(self, uid):
        self.selected_user_id = uid

    # ---------------------------------------------------------
    # AJOUT D'UN UTILISATEUR
    # ---------------------------------------------------------
    def open_add_user_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Ajouter un utilisateur")
        win.geometry("350x300")

        email_entry = ctk.CTkEntry(win, placeholder_text="Email")
        email_entry.pack(pady=10)

        password_entry = ctk.CTkEntry(win, placeholder_text="Mot de passe", show="*")
        password_entry.pack(pady=10)

        role_entry = ctk.CTkEntry(win, placeholder_text="Rôle (admin / user)")
        role_entry.pack(pady=10)

        def submit():
            email = email_entry.get()
            password = password_entry.get()
            role = role_entry.get()

            try:
                user_id = create_user_with_profile(email, password, role)
                messagebox.showinfo("Succès", f"Utilisateur créé : {user_id}")
                win.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

        ctk.CTkButton(win, text="Créer", command=submit).pack(pady=20)

    # ---------------------------------------------------------
    # SUPPRESSION D'UN UTILISATEUR
    # ---------------------------------------------------------
    def delete_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Attention", "Sélectionnez un utilisateur.")
            return

        if not messagebox.askyesno("Confirmation", "Supprimer cet utilisateur ?"):
            return

        try:
            delete_auth_user(self.selected_user_id)
            delete_profile(self.selected_user_id)
            messagebox.showinfo("Succès", "Utilisateur supprimé.")
            self.load_users()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    # ---------------------------------------------------------
    # MODULE MEMBRES V2
    # ---------------------------------------------------------
    def open_members(self):
        for widget in self.winfo_children():
            widget.destroy()
        MembersInterface(self)