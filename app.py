from enum import Enum, auto
import copy


class Color(Enum):
    CYAN = 0
    BROWN = auto()
    GRAY = auto()
    BLUE = auto()
    TEAL = auto()
    GREEN = auto()
    CHARTREUSE = auto()
    YELLOW = auto()
    PINK = auto()
    ORANGE = auto()
    RED = auto()


class Bottle:
    def __init__(self, data: list[Color], name: str, size=4):
        self.data = data
        self.size = size
        self.name = name

    def is_empty(self) -> bool:
        return len(self.data) == 0

    def is_full(self) -> bool:
        return len(self.data) == self.size

    def is_lock(self) -> bool:
        return self.is_full() and len(set(self.data)) == 1

    def space(self) -> int:
        return self.size - len(self.data)

    def top(self) -> Color:
        assert not self.is_empty()
        return self.data[0]

    def can_transfer_to(self, other: "Bottle") -> bool:
        if self.is_empty() or self.is_lock() or other.is_full():
            return False
        return other.is_empty() or self.top() == other.top()

    def transfer_to(self, other: "Bottle"):
        assert self.can_transfer_to(other)

        self_available_size = 0
        for i in range(len(self.data)):
            if self.data[i] == self.data[0]:
                self_available_size = i + 1
            else:
                break
        transfer_size = min(self_available_size, other.space())
        other.data = self.data[:transfer_size] + other.data
        self.data = self.data[transfer_size:]

    def __str__(self) -> str:
        return "_" * self.space() + "".join(str(i.value) for i in self.data)


class BottlePrinter:

    class AnsiColors:
        RESET = "\033[0m"
        # 前景色 (字体颜色) - 这里我们主要用背景色
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"

        # 256色背景 (推荐用于更多颜色选择)
        @staticmethod
        def bg_256color(code):
            return f"\033[48;5;{code}m"

    COLOR_MAP = {
        Color.CYAN: AnsiColors.bg_256color(51),  # 偏亮的青色
        Color.BROWN: AnsiColors.bg_256color(94),  # 棕色
        Color.GRAY: AnsiColors.bg_256color(242),  # 灰色 (浅灰)
        Color.BLUE: AnsiColors.bg_256color(21),  # 蓝色
        Color.TEAL: AnsiColors.bg_256color(30),  # 青绿色
        Color.GREEN: AnsiColors.bg_256color(28),  # 绿色
        Color.CHARTREUSE: AnsiColors.bg_256color(118),  # 黄绿色
        Color.YELLOW: AnsiColors.bg_256color(226),  # 黄色
        Color.PINK: AnsiColors.bg_256color(205),  # 粉色
        Color.ORANGE: AnsiColors.bg_256color(208),  # 橙色
        Color.RED: AnsiColors.bg_256color(196),  # 红色
    }
    CHAR_TO_COLOR_MAP = {}
    for i, color_enum in enumerate(Color):
        if str(i) in "0123456789":  # 确保只映射数字字符
            CHAR_TO_COLOR_MAP[str(i)] = COLOR_MAP.get(color_enum)

    CHAR_TO_COLOR_MAP["_"] = AnsiColors.bg_256color(256)  # 下划线用深黑色
    CHAR_TO_COLOR_MAP[" "] = AnsiColors.RESET + " "  # 空格保持透明

    @classmethod
    def print(cls, bottle: Bottle):
        output_parts = []
        for char in str(bottle).strip():
            color_code = BottlePrinter.CHAR_TO_COLOR_MAP.get(char)
            if color_code:
                if char != " ":
                    output_parts.append(
                        f"{color_code} {BottlePrinter.AnsiColors.RESET}"
                    )
                else:
                    output_parts.append(color_code)
            else:
                output_parts.append(char)
        print("".join(output_parts))


def solve(
    bottles: list[Bottle],
    contexts: list[str],
    searched: set[str],
    debug_mode: bool = False,
) -> bool:
    status = " ".join(sorted([str(b) for b in bottles]))

    if debug_mode:
        print("-" * 50)
        for c in contexts:
            print(c)
        print(f"bottles: {[str(b) for b in bottles]}")
        for b in bottles:
            BottlePrinter.print(b)

    if status in searched:
        return False
    searched.add(status)

    if all(i.is_empty() or i.is_lock() for i in bottles):
        for context in contexts:
            print(context)
        return True
    for i in range(len(bottles)):
        for j in range(len(bottles)):
            if i == j:
                continue
            if not bottles[i].can_transfer_to(bottles[j]):
                continue
            src_bottle = copy.deepcopy(bottles[i])
            dst_bottle = copy.deepcopy(bottles[j])
            bottles[i].transfer_to(bottles[j])
            contexts.append(f"{bottles[i].name} -> {bottles[j].name}")
            if solve(bottles, contexts, searched, debug_mode=debug_mode):
                return True
            else:
                bottles[i] = src_bottle
                bottles[j] = dst_bottle
                contexts.pop()
    return False


if __name__ == "__main__":
    bottles: list[Bottle] = [
        Bottle([Color.CYAN, Color.BROWN, Color.GRAY, Color.BLUE], "1,1"),
        Bottle([Color.TEAL, Color.GREEN, Color.BLUE, Color.BLUE], "1,2"),
        Bottle([Color.CHARTREUSE, Color.BROWN, Color.BLUE, Color.YELLOW], "1,3"),
        Bottle([Color.CHARTREUSE, Color.PINK, Color.TEAL, Color.BROWN], "1,4"),
        Bottle([Color.GREEN, Color.GREEN, Color.ORANGE, Color.BROWN], "1,5"),
        Bottle([], "2,1", size=2),
        Bottle([], "2,2", size=2),
        Bottle([], "2,3", size=2),
        Bottle([Color.CYAN, Color.GREEN, Color.TEAL, Color.YELLOW], "2,5"),
        Bottle([Color.ORANGE, Color.GRAY, Color.YELLOW, Color.TEAL], "3,1"),
        Bottle([Color.PINK, Color.CYAN, Color.CHARTREUSE, Color.GRAY], "3,2"),
        Bottle([Color.YELLOW, Color.ORANGE, Color.ORANGE, Color.GRAY], "3,3"),
        Bottle([Color.PINK, Color.CYAN, Color.GREEN, Color.PINK], "3,4"),
    ]
    print(solve(bottles, [], set(), debug_mode=True))
