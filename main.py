from game_24 import SearchTree

def run_game_24() -> None:
    while True:
        operands_raw: str = input("\nEnter the 4 numbers separated by a space (or \"quit\"): ")
        if operands_raw == "quit":
            print("Thank you for playing with this program. Have a nice day!")
            break
        operands: list[int] = [int(operand_raw) for operand_raw in operands_raw.split(" ")]
        try:
            solution: str = SearchTree(operands, enable_logging = True).search()
            print(f"A solution was found: {solution}")
        except RuntimeError:
            print(f"No solution was found!")

if __name__ == "__main__":
    run_game_24()