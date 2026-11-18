# TP : Architecture Multi-Thread et Intelligence Artificielle appliquées au Jeu d'Échecs

* **Niveau :** Master 1 Informatique

* **Durée estimée :** 4h à 6h

* **Langage :** Python 3.11+ (typage statique strict requis)

* **Thèmes abordés :** Programmation concurrente (`Thread`, `Lock`, `Event`, `Queue`), patrons de conception (*Singleton*, *Strategy*, *Observer*, *Builder*, *Proxy*), immutabilité, algorithme Minimax.

## Partie I : Sujet de TP (Distribution Étudiants)

### 1. Contexte et Objectifs Pédagogiques

Vous disposez d'une base logicielle d'un jeu d'échecs structurée autour de plusieurs patrons de conception (*Design Patterns*) :

* **Singleton (`constructor_patterns.py`) :** Garantit l'unicité de l'échiquier (`Board`).

* **Builder & Immutabilité (`pieces.py`) :** Construction fluide des pièces (`PieceBuilder`) sous forme d'objets immuables (`@dataclass(frozen=True)`).

* **Strategy (`moves.py`) :** Encapsulation des règles de déplacement (`StraightMove`, `DigonalMove`, `KnightMove`, `PawnMove`).

* **Observer (`board.py`) :** Notification automatique des composants abonnés lors d'un mouvement sur le plateau.

* **Proxy (`human.py`) :** Contrôle d'accès autour des actions du joueur humain (`HumanProxy`).

**Votre mission** consiste à transformer ce prototype en un moteur d'échecs fonctionnel, doté d'une véritable intelligence artificielle et orchestrant plusieurs fils d'exécution (*threads*) concurrents sans interblocage (*deadlock*) ni condition de course (*race condition*).

### 2. Jalon 1 : Implémenter les vraies règles des échecs

Actuellement, `Board.move_piece()` déplace n'importe quelle pièce sans contrôle et `MoveStrategy.get_targets()` génère des coordonnées théoriques sans tenir compte des bords du plateau ni des obstacles.

#### Travail à réaliser

1. **Initialisation de l'échiquier (`board.py`) :**

   * Complétez l'initialisation de `self.__grid` (matrice de taille $8 \times 8$) avec les 32 pièces réglementaires en utilisant `PieceBuilder` et les valeurs standards :

     * Pion : $1$, Cavalier : $3$, Fou : $3$, Tour : $5$, Reine : $9$, Roi : $1000$.

   * Implémentez une méthode `get_snapshot(self) -> list[list[Piece | None]]` qui renvoie une copie de la matrice du plateau.

   * *Question de conception :* Pourquoi une copie superficielle de la matrice (`[row[:] for row in self.__grid]`) suffit-elle ici pour garantir la sécurité entre threads ?

2. **Validation des trajectoires et obstacles (`moves.py`) :**

   * Faites évoluer la signature de `MoveStrategy.get_targets` pour lui fournir le contexte du plateau :

     ```
     def get_targets(
         self,
         start_x: int,
         start_y: int,
         grid: list[list[Piece | None]],
         color: Color,
     ) -> list[tuple[int, int]]: ...
     
     ```

   * Éliminez toutes les coordonnées sortant de l'échiquier ($0 \le x, y < 8$).

   * **Gestion des collisions :** Pour `StraightMove` et `DigonalMove`, parcourez chaque direction pas à pas et interrompez la progression dès qu'une pièce bloque le passage (la case est ajoutée si la pièce est adverse, ignorée si elle est alliée).

   * **Règles du Pion (`PawnMove`) :** Le pion avance tout droit uniquement si la case cible est libre (et sur $2$ cases lors de son premier coup si les deux cases sont libres). Il ne peut se déplacer en diagonale que pour capturer une pièce adverse.

