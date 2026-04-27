def divide(left: int, right: int) -> float:
    if right == 0:
        raise ZeroDivisionError("right must not be zero")
    return left / right
