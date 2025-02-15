# -*- coding: utf-8 -*-
"""
Created on Fri JAN 2 15:52:42 2025

@author: Nicolas ANNON 
"""

import yfinance as yf
import datetime
import pandas as pd
from binance.client import Client
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




# ======================  CLASSES DU PORTFEUILLE  ======================

class Actif:
    def __init__(self, nom, quantite, date_transaction, prix_achat=None):
        self.nom = nom  
        self.quantite = quantite
        self.date_transaction = date_transaction
        self.prix_achat = prix_achat      
        
        self.prix_marche = None

    def mise_a_jour_prix(self):
        pass

    def valorisation(self):
        """
        Retourne la valeur de l'actif (quantité * prix de marché).
        """
        if self.prix_marche is None:
            self.mise_a_jour_prix()
        return self.quantite * self.prix_marche

class Action(Actif):
    def __init__(self, symbole, quantite, date_transaction, prix_achat=None):
        super().__init__(symbole, quantite, date_transaction, prix_achat)
        if self.prix_achat is None:
            ticker = yf.Ticker(self.nom)
            start_date = self.date_transaction
            end_date = self.date_transaction + datetime.timedelta(days=1)
            data = ticker.history(start=start_date, end=end_date)
            if not data.empty:
                self.prix_achat = data['Close'].iloc[0]
            else:
                print(f"Aucune donnée pour fixer le prix d'achat de {self.nom} à la date {self.date_transaction}")
                self.prix_achat = 0.0

    def mise_a_jour_prix(self):
        """
        Récupère le dernier prix de clôture actuel via yfinance.
        """
        ticker = yf.Ticker(self.nom)
        data = ticker.history(period="1d")
        if not data.empty:
            self.prix_marche = data['Close'].iloc[-1]
        else:
            print(f"Aucune donnée trouvée pour {self.nom}")


class Obligation(Actif):
    def __init__(self, isin, quantite, date_transaction, taux_coupon, prix_achat=None):
        super().__init__(isin, quantite, date_transaction, prix_achat)
        self.taux_coupon = taux_coupon
        if self.prix_achat is None:
            self.prix_achat = 100

    def mise_a_jour_prix(self):
        """
        Pour simplifier, on simule ici le prix de l'obligation.
        """
        self.prix_marche = 100  

class Crypto(Actif):
    def __init__(self, symbole, quantite, date_transaction, prix_achat=None):
        super().__init__(symbole, quantite, date_transaction, prix_achat)
        if self.prix_achat is None:
            client = Client(
                api_key="XXXXXX", #à remplacer par votre clef API BINANCE 
                api_secret="XXXXXX" #à remplacer par votre clef API BINANCE 
            )
            start_str = self.date_transaction.strftime("%d %b, %Y")
            end_str = (self.date_transaction + datetime.timedelta(days=1)).strftime("%d %b, %Y")
            try:
                klines = client.get_historical_klines(
                    self.nom, Client.KLINE_INTERVAL_1DAY, start_str, end_str)
                if klines:
            
                    self.prix_achat = float(klines[0][4])
                else:
                    print(f"Pas de données historiques pour fixer le prix d'achat de {self.nom} à la date {self.date_transaction}")
                    self.prix_achat = 0.0
            except Exception as e:
                print(f"Erreur lors de la récupération du prix d'achat pour {self.nom} : {e}")
                self.prix_achat = 0.0

    def mise_a_jour_prix(self):
        """
        Récupère le prix actuel via Binance en utilisant l'API publique.
        """
        client = Client(
            api_key="XXXXXXX", #à remplacer par votre clef API BINANCE
            api_secret="XXXXX" #à remplacer par votre clef API BINANCE
        )
        try:
            prix_info = client.get_symbol_ticker(symbol=self.nom)
            self.prix_marche = float(prix_info['price'])
        except Exception as e:
            print(f"Erreur lors de la récupération du prix pour {self.nom} : {e}")


