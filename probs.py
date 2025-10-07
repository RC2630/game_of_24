from dataclasses import dataclass
from typing import Generator, Any
from game_24 import SearchTree
import pandas as pd

@dataclass
class Card:
    value: int
    suit: str

# ------------------------------------------------------------------------------------

@dataclass
class Stats:

    total_hands: int
    solvable_hands: int
    total_unique_hands: int
    solvable_unique_hands: int

    def get_probability_solvable_hand(self) -> float:
        return self.solvable_hands / self.total_hands
    
    def get_probability_solvable_unique_hand(self) -> float:
        return self.solvable_unique_hands / self.total_unique_hands
    
# ------------------------------------------------------------------------------------

@dataclass
class UniqueHandInfo:

    solvable: bool
    solution: str
    corresponding_combinations: int
    corresponding_permutations: int

    def indicator_solvable(self) -> int:
        return int(self.solvable)
    
# ------------------------------------------------------------------------------------

def generate_full_deck() -> list[Card]:
    return [Card(value, suit) for value in range(1, 14) for suit in (
        "diamond", "heart", "spade", "club"
    )]

def get_all_hands(deck: list[Card], hand_size: int) -> list[tuple[Card, ...]]:
    if hand_size == 0:
        return [()]
    results: list[tuple[Card, ...]] = []
    for i in range(len(deck)):
        for subhand in get_all_hands(deck[i+1:], hand_size - 1):
            results.append((deck[i],) + subhand)
    return results

# ------------------------------------------------------------------------------------

def generate_stats() -> tuple[Stats, dict[tuple[int, ...], UniqueHandInfo]]:

    deck: list[Card] = generate_full_deck()
    unique_hands: dict[tuple[int, ...], UniqueHandInfo] = {}

    num_hands: int = 0
    num_unique_hands: int = 0
    num_solvable_hands: int = 0
    num_solvable_unique_hands: int = 0

    for hand in get_all_hands(deck, 4):

        hand_values: list[int] = [card.value for card in hand]
        sorted_hand: tuple[int, ...] = tuple(sorted(hand_values))
        num_hands += 1

        if num_hands % 1000 == 0:
            print(f"Currently processing hand {num_hands}")

        if sorted_hand not in unique_hands:
            num_unique_hands += 1
            try:
                solution: str = SearchTree(list(sorted_hand)).search()
                unique_hands[sorted_hand] = UniqueHandInfo(True, solution, 1, 24)
                num_solvable_unique_hands += 1
                num_solvable_hands += 1
            except RuntimeError:
                unique_hands[sorted_hand] = UniqueHandInfo(False, "", 1, 24)

        else:
            num_solvable_hands += unique_hands[sorted_hand].indicator_solvable()
            unique_hands[sorted_hand].corresponding_combinations += 1
            unique_hands[sorted_hand].corresponding_permutations += 24
        
    stats: Stats = Stats(num_hands, num_solvable_hands, num_unique_hands, num_solvable_unique_hands)
    return (stats, unique_hands)

# ------------------------------------------------------------------------------------

def make_data_frame(data: dict[tuple[int, ...], UniqueHandInfo]) -> None:
    unique_hands: list[tuple[int, ...]] = list(data.keys())
    infos: list[UniqueHandInfo] = list(data.values())
    df: pd.DataFrame = pd.DataFrame(dict(
        unique_hand = unique_hands,
        solvable = [info.solvable for info in infos],
        solution = [info.solution for info in infos],
        num_combs = [info.corresponding_combinations for info in infos],
        num_perms = [info.corresponding_permutations for info in infos]
    ))
    df.to_csv("data/data.csv", index = False)

def run_find_probs() -> None:
    stats, data = generate_stats()
    make_data_frame(data)
    print(
        f"\nTotal # of hands: {stats.total_hands}"
        f"\n# of solvable hands: {stats.solvable_hands}"
        f"\nProbability of a solvable hand: {stats.get_probability_solvable_hand()}"
        f"\nTotal # of unique hands: {stats.total_unique_hands}"
        f"\n# of solvable unique hands: {stats.solvable_unique_hands}"
        f"\nProbability of a solvable unique hand: {stats.get_probability_solvable_unique_hand()}"
    )

if __name__ == "__main__":
    run_find_probs()