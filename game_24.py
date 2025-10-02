from __future__ import annotations
from typing import Callable
from rational import RationalNumber
from collections import deque

OPERATORS: dict[str, Callable[[RationalNumber, RationalNumber], RationalNumber]] = {
    "+": RationalNumber.__add__,
    "-": RationalNumber.__sub__,
    "*": RationalNumber.__mul__,
    "/": RationalNumber.__truediv__    
}

LOG_FILE: str = "log/log.txt"

# ------------------------------------------------------------------------------------

def write_to_log_file(line: str) -> None:
    with open(LOG_FILE, "a") as file:
        file.write(f"{line}\n")

def get_index_pairs(n: int) -> list[tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(n) if i != j]

# ------------------------------------------------------------------------------------

class Operand:

    def __init__(self, number: RationalNumber, original_expr: str) -> None:
        self.number: RationalNumber = number
        self.original_expr: str = original_expr

    def get_trimmed_expr(self) -> str:
        if self.original_expr.startswith("("):
            return self.original_expr[1:-1]
        else:
            return self.original_expr

# ------------------------------------------------------------------------------------

class Node:

    def __init__(self, operands: list[Operand]) -> None:
        self.operands: list[Operand] = operands

    def is_leaf(self) -> bool:
        return len(self.operands) == 1
    
    def is_24(self) -> bool:
        return self.is_leaf() and self.operands[0].number == RationalNumber(24)
    
    def create_child_nodes(self) -> list[Node]:

        assert not self.is_leaf()
        children: list[Node] = []
        index_pairs: list[tuple[int, int]] = get_index_pairs(len(self.operands))

        for index1, index2 in index_pairs:
            for operator, operation in OPERATORS.items():

                operand1: Operand = self.operands[index1]
                operand2: Operand = self.operands[index2]

                try:
                    operation_result: RationalNumber = operation(operand1.number, operand2.number)
                except ZeroDivisionError:
                    continue

                new_operands: list[Operand] = [Operand(
                    operation_result,
                    f"({operand1.original_expr} {operator} {operand2.original_expr})"
                )]

                for i in range(len(self.operands)):
                    if i not in (index1, index2):
                        new_operands.append(self.operands[i])
                
                children.append(Node(new_operands))

        return children

# ------------------------------------------------------------------------------------

class SearchTree:

    def __init__(self, initial_operands: list[int], enable_logging: bool = False) -> None:
        self.frontier: deque[Node] = deque([Node(
            [Operand(
                RationalNumber(initial_operand),
                str(initial_operand)
            ) for initial_operand in initial_operands]
        )])
        self.log: bool = enable_logging
        if self.log:
            with open(LOG_FILE, "w") as file:
                file.write("")

    def search(self) -> str:
        while len(self.frontier) != 0:
            curr_node: Node = self.frontier.popleft()
            if self.log:
                write_to_log_file(", ".join([
                    f"[{operand.get_trimmed_expr()}]" for operand in curr_node.operands
                ]))
            if curr_node.is_24():
                return curr_node.operands[0].get_trimmed_expr()
            elif not curr_node.is_leaf():
                self.frontier += curr_node.create_child_nodes()
        raise RuntimeError("no solution found")