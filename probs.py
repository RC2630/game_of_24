from dataclasses import dataclass
from typing import Generator, Any
from game_24 import SearchTree

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

def generate_full_deck() -> list[Card]:
    return [Card(value, suit) for value in range(1, 14) for suit in (
        "diamond", "heart", "spade", "club"
    )]

def get_and_remove(l: list[Any], i: int) -> tuple[list[Any], Any]:
    copy_l: list[Any] = l.copy()
    item: Any = copy_l[i]
    del copy_l[i]
    return (copy_l, item)

# ------------------------------------------------------------------------------------

def get_all_hands(deck: list[Card], hand_size: int) -> list[tuple[Card, ...]]:

    if hand_size == 0:
        return [()]

    results: list[tuple[Card, ...]] = []
    for i in range(len(deck)):
        remaining_cards, selected_card = get_and_remove(deck, i)
        for subhand in get_all_hands(remaining_cards, hand_size - 1):
            results.append((selected_card,) + subhand)

    return results

# ------------------------------------------------------------------------------------

def generate_stats() -> Stats:

    deck: list[Card] = generate_full_deck()
    unique_hands: dict[tuple[int, ...], bool] = {}

    num_hands: int = 0
    num_unique_hands: int = 0
    num_solvable_hands: int = 0
    num_solvable_unique_hands: int = 0

    for hand in get_all_hands(deck, 4):

        hand_values: list[int] = [card.value for card in hand]
        sorted_hand: tuple[int, ...] = tuple(sorted(hand_values))
        num_hands += 1
        print(f"Currently processing hand {num_hands}")

        if sorted_hand not in unique_hands:
            num_unique_hands += 1
            try:
                SearchTree(list(sorted_hand)).search()
                unique_hands[sorted_hand] = True
                num_solvable_unique_hands += 1
                num_solvable_hands += 1
            except RuntimeError:
                unique_hands[sorted_hand] = False

        else:
            num_solvable_hands += int(unique_hands[sorted_hand])
        
    return Stats(num_hands, num_solvable_hands, num_unique_hands, num_solvable_unique_hands)

# ------------------------------------------------------------------------------------

def run_find_probs() -> None:
    stats: Stats = generate_stats()
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