class Portefeuille:
    def __init__(self):
        self.actifs = []

    def ajouter_actif(self, actif):
        self.actifs.append(actif)

    def mise_a_jour_prix_actifs(self):
        """
        Met à jour le prix de marché de chacun des actifs du portefeuille.
        """
        for actif in self.actifs:
            actif.mise_a_jour_prix()

    def valorisation_totale(self):
        """
        Calcule la valorisation totale du portefeuille.
        """
        total = 0
        for actif in self.actifs:
            total += actif.valorisation()
        return total

    def calcul_pnl(self):
        """
        Calcule le PnL du portefeuille entre le prix d'achat et le prix de marché actuel.

        PnL = (prix_marche - prix_achat) * quantite

        Retourne un dictionnaire par actif et le PnL total.
        """
        total_pnl = 0.0
        pnl_details = {}
        for actif in self.actifs:
            if actif.prix_marche is None:
                actif.mise_a_jour_prix()
            pnl = (actif.prix_marche - actif.prix_achat) * actif.quantite
            pnl_details[actif.nom] = pnl
            total_pnl += pnl
        return pnl_details, total_pnl

    def supprimer_actif(self, nom, quantite=None):
        """
        Supprime (ou vend) un actif du portefeuille.

        Si 'quantite' est précisée, la quantité de l'actif est réduite de cette valeur.
        Si la quantité restante est <= 0 ou si aucune quantité n'est précisée, l'actif est supprimé.

        Parameters:
            nom (str): Le nom (symbole ou ISIN) de l'actif.
            quantite (float, optionnel): La quantité à vendre.
        """
        for actif in self.actifs:
            if actif.nom == nom:
                if quantite is None or quantite >= actif.quantite:
                    self.actifs.remove(actif)
                    print(f"Actif {nom} entièrement vendu et supprimé du portefeuille.")
                else:
                    actif.quantite -= quantite
                    montant_vente = quantite * actif.prix_marche
                    print(f"Vente de {quantite} de {nom}. Nouvelle quantité: {actif.quantite}")
                    print(f"Montant de la vente: {montant_vente}")
                return
        print(f"Aucun actif trouvé avec le nom {nom}.")



def graphique_repartition_portefeuille(portefeuille):
    """
    Affiche un camembert de la répartition du portefeuille par classe d'actif,
    basé sur la valorisation de chaque actif.
    """
    portefeuille.mise_a_jour_prix_actifs()
    distribution = {}
    for actif in portefeuille.actifs:
        classe = actif.__class__.__name__
        valeur = actif.valorisation()
        distribution[classe] = distribution.get(classe, 0) + valeur
    labels = list(distribution.keys())
    sizes = list(distribution.values())
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Répartition du portefeuille par classe d'actif")
    plt.axis('equal')
    plt.show()


# ======================  INTERFACE GRAPHIQUE (Tkinter)  ======================

