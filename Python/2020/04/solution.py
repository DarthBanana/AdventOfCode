## advent of code 2020
## https://adventofcode.com/2020
## day 04

import re
from aocpuzzle import *
REQUIRED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
height_re = re.compile(r'^(\d+)(cm|in)$')
hcl_re = re.compile(r'^#[0-9a-f]{6}$')
ecl_re = re.compile(r'^amb|blu|brn|gry|grn|hzl|oth$')
pid_re = re.compile(r'^\d{9}$')
byr_re = re.compile(r'^\d{4}$')
iyr_re = re.compile(r'^\d{4}$')
eyr_re = re.compile(r'^\d{4}$')
class Passport():
    def __init__(self, lines):
        self.data = {}
        while len(lines) > 0:
            line  = lines.pop(0)            
            
            if line == '':
                break
            for field in line.split(' '):
                key, value = field.split(':')
                self.data[key] = value

    def is_field_valid(self, field):        
        if field not in self.data:            
            return False, "not found"
        value = self.data[field]
        if field == 'byr':
            if not byr_re.match(value):                
                return False, f'byr {value} is not a valid year'
            if int(value) < 1920 or int(value) > 2002:                
                return False, f'byr {value} is not between 1920 and 2002'
        elif field == 'iyr':    
            if not iyr_re.match(value):                
                return False, f'iyr {value} is not a valid year'
            if int(value) < 2010 or int(value) > 2020:                
                return False, f'iyr {value} is not between 2010 and 2020'
        elif field == 'eyr':
            if not eyr_re.match(value):                
                return False, f'eyr {value} is not a valid year'
            if int(value) < 2020 or int(value) > 2030:                
                return False, f'eyr {value} is not between 2020 and 2030'
        elif field == 'hgt':
            m = height_re.match(value)
            if m is None:                
                return False, f'hgt {value} is not a valid height'
            height = int(m.group(1))
            unit = m.group(2)
            if unit == 'cm':
                if height < 150 or height > 193:                    
                    return False, f'hgt {value} is not between 150cm and 193cm'
            elif unit == 'in':
                if height < 59 or height > 76:                    
                    return False, f'hgt {value} is not between 59in and 76in'
            else:
                return False
        elif field == 'hcl':
            if not hcl_re.match(value):                
                return False, f'hcl {value} is not a valid hair color'
        elif field == 'ecl':
            if not ecl_re.match(value):                
                return False, f'ecl {value} is not a valid eye color'
        elif field == 'pid':
            if not pid_re.match(value):                
                return False, f'pid {value} is not a valid passport id'
            
        #print(f'{field} {value} is valid')
        return True, ""


    def is_valid(self):
        for field in REQUIRED_FIELDS:
            if field not in self.data:
                return False                    
        return True
    
    def are_fields_valid(self):
        for field in REQUIRED_FIELDS:
            v, reason = self.is_field_valid(field)
            if not v:
                return False        
        return True
    
    def __str__(self):
        string = ""
        keys = list(self.data.keys())
        keys.sort()
        if "pid" in keys:
            keys.remove("pid")
            v, reason = self.is_field_valid("pid")
            if v:
                string += "pid: " + self.data["pid"] + " (valid)\n"
            else:
                string += "pid: " + self.data["pid"] + " (invalid): " + reason + "\n"            
            
        else:            
            string += "pid: not found (invalid)\n"            

        for key in keys:
            v, reason = self.is_field_valid(key)
            if v:
                string += "\t" + str(key) + ": " + self.data[key] + " (valid)\n"
                
            else:
                string += "\t" + str(key) + ": " + self.data[key] + " (invalid): " + reason + "\n"
        
        for k in REQUIRED_FIELDS:
            if k not in self.data:
                string += "\t" + str(k) + ": not found (invalid)\n"

        return string                
            

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        self.passports = []
        AoCPuzzle.__init__(self, lines, is_test)
        while len(lines) > 0:
            self.passports.append(Passport(lines))

    def part1(self):
        valid = 0
        for p in self.passports:
            if p.is_valid():
                valid += 1
        return valid

    def part2(self):
        valid = 0
        to_test = []
        
        for p in self.passports:
            if p.is_valid():
                to_test.append(p)
        for p in to_test:
            if p.are_fields_valid():            
                valid += 1
                
        return valid