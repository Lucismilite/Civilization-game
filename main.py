# main.py
# Entry point del gioco Civilization-like

import random
import json


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

    def stampa_mappa(self, unita: list["Unit"] | None = None) -> None:
        """Stampa la mappa convertendo i terreni in simboli.

        Se presente una unita' nella cella viene mostrata ``U``. Se la cella
        ospita una citta' viene mostrato ``S``.
        """

        simboli = {
            "pianura": "P",
            "collina": "C",
            "montagna": "M",
            "foresta": "F",
        }
        unita = unita or []
        for r, riga in enumerate(self.griglia):
            simboli_riga = []
            for c, terreno in enumerate(riga):
                if any(u.x == r and u.y == c for u in unita):
                    simboli_riga.append("U")
                elif any(city.x == r and city.y == c for city in self.cities):
                    simboli_riga.append("S")
                else:
                    simboli_riga.append(simboli[terreno])
            print(" ".join(simboli_riga))

# Bonus di risorse per i vari terreni
TERRAIN_BONUS = {
    "pianura": {"cibo": 20, "oro": 0, "legno": 5},
    "collina": {"cibo": 10, "oro": 0, "legno": 15},
    "montagna": {"cibo": 5, "oro": 20, "legno": 5},
    "foresta": {"cibo": 10, "oro": 0, "legno": 20},
}

# Definizione edifici e bonus
EDIFICI_DISPONIBILI = {
    "Mulino": {"produzione": 3},
    "Mercato": {"popolazione": 100},
}

# Bonus di risorse che derivano dagli edifici
EDIFICI_RISORSE = {
    "Mulino": {"cibo": 10},
    "Mercato": {"oro": 10},
}


class City:
    """Rappresenta una citta' del giocatore."""

    def __init__(self, nome: str, x: int, y: int, popolazione: int, produzione: int, terreno: str) -> None:
        self.nome = nome
        self.x = x
        self.y = y
        self.popolazione = popolazione
        self.produzione = produzione
        self.terreno = terreno
        self.edifici: list[str] = []
        self.risorse = {"cibo": 0, "oro": 0, "legno": 0}

    def stato(self) -> str:
        edifici = ", ".join(self.edifici) if self.edifici else "Nessuno"
        ris = ", ".join(f"{k}:{v}" for k, v in self.risorse.items())
        return (
            f"{self.nome} - Posizione: ({self.x}, {self.y}), "
            f"Popolazione: {self.popolazione}, Produzione: {self.produzione}, "
            f"Edifici: {edifici}, Risorse: {ris}"
        )

    def costruisci_edificio(self, disponibili: dict[str, dict]) -> str | None:
        restanti = [e for e in disponibili if e not in self.edifici]
        if not restanti:
            return None
        edificio = random.choice(restanti)
        self.edifici.append(edificio)
        bonus = disponibili[edificio]
        self.produzione += bonus.get("produzione", 0)
        self.popolazione += bonus.get("popolazione", 0)
        return edificio

    def produci_risorse(self, terreni_bonus: dict[str, dict], edifici_bonus: dict[str, dict]) -> None:
        bonus = terreni_bonus.get(self.terreno, {})
        for k, v in bonus.items():
            self.risorse[k] += v
        for ed in self.edifici:
            for k, v in edifici_bonus.get(ed, {}).items():
                self.risorse[k] += v
        while self.risorse["cibo"] >= 1000:
            self.risorse["cibo"] -= 1000
            self.popolazione += 500

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


def muovi_verso(unita: "Unit", dest_x: int, dest_y: int) -> None:
    """Muove l'unita' di un passo verso le coordinate fornite."""

    dx = 0
    dy = 0
    if unita.x < dest_x:
        dx = 1
    elif unita.x > dest_x:
        dx = -1

    if unita.y < dest_y:
        dy = 1
    elif unita.y > dest_y:
        dy = -1

    unita.muovi(dx, dy)
    print(f"{unita.nome} si muove a ({unita.x}, {unita.y})")

def ia_unita(unita: Unit, propria: City, nemica: City) -> str:
    dist_enemy = abs(unita.x - nemica.x) + abs(unita.y - nemica.y)
    dist_home = abs(unita.x - propria.x) + abs(unita.y - propria.y)
    if dist_enemy <= dist_home:
        muovi_verso(unita, nemica.x, nemica.y)
        return "avanza verso la citta' nemica"
    else:
        muovi_verso(unita, propria.x, propria.y)
        return "torna a difendere"


