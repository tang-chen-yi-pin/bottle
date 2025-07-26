from enum import Enum, auto
import copy


class Color(Enum):
    CYAN = auto()
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
    def __init__(self, data:list[Color], name: str, size = 4) :
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
                self_available_size = i+1
            else:
                break
        transfer_size = min(self_available_size, other.space())
        other.data = self.data[: transfer_size] + other.data
        self.data = self.data[transfer_size:]

    def __str__(self) -> str:
        return '_'*self.space() + ''.join(str(i.value) for i in self.data)

    


def solve(bottles: list[Bottle], contexts: list[str], searched: set[str]) -> bool:
    status = ''.join(str(b) for b in bottles)
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
            contexts.append(f'{bottles[i].name} -> {bottles[j].name}')
            if solve(bottles, contexts, searched):
                return True
            else:
                bottles[i] = src_bottle
                bottles[j] = dst_bottle
                contexts.pop()
    return False

if __name__ == '__main__':
    bottles : list[Bottle] = [
        Bottle([Color.CYAN, Color.BROWN, Color.GRAY, Color.BLUE], '1,1'),
        Bottle([Color.TEAL, Color.GREEN, Color.BLUE, Color.BLUE], '1,2'),
        Bottle([Color.CHARTREUSE, Color.BROWN, Color.BLUE, Color.YELLOW],'1,3'),
        Bottle([Color.CHARTREUSE, Color.PINK, Color.TEAL, Color.BROWN], '1,4'),
        Bottle([Color.GREEN,Color.GREEN, Color.ORANGE, Color.BROWN], '1,5'),
        
        Bottle([], '2,1',size=2),
        Bottle([], '2,2',size=2),
        Bottle([], '2,3',size=2),
        Bottle([Color.CYAN, Color.GREEN, Color.TEAL, Color.YELLOW], '2,5'),

        Bottle([Color.ORANGE, Color.GRAY, Color.YELLOW, Color.TEAL], '3,1'),
        Bottle([Color.PINK, Color.CYAN,Color.CHARTREUSE, Color.GRAY], '3,2'),
        Bottle([Color.YELLOW, Color.ORANGE, Color.ORANGE, Color.GRAY], '3,3'),
        Bottle([Color.PINK, Color.CYAN, Color.GREEN, Color.PINK], '3,4')
    ]
    print(solve(bottles, [], set()))