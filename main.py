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


class City:
    """Rappresenta una citta' del giocatore."""

    def __init__(self, nome: str, x: int, y: int, popolazione: int, produzione: int) -> None:
        self.nome = nome
        self.x = x
        self.y = y
        self.popolazione = popolazione
        self.produzione = produzione

    def stato(self) -> str:
        return (
            f"{self.nome} - Posizione: ({self.x}, {self.y}), "
            f"Popolazione: {self.popolazione}, Produzione: {self.produzione}"
        )

if __name__ == "__main__":
    benvenuto()
    game_map = GameMap()
    game_map.stampa_mappa()

    # Crea due citta' in posizioni casuali distinte
    x1, y1 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
    while True:
        x2, y2 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
        if (x2, y2) != (x1, y1):
            break

    citta1 = City("Citta 1", x1, y1, 1000, 10)
    citta2 = City("Citta 2", x2, y2, 1000, 10)

    print(citta1.stato())
    print(citta2.stato())