class Application(tk.Tk):
    def __init__(self, portefeuille):
        super().__init__()
        self.title("Gestion de Portefeuille")
        self.portefeuille = portefeuille

        self.frame_form = tk.Frame(self)
        self.frame_form.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.frame_actions = tk.Frame(self)
        self.frame_actions.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.btn_import = tk.Button(self.frame_actions, text="Importer Portefeuille", command=self.importer_portefeuille)
        self.btn_import.grid(row=0, column=4, padx=5)

        self.frame_output = tk.Frame(self)
        self.frame_output.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_form, text="Type d'actif:").grid(row=0, column=0, sticky=tk.W)
        self.asset_type = tk.StringVar(value="Action")
        self.option_asset = ttk.Combobox(self.frame_form, textvariable=self.asset_type,
                                         values=["Action", "Obligation", "Crypto"])
        self.option_asset.grid(row=0, column=1)

        tk.Label(self.frame_form, text="Nom (symbole ou ISIN):").grid(row=1, column=0, sticky=tk.W)
        self.entry_nom = tk.Entry(self.frame_form)
        self.entry_nom.grid(row=1, column=1)

        tk.Label(self.frame_form, text="Quantité:").grid(row=2, column=0, sticky=tk.W)
        self.entry_quantite = tk.Entry(self.frame_form)
        self.entry_quantite.grid(row=2, column=1)

        tk.Label(self.frame_form, text="Date Transaction (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W)
        self.entry_date = tk.Entry(self.frame_form)
        self.entry_date.grid(row=3, column=1)

        tk.Label(self.frame_form, text="Prix d'achat (optionnel):").grid(row=4, column=0, sticky=tk.W)
        self.entry_prix_achat = tk.Entry(self.frame_form)
        self.entry_prix_achat.grid(row=4, column=1)

        tk.Label(self.frame_form, text="Taux Coupon (Obligation):").grid(row=5, column=0, sticky=tk.W)
        self.entry_taux_coupon = tk.Entry(self.frame_form)
        self.entry_taux_coupon.grid(row=5, column=1)

        self.btn_ajouter = tk.Button(self.frame_form, text="Ajouter Actif", command=self.ajouter_actif)
        self.btn_ajouter.grid(row=6, column=0, columnspan=2, pady=5)

        
        self.btn_supprimer = tk.Button(self.frame_actions, text="Supprimer Actif", command=self.supprimer_actif)
        self.btn_supprimer.grid(row=0, column=0, padx=5)

        self.btn_valorisation = tk.Button(self.frame_actions, text="Afficher Valorisation Totale",
                                          command=self.afficher_valorisation)
        self.btn_valorisation.grid(row=0, column=1, padx=5)

        self.btn_pnl = tk.Button(self.frame_actions, text="Calculer PnL", command=self.afficher_pnl)
        self.btn_pnl.grid(row=0, column=2, padx=5)

        self.btn_graph = tk.Button(self.frame_actions, text="Afficher Graphique", command=self.afficher_graphique)
        self.btn_graph.grid(row=0, column=3, padx=5)

        # Zone d'affichage des résultats
        self.text_output = tk.Text(self.frame_output, height=10)
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        self.btn_export = tk.Button(self.frame_actions, text="Exporter Portefeuille", command=self.exporter_portefeuille)
        self.btn_export.grid(row=0, column=5, padx=5)
        
    
    def importer_portefeuille(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner un fichier Excel",
            filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
        )
        if not filename:
            return
    
        try:
            df = pd.read_excel(filename)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier Excel.\n{e}")
            return
    
        colonnes_attendues = ["Classe", "Nom", "Quantité", "Prix dachat", "Date de transaction"]
        for col in colonnes_attendues:
            if col not in df.columns:
                messagebox.showerror("Erreur", f"Colonne '{col}' manquante.")
                return
    
        for idx, row in df.iterrows():
            classe = str(row["Classe"]).strip()
            nom = str(row["Nom"]).strip()
    
            # Quantité
            try:
                quantite = float(row["Quantité"])
            except ValueError:
                messagebox.showwarning("Avertissement", f"Ligne {idx}: Quantité invalide, ignorée.")
                continue
    
            
            try:
                prix_achat = float(row["Prix dachat"])
            except ValueError:
                prix_achat = None
    
            
            try:
                date_transaction = pd.to_datetime(row["Date de transaction"]).date()
            except Exception:
                messagebox.showwarning("Avertissement", f"Ligne {idx}: Date de transaction invalide, ignorée.")
                continue
    
            
            if classe.lower() == "action":
                actif = Action(nom, quantite, date_transaction, prix_achat=prix_achat)
            elif classe.lower() == "crypto":
                actif = Crypto(nom, quantite, date_transaction, prix_achat=prix_achat)
            elif classe.lower() == "obligation":
                actif = Obligation(nom, quantite, date_transaction, taux_coupon=0.0, prix_achat=prix_achat)
            else:
                messagebox.showwarning("Avertissement", f"Ligne {idx}: Classe '{classe}' inconnue, ignorée.")
                continue
    
            self.portefeuille.ajouter_actif(actif)
    
        messagebox.showinfo("Succès", "Portefeuille importé avec succès.")
        self.afficher_portefeuille()

    def exporter_portefeuille(self):
        """
        Exporte le portefeuille actuel dans un fichier Excel.
        On demande à l'utilisateur de choisir le nom et l'emplacement du fichier.
        Le fichier contiendra pour chaque actif : 
          - Classe
          - Nom
          - Quantité
          - Date de transaction
          - Prix d'achat
          - Prix de marché
          - (Taux Coupon pour les obligations)
        """
        filename = filedialog.asksaveasfilename(
            title="Enregistrer le portefeuille",
            defaultextension=".xlsx",
            filetypes=[("Fichiers Excel", "*.xlsx")]
        )
        if not filename:
            return

        data = []
        for actif in self.portefeuille.actifs:
            asset_data = {
                "Classe": actif.__class__.__name__,
                "Nom": actif.nom,
                "Quantité": actif.quantite,
                "Date de transaction": actif.date_transaction.strftime("%Y-%m-%d") 
                                        if isinstance(actif.date_transaction, datetime.date)
                                        else actif.date_transaction,
                "Prix d'achat": actif.prix_achat,
                "Prix de marché": actif.prix_marche
            }
            if isinstance(actif, Obligation):
                asset_data["Taux Coupon"] = actif.taux_coupon
            else:
                asset_data["Taux Coupon"] = None
            data.append(asset_data)

        df = pd.DataFrame(data)
        try:
            df.to_excel(filename, index=False)
            messagebox.showinfo("Succès", f"Portefeuille exporté dans {filename}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation du portefeuille : {e}")

    
    def ajouter_actif(self):
        asset_type = self.asset_type.get()
        nom = self.entry_nom.get().strip()
        try:
            quantite = float(self.entry_quantite.get().strip())
        except ValueError:
            messagebox.showerror("Erreur", "Quantité invalide.")
            return
        date_str = self.entry_date.get().strip()
        try:
            date_transaction = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Erreur", "Date invalide. Format attendu: YYYY-MM-DD")
            return

        prix_achat_str = self.entry_prix_achat.get().strip()
        prix_achat = float(prix_achat_str) if prix_achat_str else None

        if asset_type == "Action":
            actif = Action(nom, quantite, date_transaction, prix_achat)
        elif asset_type == "Obligation":
            taux_coupon_str = self.entry_taux_coupon.get().strip()
            try:
                taux_coupon = float(taux_coupon_str) if taux_coupon_str else 0.0
            except ValueError:
                messagebox.showerror("Erreur", "Taux coupon invalide.")
                return
            actif = Obligation(nom, quantite, date_transaction, taux_coupon, prix_achat)
        elif asset_type == "Crypto":
            actif = Crypto(nom, quantite, date_transaction, prix_achat)
        else:
            messagebox.showerror("Erreur", "Type d'actif inconnu.")
            return

        self.portefeuille.ajouter_actif(actif)
        messagebox.showinfo("Succès", f"Actif {nom} ajouté.")
        self.effacer_champs()
        self.afficher_portefeuille()

    def supprimer_actif(self):
        nom = self.entry_nom.get().strip()
        quantite_str = self.entry_quantite.get().strip()
        quantite = None
        if quantite_str:
            try:
                quantite = float(quantite_str)
            except ValueError:
                messagebox.showerror("Erreur", "Quantité invalide.")
                return
        self.portefeuille.supprimer_actif(nom, quantite)
        self.afficher_portefeuille()

    def afficher_valorisation(self):
        self.portefeuille.mise_a_jour_prix_actifs()
        valorisation = self.portefeuille.valorisation_totale()
        self.text_output.insert(tk.END, f"Valorisation totale du portefeuille: {valorisation}\n")

    def afficher_pnl(self):
        pnl_details, pnl_total = self.portefeuille.calcul_pnl()
        self.text_output.insert(tk.END, "PnL par actif:\n")
        for nom, pnl in pnl_details.items():
            self.text_output.insert(tk.END, f"{nom}: {pnl}\n")
        self.text_output.insert(tk.END, f"PnL total: {pnl_total}\n")

    def afficher_graphique(self):
        graphique_repartition_portefeuille(self.portefeuille)

    def afficher_portefeuille(self):
        self.text_output.insert(tk.END, "Portefeuille actuel:\n")
        for actif in self.portefeuille.actifs:
            self.text_output.insert(tk.END, f"{actif.nom} - Quantité: {actif.quantite}\n")

    def effacer_champs(self):
        self.entry_nom.delete(0, tk.END)
        self.entry_quantite.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)
        self.entry_prix_achat.delete(0, tk.END)
        self.entry_taux_coupon.delete(0, tk.END)
        
    def afficher_graphique(self):
        new_window = tk.Toplevel(self)
        new_window.title("Graphique de répartition")
    
        fig = construire_camembert(self.portefeuille)

        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()  
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    
def construire_camembert(portefeuille):
    """
    Construit et renvoie un objet Figure contenant le camembert de répartition.
    Ne fait pas d'appel à plt.show() pour ne pas ouvrir de fenêtre Matplotlib.
    """
    portefeuille.mise_a_jour_prix_actifs()
    distribution = {}
    for actif in portefeuille.actifs:
        classe = actif.__class__.__name__
        valeur = actif.valorisation()
        distribution[classe] = distribution.get(classe, 0) + valeur

    labels = list(distribution.keys())
    sizes = list(distribution.values())

    # Création de la figure
    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("Répartition du portefeuille par classe d'actif")
    ax.axis('equal')
    return fig

# ======================  PROGRAMME PRINCIPAL  ======================

if __name__ == "__main__":
    portefeuille = Portefeuille()
    app = Application(portefeuille)
    app.mainloop()
