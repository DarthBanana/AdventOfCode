import os
import re


def open_file(file):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    absolute_path = absolute_path + '\\'
    file_path = absolute_path + file
    input_file = open(file_path, "r")
    return input_file


class Bot:
    def __init__(self, id, low, high):
        self.id = id
        self.items = []
        self.low = low
        self.high = high


class Factory:
    def __init__(self):
        self.bots = {}
        self.values = []
        self.output_bins = {}

    def process_instruction(self, instruction):
        value_re = re.compile(r"value (\d+) goes to bot (\d+)")
        bot_re = re.compile(
            r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")

        match = value_re.search(instruction)
        if match:
            group = match.groups()
            value_id = int(group[0])
            destination_id = int(group[1])
            self.values.append((value_id, destination_id))
            return

        match = bot_re.search(instruction)
        if match:
            group = match.groups()
            bot_id = int(group[0])
            low_dest_type = group[1]
            low_dest_id = int(group[2])
            high_dest_type = group[3]
            high_dest_id = int(group[4])
            self.bots[bot_id] = Bot(
                bot_id, (low_dest_type, low_dest_id), (high_dest_type, high_dest_id))
            return

    def process_instructions(self, instructions):
        for line in instructions.splitlines():
            self.process_instruction(line)

    def put_chip_in_output(self, bin_id, value):

        current_bin_contents = self.output_bins.get(bin_id)

        if current_bin_contents == None:
            current_bin_contents = []

        current_bin_contents.append(value)
        self.output_bins[bin_id] = current_bin_contents

    def give_chip_to_bot(self, bot_id, item):
        bot = self.bots[bot_id]
        bot.items.append(item)
        if len(bot.items) == 2:
            bot.items.sort()
            bot.items.reverse()
            if bot.items == self.target:
                print("Found Bot  ", bot_id)
            if bot.low[0] == "output":
                self.put_chip_in_output(bot.low[1], bot.items.pop())
            else:
                self.give_chip_to_bot(bot.low[1], bot.items.pop())

            if bot.high[0] == "output":
                self.put_chip_in_output(bot.high[1], bot.items.pop())
            else:
                self.give_chip_to_bot(bot.high[1], bot.items.pop())

    def run(self, low, high):
        self.target = [high, low]

        for value in self.values:
            self.give_chip_to_bot(value[1], value[0])

        return


test_data = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


def test():
    factory = Factory()
    factory.process_instructions(test_data)
    factory.run(2, 5)
    print(factory.bots)
    print(factory.output_bins)
    result = factory.output_bins[0][0] * \
        factory.output_bins[1][0] * factory.output_bins[2][0]
    print(result)


def solve():
    file = open_file("input.txt")
    data = file.read()
    factory = Factory()
    factory.process_instructions(data)
    factory.run(17, 61)
    print(factory.output_bins)
    result = factory.output_bins[0][0] * \
        factory.output_bins[1][0] * factory.output_bins[2][0]
    print(result)


test()

solve()
