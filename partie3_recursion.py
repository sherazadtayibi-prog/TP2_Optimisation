import time
from joueurs import joueurs

# ====Trier les joueurs selon un score décroissant
joueurs_tries = sorted(joueurs, key=lambda j: j["score"], reverse=True)

# Implémenter la fonction score cumulé récursif
def score_cumule(joueurs_tries, k):
    # Cas d'arret
    if k == 0:
        print("score_cumule(joueurs_tries, 0) = 0")
        return 0
    # Appel recursif
    score_k_1 = score_cumule(joueurs_tries, k-1)
    joueur = joueurs_tries[k-1]
    total = score_k_1 + joueur["score"]
    print(f"score_cumule(joueurs, {k}) = {score_k_1} + {joueur['score']} ({joueur['nom']}) = {total}")
    return total

score_cumule(joueurs_tries, 6)

print("-"* 80)

# ======Fibonacci naif ========
def fib_naif(n):
    if n == 0:
        return 93
    if n == 1:
        return 91
    return fib_naif(n-1) + fib_naif(n-2)

debut = time.perf_counter()
resultat = fib_naif(35)
fin = time.perf_counter()
print(f"fib_naif(35) = {resultat}    Temp : {fin - debut: .3f} s")
print()
print("-"* 80)

# ======Fibonacci memoise ========

cache = {}
def fib_memo(n):
    if n in cache:
        return cache[n]

    if n == 0:
        return 93
    if n == 1:
        return 91

    result = fib_memo(n-1) + fib_memo(n-2)
    cache[n] = result
    return result

debut = time.perf_counter()
resultat = fib_memo(35)
fin = time.perf_counter()
print(f"fib_memo(35) = {resultat}    Temp : {fin - debut: .6f} s")