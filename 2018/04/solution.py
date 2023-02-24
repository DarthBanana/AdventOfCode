## advent of code 2018
## https://adventofcode.com/2018
## day 04
from datetime import datetime
from enum import Enum
import re


date_re = re.compile(r"\[(.*)\]")
sleep_re = re.compile(r"falls asleep")
wake_re = re.compile(r"wakes up")
begin_re = re.compile(r"Guard #(\d+) begins shift")

class EventType(Enum):
    WAKE = 1
    SLEEP = 2
    BEGIN_SHIFT = 3


class Record:
    def __init__(self, line):
        date_string = date_re.search(line).group(1)
        self.date = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        self.guard = -1
        if sleep_re.search(line):
            self.type = EventType.SLEEP
        elif wake_re.search(line):
            self.type = EventType.WAKE
        else:
            self.guard = int(begin_re.search(line).group(1))
            self.type = EventType.BEGIN_SHIFT    


class Puzzle:
    def __init__(self, lines):
        self.records = []
        for line in lines:
            self.records.append(Record(line))
        self.records.sort(key=lambda x:x.date)
        last_guard = -1
        for record in self.records:
            if record.type == EventType.BEGIN_SHIFT:
                last_guard = record.guard
            else:
                record.guard = last_guard
        self.guards = {}    

    def unpack_minutes_asleep(self):
        for record in self.records:
            if record.type == EventType.SLEEP:
                fell_asleep = record.date.minute
            elif record.type == EventType.WAKE:
                guard_minutes = self.guards.get(record.guard, {})
                time = record.date.minute - fell_asleep                
                for t in range(fell_asleep, record.date.minute):
                    guard_minutes[t] = guard_minutes.get(t, 0) + 1
                self.guards[record.guard] = guard_minutes

    def part1(self):
        self.unpack_minutes_asleep()
        
        max_guard = -1
        max_minute_count = -1
        for guard, guard_minutes in self.guards.items():
            count = sum(guard_minutes.values())
            if count > max_minute_count:
                max_guard = guard
                max_minute_count = count
        print(max_guard)
                        
        max_minutes = self.guards[max_guard]
        max_minute_count = max(max_minutes.values())
        for minute,count in filter(lambda m:m[1] == max_minute_count, max_minutes.items()):
            max_minute = minute

        return max_minute * max_guard

    def part2(self):

        max_minute_count = -1
        max_minute_guard = -1
        max_minute = -1
        for guard,guard_minutes in self.guards.items():
            max_min = max(guard_minutes.values())
            if max_min > max_minute_count:
                max_minute_guard = guard
                max_minute_count = max_min
                max_minute = {i for i in guard_minutes if guard_minutes[i]==max_minute_count}.pop()
        return max_minute * max_minute_guard

        

        
        
def parse_input(lines):
    return Puzzle(lines)

def part1(puzzle):
    return puzzle.part1()
    

def part2(puzzle):
    return puzzle.part2()