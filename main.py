# main.py
# Entry point del gioco Civilization-like

import random


def benvenuto():
    print("Benvenuto in Civilization Game!")


class GameMap:
    """Rappresenta una mappa di gioco 10x10."""

    def __init__(self, size: int = 10) -> None:
        self.size = size
        tipi_terreno = ["pianura", "collina", "montagna", "foresta"]
        self.griglia = [
            [random.choice(tipi_terreno) for _ in range(size)] for _ in range(size)
        ]

    def stampa_mappa(self) -> None:
        """Stampa la mappa convertendo i terreni in simboli."""

        simboli = {
            "pianura": "P",
            "collina": "C",
            "montagna": "M",
            "foresta": "F",
        }
        for riga in self.griglia:
            print(" ".join(simboli[cel] for cel in riga))

if __name__ == "__main__":
    benvenuto()
    game_map = GameMap()
    game_map.stampa_mappa()
