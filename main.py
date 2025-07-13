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
        self.cities = []

    def add_city(self, city: "City") -> None:
        """Aggiunge una citta' alla mappa."""
        self.cities.append(city)

    def stampa_mappa(self) -> None:
        """Stampa la mappa convertendo i terreni in simboli."""

        simboli = {
            "pianura": "P",
            "collina": "C",
            "montagna": "M",
            "foresta": "F",
        }
        for r, riga in enumerate(self.griglia):
            simboli_riga = []
            for c, terreno in enumerate(riga):
                if any(city.x == r and city.y == c for city in self.cities):
                    simboli_riga.append("S")
                else:
                    simboli_riga.append(simboli[terreno])
            print(" ".join(simboli_riga))


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


class Unit:
    """Rappresenta un'unita' militare."""

    def __init__(self, nome: str, tipo: str, x: int, y: int, mov: int) -> None:
        self.nome = nome
        self.tipo = tipo
        self.x = x
        self.y = y
        self.mov = mov

    def muovi(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

if __name__ == "__main__":
    benvenuto()
    game_map = GameMap()

    # Crea due citta' in posizioni casuali distinte
    x1, y1 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
    while True:
        x2, y2 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
        if (x2, y2) != (x1, y1):
            break

    citta1 = City("Citta 1", x1, y1, 1000, 10)
    citta2 = City("Citta 2", x2, y2, 1000, 10)

    game_map.add_city(citta1)
    game_map.add_city(citta2)

    game_map.stampa_mappa()

    print(citta1.stato())
    print(citta2.stato())

    # Posiziona un'unita' accanto a ciascuna citta'
    def pos_accanto(x: int, y: int) -> tuple[int, int]:
        if x + 1 < game_map.size:
            return x + 1, y
        return x - 1, y

    unita1 = Unit("Unita 1", "guerriero", *pos_accanto(x1, y1), 2)
    unita2 = Unit("Unita 2", "guerriero", *pos_accanto(x2, y2), 2)

    # Ciclo di gioco per 5 turni
    for turno in range(1, 6):
        print(f"\n-- Turno {turno} --")
        for city in (citta1, citta2):
            city.popolazione += 100
            city.produzione += 2
            print(city.stato())