3. **Arbitrage, score et fin de partie (`board.py`, `game.py`) :**

   * Créez une exception personnalisée `IllegalMoveError(Exception)`.

   * Dans `Board.move_piece()`, vérifiez que la pièce existe, que la destination appartient aux cibles légales, et que le coup ne laisse pas le Roi du joueur en échec.

   * En cas de capture d'une pièce adverse, ajoutez sa propriété `value` au score du joueur dans `players_scores`.

   * Détectez l'échec et mat (le joueur suivant est en échec et ne dispose d'aucun coup légal) et basculez l'état de `Game` vers `Status.FINISHED`.

### 3. Jalon 2 : Rendre `AiVirtualPlayer` intelligent (Algorithme Minimax)

L'IA ne doit plus jouer au hasard ou de manière scriptée. Elle doit anticiper les coups grâce à l'algorithme **Minimax**.

#### Travail à réaliser

1. **Fonction d'évaluation heuristique :**

   * Écrivez une méthode `evaluate_board(self, grid: list[list[Piece | None]]) -> float` qui évalue l'avantage matériel de l'IA :
     

     $$
     \text{Score} = \sum_{p \in \text{IA}} \text{valeur}(p) - \sum_{p \in \text{Adversaire}} \text{valeur}(p)
     $$

   * *(Bonus)* Ajoutez un léger bonus ($+0.2$ point) pour chaque pièce contrôlant ou occupant les 4 cases centrales $(3,3)$, $(3,4)$, $(4,3)$ et $(4,4)$.

2. **Exploration Minimax (profondeur** $d = 2$ **ou** $d = 3$**) :**

   * Implémentez l'algorithme récursif Minimax sur des grilles simulées (copies de la matrice) afin de ne jamais altérer l'état réel de `Board` ni déclencher les observateurs pendant la recherche.

3. **Contrainte stricte de concurrence :**

   * Le calcul Minimax peut prendre plusieurs centaines de millisecondes. **Il est strictement interdit de conserver le `Lock` partagé pendant ce calcul**, sous peine de figer l'horloge et l'interface utilisateur.

   * Votre méthode de jeu dans `AiVirtualPlayer` doit impérativement respecter le séquencement en 3 phases :

     1. **Phase 1 (Verrouillée) :** Acquérir `self.__lock` $\rightarrow$ récupérer `snapshot = self.__board.get_snapshot()` $\rightarrow$ libérer `self.__lock`.

     2. **Phase 2 (Libre) :** Exécuter `minimax(snapshot, depth=3, ...)` sans aucun verrou.

     3. **Phase 3 (Verrouillée) :** Acquérir `self.__lock` $\rightarrow$ vérifier que `self.__game.status is Status.PLAYING` $\rightarrow$ appliquer le meilleur coup via `self.__board.move_piece(...)` $\rightarrow$ libérer `self.__lock`.

### 4. Jalon 3 : Développer 2 nouveaux Threads

Vous devez enrichir l'architecture concurrente du logiciel en implémentant **deux nouveaux threads** reposant sur des mécanismes de synchronisation distincts.

| Thread à implémenter | Rôle dans l'application | Primitives mobilisées | 
| ----- | ----- | ----- | 
| **`ChessClockThread`** | Pendule d'échecs décomptant le temps réel de chaque camp. | `Thread`, `Lock`, `Event`, `Observer` | 
| **`MoveLoggerThread`** | Sauvegarde asynchrone des coups dans un fichier `partie.pgn`. | `Thread`, `queue.Queue` (Producteur-Consommateur) | 

#### 4.1. `ChessClockThread` (Temps réel & Patron Observer)

Remplacez la classe passive `Clock` de `board.py` par un véritable thread actif :

* Initialise deux compteurs de temps (ex. $300.0$ secondes pour `Color.WHITE` et `Color.BLACK`) et un attribut `__active_color = Color.WHITE`.

* Implémente le protocole `Observer` et s'abonne à `Board`. À chaque coup joué (`notify()`), la pendule bascule `__active_color` vers l'adversaire sous la protection de son verrou interne `__clock_lock`.

