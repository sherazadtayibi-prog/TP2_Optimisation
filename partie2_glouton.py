from joueurs import joueurs
from itertools import combinations
import matplotlib.pyplot as plt

nombre_joueurs = len(joueurs)
joueurs_id = range(nombre_joueurs)  # 0..7

Budget_max= 8500
Poids_max= 250
Taille_equipe=3

# Valeurs de PuLP
score_global = 524
budget_total = 8450

# 1- Construire les équipes
#================================
def construire_equipe(joueurs_tries, nom_strategie):
    equipe_A= []
    equipe_B= []
    poids_A= 0
    poids_B= 0
    Budget_total= 0

    # Parcourire les joueures selon la strategie
    for j in joueurs_tries:
        poids = j["poids"]
        salaire = j["salaire"]

        # Ajout dans l'équipe A
        if len(equipe_A) < Taille_equipe:
            if (Budget_total + salaire) <= Budget_max and (poids_A + poids) <= Poids_max:
                equipe_A.append(j)
                Budget_total += salaire
                poids_A += poids
                continue

        # Ajout dans l'équipe B
        if len(equipe_B) < Taille_equipe:
            if (Budget_total + salaire) <= Budget_max and (poids_B + poids) <= Poids_max:
                equipe_B.append(j)
                Budget_total += salaire
                poids_B += poids
                continue

    # Vérification des contraintes
    if len(equipe_A) != Taille_equipe or len(equipe_B) != Taille_equipe :
        print(f"\n ERREUR {nom_strategie} : impossible de former deux equipes ")
        print(f"Taille equipe A : {len(equipe_A)}")
        print(f"Taille equipe B  : {len(equipe_B)}")
        print(f"Une des contraintes empeche de completer les equipes")

    # Calcule du score total
    Score_total = sum(j["score"] for j in equipe_A + equipe_B)

    return {
        "nom": nom_strategie,
        "equipe_A": equipe_A,
        "equipe_B": equipe_B,
        "score_total": Score_total,
        "budget_total": Budget_total,
        "poids_A": poids_A,
        "poids_B": poids_B,
    }

# 2- Stratégie_1 : Meilleur score absolu (on trie les joueurs par score decroissant)
#===========================================
def score_absolue():
    joueurs_tries =sorted(joueurs, key=lambda j: j["score"], reverse=True)
    return construire_equipe(joueurs_tries, "Strategie_1 : Meilleur score absolue")

# 3- Stratégie_2 : Meilleur ratio score/salaire (Qualité_prix, on trie les joueur par ratio (score/salaire) decroissant)
#=================================================
def ratio_score_salaire():
    joueurs_tries = sorted(joueurs, key=lambda j: j["score"] / j["salaire"], reverse=True)
    return construire_equipe(joueurs_tries, "Strategie_2 : Meilleur ratio score/salaire ")

# 4- Stratégie_3 : Meilleur ratio score/poids (on favorise les joueurs les plus légères
#================================================
def ratio_score_poids():
    joueurs_tries = sorted(joueurs, key=lambda j: j["score"] / j["poids"], reverse=True)
    return construire_equipe(joueurs_tries, "Strategie_3 : Meilleur ratio score/poids ")

# 5- Strat/gie_4 : Alternence score ratio(score/salaire)
#=========================================================
def alt_score_ratio():
    # Creer une nouvelle liste independante
    joueurs_restands = joueurs.copy()

    joueurs_selectiones = []
    compteur = 0
    while len(joueurs_selectiones) < 6 and joueurs_restands:
        # Meilleur score
        if compteur % 2 == 0:
            joueurs_tries = sorted(joueurs_restands, key=lambda j: j["score"], reverse=True)
        # Meilleur ratio score/salaire
        else:
            joueurs_tries = sorted(joueurs_restands, key=lambda j: j["score"] / j["salaire"], reverse=True)

        meilleur_joueur = joueurs_tries[0]
        joueurs_selectiones.append(meilleur_joueur)

        joueurs_restands.remove(meilleur_joueur)

        compteur += 1

    return construire_equipe(joueurs_selectiones, "Strategie_4 : Alternance score/ratio ")

# 6- Exécution des stratégie et tableau comparatif
#===============================================
def main():
    resultat_1 = score_absolue()
    resultat_2 = ratio_score_salaire()
    resultat_3 = ratio_score_poids()
    resultat_4 = alt_score_ratio()

    # Tableau comparatif
    resultats = [resultat_1, resultat_2, resultat_3, resultat_4]

    print("\n Tableau comparatif des strat/gies gloutonnes vs PuLP \n")
    print(f"{'Stratégies':<50} {'Score total':<12} {'Budget utilisé':<15} {'Écart pts':<10} {'Écart %':<10}")
    print("-" * 100)

    for resultat in resultats:
        score = resultat["score_total"]
        budget = resultat["budget_total"]
        ecart_glout_PuLP = score - score_global
        ecart_pourcentage = (ecart_glout_PuLP/score_global)*100

        print(f"{resultat['nom']:<50} {score:<12} {budget:<15} {ecart_glout_PuLP:<15} {ecart_pourcentage:<10.2f}%")

    # Ligne de référence PuLP
    print("-" * 100)
    print(f"{'PuLP':<50} {score_global:<12} {budget_total:<15}")

    # === Graphique comparatif des scores===
    scores_dict = {
        "Strategie_1": resultat_1["score_total"],
        "Strategie_2": resultat_2["score_total"],
        "Strategie_3": resultat_3["score_total"],
        "Strategie_4": resultat_4["score_total"],
        "PuLP (optimal)": score_global
    }
    couleurs = ["steelblue", "salmon", "green", "yellow", "turquoise"]

    plt.figure(figsize=(10, 6))
    plt.bar(scores_dict.keys(), scores_dict.values(), color=couleurs)

    plt.axhline(y=score_global, linestyle="--", color="red", linewidth=2, label="PuLP optimal")
    plt.title("PuLP vs Glouton")
    plt.xlabel("Strategies")
    plt.ylabel("Score")
    plt.xticks(rotation=30)

    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()




