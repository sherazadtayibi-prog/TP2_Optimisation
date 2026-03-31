import pulp as pl
import time
from joueurs import joueurs
import matplotlib.pyplot as plt
import numpy as np

nombre_joueurs = len(joueurs)
joueurs_id = range(nombre_joueurs)  # 0..7

# 1- Modèle
# -----------------------
prob = pl.LpProblem("Selection_Optimale_Equipes", pl.LpMaximize)

# -----------------------
# 2- Variables binaires
# -----------------------
# x_iA et x_iB pour chaque joueur i
xA = pl.LpVariable.dicts("xA", joueurs_id, lowBound=0, upBound=1, cat=pl.LpBinary)
xB = pl.LpVariable.dicts("xB", joueurs_id, lowBound=0, upBound=1, cat=pl.LpBinary)

# -----------------------
# 3- Fonction objective
prob += pl.lpSum(joueurs[i]["score"] * (xA[i] + xB[i]) for i in joueurs_id), "Score_total"

# -----------------------
# 4- Contraintes
# -----------------------

# 1- Taille des équipes : 3 joueurs par équipe
prob += pl.lpSum(xA[i] for i in joueurs_id) == 3, "Taille_equipe_A"
prob += pl.lpSum(xB[i] for i in joueurs_id) == 3, "Taille_equipe_B"

# 2- Un joueur au plus dans une équipe
for i in joueurs_id:
    prob += xA[i] + xB[i] <= 1, f"Un_seul_club_pour_joueur_{i}"

# 3- Budget total <= 8500
prob += pl.lpSum(joueurs[i]["salaire"] * (xA[i] + xB[i]) for i in joueurs_id) <= 8500, "Budget_total"

# 4- Poids max par équipe : 250 kg
prob += pl.lpSum(joueurs[i]["poids"] * xA[i] for i in joueurs_id) <= 250, "Poids_equipe_A"
prob += pl.lpSum(joueurs[i]["poids"] * xB[i] for i in joueurs_id) <= 250, "Poids_equipe_B"

# -----------------------
# 5- Résolution
# -----------------------
prob.solve(pl.PULP_CBC_CMD(msg=False))

print("Status:", pl.LpStatus[prob.status])

# -----------------------
# 6- Affichage des équipes
# -----------------------
equipe_A = []
equipe_B = []

for i in joueurs_id:
    if pl.value(xA[i]) == 1:
        equipe_A.append(joueurs[i])
    if pl.value(xB[i]) == 1:
        equipe_B.append(joueurs[i])

def resume_equipe(nom, equipe):
    score_total = sum(j["score"] for j in equipe)
    salaire_total = sum(j["salaire"] for j in equipe)
    poids_total = sum(j["poids"] for j in equipe)
    print(f"\n{nom}:")
    for j in equipe:
        print(f"  - {j['nom']} | score={j['score']} | salaire={j['salaire']} | poids={j['poids']}")
    print(f"  Score total  = {score_total}")
    print(f"  Salaire total = {salaire_total}")
    print(f"  Poids total   = {poids_total}")

resume_equipe("Équipe A", equipe_A)
resume_equipe("Équipe B", equipe_B)

print("\nScore total global =", pl.value(prob.objective))

# -----------------------
# 7- Graphique-1: Budget et poids par equipe
# -----------------------
# Calcul des valeurs
budget_A = sum(j["salaire"] for j in equipe_A)
budget_B = sum(j["salaire"] for j in equipe_B)

poids_A = sum(j["poids"] for j in equipe_A)
poids_B = sum(j["poids"] for j in equipe_B)

# Bornes maximales autorisées
max_budget = 8500
max_poids = 250

# Données pour Matplotlib
labels = ["Budget", "Poids"]
equipeA_vals = [budget_A, poids_A]
equipeB_vals = [budget_B, poids_B]
max_vals = [max_budget, max_poids]

# Positionnement des barres sur l'axe X et leur largeur
x = np.arange(len(labels))
width = 0.35

# Création du graphique
plt.figure(figsize=(8, 5))

# Barres d'équipes A et B
plt.bar(x - width/2, equipeA_vals, width, label="Équipe A", color="steelblue")
plt.bar(x + width/2, equipeB_vals, width, label="Équipe B", color="salmon")

# Lignes horizontales des contraintes
# Droite verte pointillée pour le budget maximal
plt.axhline(max_budget, color="green", linestyle="--", label="Budget max")

# Droite orange pointillée , poids maximal
plt.axhline(max_poids, color="orange", linestyle="--", label="Poids max")

plt.xticks(x, labels)  # remplacer 0 et 1 par 'Budget' et 'Poids'
plt.ylabel("Valeurs")
plt.title("Répartition du budget et du poids par équipe (PuLP)")
plt.legend()
plt.tight_layout()  # Ajuste les marges


# -----------------------
# 8- Graphique-2: Profil des joueurs selectionnes
# -----------------------
# Récupération des valeurs
scores = [j["score"] for j in equipe_A + equipe_B]
salaires = [j["salaire"] for j in equipe_A + equipe_B]
poids = [j["poids"] for j in equipe_A + equipe_B]
noms = [j["nom"] for j in equipe_A + equipe_B]

# Normalisation
def normaliser(values):
    return [(v - min(values)) / (max(values) - min(values)) for v in values]

scores_norm = normaliser(scores)
salaires_norm = normaliser(salaires)
poids_norm = normaliser(poids)

# Position et largeur des barres sur l'axe X
x = np.arange(len(noms))
width = 0.25

# Création de la figure
plt.figure(figsize=(10, 6))

# barres pour le score normalisé, le salaire et le poids normalisés
plt.bar(x - width, scores_norm, width, label="Score normalisé", color="purple")
plt.bar(x, salaires_norm, width, label="Salaire normalisé", color="green")
plt.bar(x + width, poids_norm, width, label="Poids normalisé", color="orange")

plt.xticks(x, noms, rotation=45)
plt.ylabel("Valeurs normalisées (0 à 1)")
plt.title("Profil des joueurs sélectionnés par PuLP")
plt.legend()
plt.tight_layout()


plt.show()