* Dans sa boucle `run()`, attend par pas de $0.1\text{ s}$ via `self.__stop_event.wait(0.1)` et décrémente le temps du joueur actif. Si le chronomètre atteint $0.0\text{ s}$, la partie est immédiatement terminée (`Status.FINISHED`) avec annonce du vainqueur au temps.

#### 4.2. `MoveLoggerThread` (Modèle Producteur-Consommateur)

Les entrées/sorties disque (I/O) sont lentes et ne doivent pas ralentir le moteur de jeu :

* **Producteur :** Un observateur abonné à `Board` formate chaque coup joué (ex. `"Coup #1 [WHITE] : (1, 0) -> (2, 2)"`) et le dépose dans une instance partagée de `queue.Queue`.

* **Consommateur (`MoveLoggerThread`) :**

  * Bloque en attente d'un message via `self.__log_queue.get()`.

  * Écrit la ligne dans le fichier `partie.pgn` (ajoutez un `sleep(0.05)` pour simuler une latence disque et observer l'asynchronicité) puis appelle `self.__log_queue.task_done()`.

  * Gère l'arrêt propre grâce à une **valeur sentinelle** (`None`) envoyée dans la file par `main.py` lors de la fermeture du programme.

#### 4.3. Squelettes de départ à compléter

```
from queue import Queue
from threading import Event, Lock, Thread
from time import sleep
from typing import override

from .board import Observer
from .game import Game, Status
from .pieces import Color


class ChessClockThread(Thread, Observer):
    def __init__(self, initial_seconds: float, game: Game) -> None:
        Thread.__init__(self, name="chess-clock-thread")
        self.__times: dict[Color, float] = {
            Color.WHITE: initial_seconds,
            Color.BLACK: initial_seconds,
        }
        self.__active_color: Color = Color.WHITE
        self.__game: Game = game
        self.__clock_lock: Lock = Lock()
        self.__stop_event: Event = Event()

    @override
    def notify(self, *args, **kwargs) -> None:
        # TODO : Basculer self.__active_color de manière thread-safe
        pass

    @override
    def run(self) -> None:
        # TODO : Décrémenter toutes les 0.1s le temps du joueur actif.
        # Si temps <= 0 : basculer game vers Status.FINISHED et stopper le thread.
        pass

    def stop(self) -> None:
        self.__stop_event.set()


class MoveLoggerThread(Thread):
    def __init__(
        self, log_queue: Queue[str | None], filepath: str = "partie.pgn"
    ) -> None:
        Thread.__init__(self, name="move-logger-thread")
        self.__log_queue: Queue[str | None] = log_queue
        self.__filepath: str = filepath

    @override
    def run(self) -> None:
        # TODO : Lire la file avec get(), écrire dans self.__filepath,
        # appeler task_done() et quitter proprement à réception de None.
        pass

```

#### 4.4. Questions Bonus (Pour aller plus loin)

1. **Singleton Thread-Safe :** Protégez le décorateur `@singleton` dans `constructor_patterns.py` à l'aide d'un `Lock` (*Double-Checked Locking*) afin d'éviter la création de deux instances si deux threads appellent `Board()` simultanément.

2. **Pondering IA (`AiPonderThread`) :** Implémentez un thread qui anticipe le coup de l'humain et calcule la réponse de l'IA pendant le tour de l'humain, mais qui s'interrompt immédiatement via un `threading.Event` si l'humain joue un coup différent de celui anticipé.

## Partie II : Grille d'Évaluation & Guide de Soutenance (Espace Enseignant)

### 1. Barème de notation sur 20 points

| Critère d'évaluation | Points | Indicateurs de réussite attendus | 
| ----- | ----- | ----- | 
| **Jalon 1 : Règles métier des échecs** | **/ 5** | Plateau initialisé ($32$ pièces), collisions gérées sur les diagonales/lignes, règles du pion exactes, détection d'échec/mat et exception `IllegalMoveError`. | 
| **Jalon 2 : IA Minimax & Isolation du `Lock`** | **/ 5** | L'IA choisit des coups cohérents (captures avantageuses, protection du roi). Le `Lock` n'est **jamais** détenu pendant l'appel récursif Minimax. | 
| **Jalon 3a : `ChessClockThread`** | **/ 4** | Décompte précis ($0.1\text{ s}$), bascule *thread-safe* via `Observer.notify()`, arrêt immédiat de la partie lorsque le temps d'un camp expire. | 
| **Jalon 3b : `MoveLoggerThread`** | **/ 4** | Utilisation correcte de `queue.Queue`, écriture asynchrone sans ralentir le jeu, appel systématique à `task_done()`, arrêt propre via sentinelle `None`. | 
| **Cycle de vie & Qualité architecturale** | **/ 2** | Respect des patrons existants, typage propre, aucun thread bloqué à la fermeture (`stop()` + `join()` sur tous les threads). | 

### 2. Les 5 pièges classiques à vérifier en soutenance

1. **Le verrou global pendant Minimax (Anti-pattern majeur) :**

   * *Symptôme :* L'étudiant place `with self.__lock:` englobant tout le corps de `play_turn()` ou `run()` de `AiVirtualPlayer`.

   * *Conséquence :* Pendant que l'IA réfléchit ($1$ à $2\text{ s}$), `ChessClockThread` ou `AiReferee` est bloqué en attente du verrou.

2. **Mutation de la grille partagée pendant la simulation Minimax :**

   * *Symptôme :* Minimax modifie directement `board.__grid` et annule le coup ensuite (*make/unmake*) sur la grille réelle au lieu d'opérer sur `get_snapshot()`.

   * *Conséquence :* Les autres threads lisent un échiquier incohérent rempli de coups « fantômes » en cours de calcul.

3. **Oubli de la sentinelle `None` ou boucle `while True` bloquante sur `Queue` :**

   * *Symptôme :* `MoveLoggerThread` utilise `log_queue.get()` sans sentinelle ni timeout, et `main.py` appelle `logger_thread.join()`.

   * *Conséquence :* Le programme ne se termine jamais (*deadlock* à l'extinction).

4. **Inversion de l'ordre d'acquisition des verrous (*Deadlock* croisé) :**

   * *Symptôme :* Thread A acquiert `shared_lock` puis `clock_lock`, tandis que Thread B acquiert `clock_lock` puis `shared_lock`.

   * *Vérification :* S'assurer que `ChessClockThread` utilise son propre `clock_lock` uniquement pour protéger `__times` et `__active_color`, sans jamais demander le `shared_lock` du plateau à l'intérieur.

5. **Itération non protégée sur `players_scores` :**

   * *Symptôme :* `AiReferee` lit `players_scores.items()` sans acquérir le `Lock` partagé.

## Partie III : Corrigé Type de Référence (Espace Enseignant)

Voici l'implémentation de référence pour les nouveaux composants concurrents et l'intégration dans `main.py`.

### 1. Implémentation de `ChessClockThread` et `MoveLoggerThread`

```
from queue import Queue
from threading import Event, Lock, Thread
from time import sleep
from typing import override

from .board import Observer
from .game import Game, Status
from .pieces import Color


class ChessClockThread(Thread, Observer):
    def __init__(self, initial_seconds: float, game: Game) -> None:
        Thread.__init__(self, name="chess-clock-thread")
        self.__times: dict[Color, float] = {
            Color.WHITE: initial_seconds,
            Color.BLACK: initial_seconds,
        }
        self.__active_color: Color = Color.WHITE
        self.__game: Game = game
        self.__clock_lock: Lock = Lock()
        self.__stop_event: Event = Event()

    @override
    def notify(self, *args, **kwargs) -> None:
        with self.__clock_lock:
            self.__active_color = (
                Color.BLACK
                if self.__active_color is Color.WHITE
                else Color.WHITE
            )

    def get_remaining_time(self, color: Color) -> float:
        with self.__clock_lock:
            return max(0.0, self.__times[color])

    @override
    def run(self) -> None:
        tick: float = 0.1
        while not self.__stop_event.is_set():
            self.__stop_event.wait(tick)
            if self.__stop_event.is_set():
                break

            with self.__clock_lock:
                if self.__game.status is not Status.PLAYING:
                    continue

                self.__times[self.__active_color] -= tick
                if self.__times[self.__active_color] <= 0.0:
                    self.__times[self.__active_color] = 0.0
                    loser = self.__active_color.name
                    print(f"\n[PENDULE] Temps écoulé pour {loser} ! Fin de partie.")
                    self.__game.to_finished_status()
                    self.__stop_event.set()

    def stop(self) -> None:
        self.__stop_event.set()


class MoveLoggerObserver(Observer):
    """Producteur : transforme chaque notification du plateau en message PGN."""

    def __init__(self, log_queue: Queue[str | None]) -> None:
        self.__log_queue: Queue[str | None] = log_queue
        self.__move_count: int = 0

    @override
    def notify(self, *args, **kwargs) -> None:
        self.__move_count += 1
        piece_name = kwargs.get("piece_name", "Pièce")
        color = kwargs.get("color", "?")
        destination = kwargs.get("destination", (?, ?))
        entry = f"Coup #{self.__move_count} [{color}] : {piece_name} -> {destination}"
        self.__log_queue.put(entry)


class MoveLoggerThread(Thread):
    """Consommateur : écrit les coups sur le disque de manière asynchrone."""

    def __init__(
        self, log_queue: Queue[str | None], filepath: str = "partie.pgn"
    ) -> None:
        Thread.__init__(self, name="move-logger-thread")
        self.__log_queue: Queue[str | None] = log_queue
        self.__filepath: str = filepath

    @override
    def run(self) -> None:
        with open(self.__filepath, "w", encoding="utf-8") as file:
            file.write("=== Historique de la partie ===\n")
            while True:
                entry = self.__log_queue.get()
                try:
                    if entry is None:  # Sentinelle d'arrêt propre
                        break
                    sleep(0.05)  # Simulation latence I/O disque
                    file.write(f"{entry}\n")
                    file.flush()
                finally:
                    self.__log_queue.task_done()

```

### 2. Architecture du cycle `think()` / `play_turn()` avec Minimax (`AiVirtualPlayer`)

```
    def __compute_best_move(
        self, snapshot: list[list[Piece | None]]
    ) -> tuple[tuple[int, int], tuple[int, int]] | None:
        best_score: float = float("-inf")
        best_move: tuple[tuple[int, int], tuple[int, int]] | None = None

        for move in self.__get_all_legal_moves(snapshot, self.__color):
            simulated_grid = self.__simulate_move(snapshot, move)
            score = self.__minimax(
                simulated_grid, depth=2, is_maximizing=False
            )
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    @override
    def play_turn(self) -> None:
        # 1. Lecture rapide protégée par le verrou
        with self.__lock:
            if self.__game.status is not Status.PLAYING:
                return
            snapshot = self.__board.get_snapshot()

        # 2. Calcul lourd Minimax HORS du verrou
        chosen_move = self.__compute_best_move(snapshot)
        if chosen_move is None or self.__stop_event.is_set():
            return

        # 3. Application atomique du coup protégée par le verrou
        with self.__lock:
            if self.__game.status is Status.PLAYING:
                origin, destination = chosen_move
                self.__board.move_piece_from_coords(origin, destination)

```

### 3. Extinction propre de tous les threads dans `main.py`

```
    # Arrêt coordonné à la fin de la partie
    if game.status is Status.PLAYING:
        game.to_finished_status()

    ai_player.stop()
    ai_ref.stop()
    chess_clock.stop()

    # Envoi de la sentinelle pour débloquer MoveLoggerThread
    log_queue.put(None)

    ai_player.join()
    ai_ref.join()
    chess_clock.join()
    move_logger.join()
    print("Tous les threads ont été arrêtés proprement.")

```
