from typing import Union

# a et b doivent être des nombres
def addition(a: Union[int, float], b: Union[int, float]) -> float:
    return a + b

def afficher_resultat() -> None:
    print(addition(3, 5))  # Les valeurs sont maintenant numériques

afficher_resultat()