def azione_citta(citta: City, turno: int) -> str:
    azione = "nessuna"
    # produzione risorse
    citta.produci_risorse(TERRAIN_BONUS, EDIFICI_RISORSE)
    if turno % 3 == 0:
        costruito = citta.costruisci_edificio(EDIFICI_DISPONIBILI)
        if costruito:
            azione = f"costruisce {costruito}"
    elif citta.risorse["oro"] > 200:
        citta.produzione += 1
        citta.risorse["oro"] -= 200
        azione = "aumenta la produzione"
    elif citta.risorse["cibo"] > 500:
        citta.popolazione += 50
        citta.risorse["cibo"] -= 500
        azione = "aumenta la popolazione"
    return azione


def evento_casuale(citta: City) -> str | None:
    eventi = [
        ("Carestia", lambda c: c.risorse.update(c.risorse | {"cibo": max(0, c.risorse["cibo"] - 100)})),
        ("Invasione", lambda c: setattr(c, "popolazione", max(0, c.popolazione - 100))),
        ("Scoperta", lambda c: c.risorse.update({"oro": c.risorse["oro"] + 50})),
    ]
    if random.random() < 0.3:
        nome, effetto = random.choice(eventi)
        effetto(citta)
        return nome
    return None


def salva_gioco(filename: str, game_data: dict) -> None:
    with open(filename, "w") as f:
        json.dump(game_data, f, indent=2)


def carica_gioco(filename: str) -> dict:
    with open(filename) as f:
        return json.load(f)

def mostra_stato(mappa: GameMap, citta: list[City], unita: list[Unit]) -> None:
    """Stampa la mappa insieme allo stato di citta' e unita'."""

    mappa.stampa_mappa(unita)
    for city in citta:
        print(city.stato())
    for u in unita:
        print(f"{u.nome} - Posizione: ({u.x}, {u.y})")


def verifica_scontri(unita: list[Unit]) -> None:
    """Rimuove le unita' che si trovano sulla stessa cella."""

    if len(unita) < 2:
        return

    pos = {}
    to_remove = []
    for u in unita:
        key = (u.x, u.y)
        if key in pos:
            print("Scontro!")
            to_remove.append(u)
            to_remove.append(pos[key])
        else:
            pos[key] = u

    for u in to_remove:
        if u in unita:
            unita.remove(u)

if __name__ == "__main__":
    benvenuto()
    print("Modalita' spettatore IA contro IA")
    game_map = GameMap()

    # Crea due citta' in posizioni casuali distinte
    x1, y1 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
    while True:
        x2, y2 = random.randint(0, game_map.size - 1), random.randint(0, game_map.size - 1)
        if (x2, y2) != (x1, y1):
            break
    terreno1 = game_map.griglia[x1][y1]
    terreno2 = game_map.griglia[x2][y2]
    citta1 = City("Citta 1", x1, y1, 1000, 10, terreno1)
    citta2 = City("Citta 2", x2, y2, 1000, 10, terreno2)

    game_map.add_city(citta1)
    game_map.add_city(citta2)

    # Posiziona un'unita' accanto a ciascuna citta'
    def pos_accanto(x: int, y: int) -> tuple[int, int]:
        if x + 1 < game_map.size:
            return x + 1, y
        return x - 1, y

    unita1 = Unit("Unita 1", "guerriero", *pos_accanto(x1, y1), 2)
    unita2 = Unit("Unita 2", "guerriero", *pos_accanto(x2, y2), 2)

    unita = [unita1, unita2]

    # Stato iniziale
    mostra_stato(game_map, [citta1, citta2], unita)
    # Ciclo di gioco IA vs IA
    for turno in range(1, 11):
        print(f"\n-- Turno {turno} --")
        for city in (citta1, citta2):
            az_citta = azione_citta(city, turno)
            evento = evento_casuale(city)
            msg = f"IA {city.nome}: {az_citta}"
            if evento:
                msg += f" | Evento: {evento}"
            print(msg)

        az1 = ia_unita(unita1, citta1, citta2)
        az2 = ia_unita(unita2, citta2, citta1)
        print(f"IA {unita1.nome}: {az1}")
        print(f"IA {unita2.nome}: {az2}")

        verifica_scontri(unita)
        mostra_stato(game_map, [citta1, citta2], unita)

    salva_gioco("save.json", {
        "citta": [city.__dict__ for city in (citta1, citta2)],
        "unita": [u.__dict__ for u in unita],
    })
