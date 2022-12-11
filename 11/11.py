from dataclasses import dataclass


def ints():
    return [int(x) for x in open("input.txt").readlines()]


@dataclass
class Monkey:
    items: list
    operation_addend: int
    operation_multiplier: int
    operation_exponent: int
    test: int
    test_true_target: int
    test_false_target: int
    inspections: int

    @staticmethod
    def from_input(text: str):
        lines = text.split("\n")
        starting_items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
        operation = lines[2].split(": ")[1]
        if "*" in operation:
            if operation.split(" ")[-1] == "old":
                operation_exponent = 2
                operation_mul = 1
            else:
                operation_exponent = 1
                operation_mul = int(operation.split(" ")[-1])
            operation_add = 0
        elif "+" in operation:
            operation_exponent = 1
            operation_mul = 1
            operation_add = int(operation.split(" ")[-1])
        else:
            print("Failed to parse!", operation)
            exit()
        test = int(lines[3].split(" ")[-1])
        if_true = int(lines[4].split(" ")[-1])
        if_false = int(lines[5].split(" ")[-1])
        return Monkey(starting_items, operation_add, operation_mul, operation_exponent, test, if_true, if_false, 0)



def s():
    return [Monkey.from_input(x.strip()) for x in open("input.txt").read().split("\n\n")]


monkeys = s()


print(monkeys)

def sim():
    global monkeys

    for monkey in monkeys:
        for i, item in enumerate(monkey.items):
            item = int(pow(item, monkey.operation_exponent))
            item *= monkey.operation_multiplier
            item += monkey.operation_addend
            item //= 3
            print(item)
            monkey.inspections += 1

            if item % monkey.test == 0:
                print("Throwing to", monkey.test_true_target)
                monkeys[monkey.test_true_target].items.append(item)
            else:
                print("Throwing to", monkey.test_false_target)
                monkeys[monkey.test_false_target].items.append(item)

        monkey.items = []


for i in range(20):
    sim()

monkeys.sort(key=lambda m: m.inspections)

monkey_business = monkeys[-1].inspections * monkeys[-2].inspections
print(monkey_business)