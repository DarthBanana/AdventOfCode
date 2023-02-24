## advent of code 2018
## https://adventofcode.com/2018
## day 24

import re


army_re = re.compile(r'(\d+) units each with (\d+) hit points with an attack that does (\d+) (\w+) damage at initiative (\d+)')
army_weakness_re = re.compile(r' \(.*\)')
immune_re = re.compile(r'immune to ([\w, ]+)')
weak_re = re.compile(r'weak to ([\w, ]+)')

class Group:
    def __init__(self, line, type, id, boost=0):
        self.id = id
        self.boost = boost
        #print(line)
        self.type = type
        weaknesses = army_weakness_re.search(line)
        new_line = army_weakness_re.sub('', line)
        #print(new_line)
        
        m = army_re.match(new_line)
        assert(m)
        self.units = int(m.group(1))
        self.hp = int(m.group(2))
        self.attack = int(m.group(3)) + boost
        self.attack_type = m.group(4)
        self.initiative = int(m.group(5))
        self.weak = []
        self.immune = []
        if weaknesses:
            m2 = immune_re.search(weaknesses.group(0))
            if m2:                
                self.immune = m2.group(1).split(', ')
            m2 = weak_re.search(weaknesses.group(0))
            if m2:                
                self.weak = m2.group(1).split(', ')
        #print(self)
        
        
    def effective_power(self):
        return self.units * self.attack

    def damage(self, other):
        if self.attack_type in other.immune:
            return 0
        elif self.attack_type in other.weak:
            return self.effective_power() * 2
        else:
            return self.effective_power()

    def __repr__(self):
        return f'{self.type} group {self.id} - {self.units} units with {self.hp} hp each, {self.attack} {self.attack_type} damage at initiative {self.initiative}, weakensses: {self.weak}, immunities: {self.immune}'

class Puzzle:
    def __init__(self, lines):
        self.lines = lines
        self.reset()

    def reset(self, boost=0):

        self.groups = []
        type = "none"
        id = 1
        for line in self.lines:        

            if line.startswith('Immune System'):
                type = "immune"
                id = 1
                applied_boost = boost
            elif line.startswith('Infection'):
                type = "infection"
                id = 1
                applied_boost = 0
            elif line:
                self.groups.append(Group(line, type, id, applied_boost))   
                id += 1        

    def attack(self, attacker, defender):
        #print("Attacking: ", attacker)
        #print("Defending: ", defender)
        
        damage = attacker.damage(defender)        
        units_lost = damage // defender.hp
        if units_lost > defender.units:
            units_lost = defender.units
        #print(attacker.type, attacker.id, defender.type, defender.id, "Units lost: ", units_lost, damage)
        defender.units -= units_lost
        return units_lost    

    def target_selection(self):
        #print("Target selection")
        self.groups.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)        

        targets = {}
        for attacker in self.groups:

            if attacker.units <= 0:
                continue

            best_damage = 0
            best_defenders = []
            for defender in self.groups:
                if defender.type == attacker.type or defender in targets.values() or defender.units <= 0:
                    continue
                damage = attacker.damage(defender)
                #print(attacker, defender, damage)
                if damage > best_damage:
                    best_damage = damage
                    best_defenders = [defender]
                elif damage == best_damage:
                    best_defenders.append(defender)
            best_defenders.sort(key=lambda x: (x.effective_power(), x.initiative), reverse=True)
            if best_damage > 0:
                targets[attacker] = best_defenders[0]
        return targets

    def units(self, type):
        return sum([x.units for x in self.groups if x.type == type and x.units > 0])

    def round(self):
        targets = self.target_selection()
        self.groups.sort(key=lambda x: x.initiative, reverse=True)
        for attacker in self.groups:
            if attacker.units <= 0:
                continue
            if attacker in targets:
                self.attack(attacker, targets[attacker])

    def battle(self):
        round = 1
        
        while True:
            starting_immune_units = self.units("immune")
            starting_infection_units = self.units("infection")            
            print("Round: ", round, " Immune System:", self.units("immune"), " Infection:", self.units("infection"))
            
            self.round()
            print("Round: ", round, " Immune System:", self.units("immune"), " Infection:", self.units("infection"))
            round += 1
            if self.units("immune") == starting_immune_units and self.units("infection") == starting_infection_units:
                print("Stalemate")
                return False
            if self.units("immune") == 0:
                print("Infection wins")
                return False
            if self.units("infection") == 0:
                print("Immune System wins")
                return True
                    


    def part1(self):
        
        # NOT 16746!!
        self.battle()
        return sum([x.units for x in self.groups if x.units > 0])
        

    def part2(self):
        
        boost = 0
        increment = 1024
        while True:
            print("Boost: ", boost, "Increment: ", increment)
            self.reset(boost)
            if self.battle():
                if increment == 1:
                    return sum([x.units for x in self.groups if x.units > 0])
                boost -= increment
                increment = increment // 2
            boost += increment
            
        