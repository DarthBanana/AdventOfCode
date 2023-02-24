## advent of code 2018
## https://adventofcode.com/2018
## day 12
class Puzzle:
    def __init__(self, lines):
        self.plants = set()
        
        self.rules = {}
        for line in lines:            
            if line.find("initial state") > -1:
                split = line.split(": ")  
                self.plants = self.get_plants_from_string(split[1], 0)
            elif line.find("=>") > -1:
                print(line)
                split = line.split(" => ")
                self.rules[split[0]] = split[1]    

    def get_plants_from_string(self, string, min_index):
        i = min_index
        plants = set()
        for c in string:
            if c == "#":
                plants.add(i)
            i += 1
        return plants

    def get_pattern(self, plants, index):
        pattern = ""
        for i in range(index-2, index + 3):            
            if i in plants:
                pattern += "#"
            else:
                pattern += "."            
        return pattern

    def get_plant_string(self, plants):
        min_plant = min(plants)
        max_plant = max(plants)
        string=""
        for i in range(min_plant, max_plant+1):
            if i in plants:
                string += "#"
            else:
                string += "."
        return string.strip(".")

    def is_plant(self, plants, index):
        pattern = self.get_pattern(plants, index)
        
        replacement = self.rules.get(pattern, ".")        
        return replacement == "#"
    
    def run_iteration(self, plants):          
        new_plants = set()
        min_plant = min(plants)
        max_plant = max(plants) 
        for i in range(min_plant - 2, max_plant + 3):
            if self.is_plant(plants, i):
                new_plants.add(i)            
        return new_plants

    def run_iterations(self, count):
        history = {}

        plants = self.plants.copy()
        iteration = 0
        while iteration < count:
            string = self.get_plant_string(plants)
            print(iteration, string)
            if string in history:
                print("FOUND A CYCLE")

                # Found a cycle
                current_min = min(plants)
                last_iteration, last_min_index = history[string]
                print(iteration, current_min, last_iteration, last_min_index)
                # How big is the cycle?
                cycle_len = iteration - last_iteration
                # How much does the pattern shift per cycle?
                step_size = current_min - last_min_index

                # How many more iterations do we have
                count_left = count - iteration

                #advance N cycles
                cycles_left = count_left // cycle_len
                shift_amount = cycles_left * step_size
                new_min = min(plants) + shift_amount

                # Now account for the remainder                
                remainder = count_left % cycle_len
                # the answer must already be in history
                answer_iteration = last_iteration + remainder
                for key, (iter, mi) in history.items():
                    if iter == answer_iteration:
                        shift_amount = mi - last_min_index
                        new_min += shift_amount
                        return self.get_plants_from_string(key, new_min)
            history[string] = (iteration, min(plants))            
            #print(iteration,self.get_plant_string(plants))
            plants = self.run_iteration(plants)
            iteration += 1
        print(iteration,self.get_plant_string(plants))
        
        return plants


    def part1(self):
        plants = self.run_iterations(20)
        return sum(plants)

    def part2(self):
        plants = self.run_iterations(50000000000)
        return sum(plants)