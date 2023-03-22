## advent of code 2019
## https://adventofcode.com/2019
## day 22

from aocpuzzle import *
from parsehelp import get_all_ints
DECK_SIZE = 10007
DECK_SIZE2 = 119315717514047
SHUFFLES = 101741582076661

def cheat(instructions):
    n = 119315717514047
    c = 2020

    a, b = 1, 0
    for instruction in instructions:
        if instruction[0] == "d":
            if instruction[1] == None:
                la, lb = -1, -1
            else:
                la, lb = instruction[1], 0
        elif instruction[0] == "c":
             la, lb = 1, -instruction[1]
        else:
            assert(False)
        
        # la * (a * x + b) + lb == la * a * x + la*b + lb
        # The `% n` doesn't change the result, but keeps the numbers small.
        a = (la * a) % n
        b = (la * b + lb) % n

    print("cheat a,b: ", a, b)
    M = 101741582076661
    # Now want to morally run:
    # la, lb = a, b
    # a = 1, b = 0
    # for i in range(M):
    #     a, b = (a * la) % n, (la * b + lb) % n

    # For a, this is same as computing (a ** M) % n, which is in the computable
    # realm with fast exponentiation.
    # For b, this is same as computing ... + a**2 * b + a*b + b
    # == b * (a**(M-1) + a**(M) + ... + a + 1) == b * (a**M - 1)/(a-1)
    # That's again computable, but we need the inverse of a-1 mod n.

    # Fermat's little theorem gives a simple inv:
    def inv(a, n): return pow(a, n-2, n)

    Ma = pow(a, M, n)
    Mb = (b * (Ma - 1) * inv(a-1, n)) % n
    
    print("Cheat Ma, Mb : ",Ma,Mb)
    # This computes "where does 2020 end up", but I want "what is at 2020".
    #print((Ma * c + Mb) % n)

    # So need to invert (2020 - MB) * inv(Ma)
    val = ((c - Mb) * inv(Ma, n)) % n
    return val

class Puzzle(AoCPuzzle):
    def __init__(self, lines, is_test=False):
        AoCPuzzle.__init__(self, lines, is_test)
        
        if is_test:
            self.deck_size = 10
        else:
            self.deck_size = DECK_SIZE

        self.instructions = []
        for line in lines:
            d = line[0]
            v = get_all_ints(line)
            if len(v):
                v = v[0]
            else:
                v = None
            self.instructions.append((d, v))

        self.deck = [i for i in range(self.deck_size)]
        
    
    def deal_into_new_stack(self):
        self.deck.reverse()

    def cut(self, n):
        self.deck = self.deck[n:] + self.deck[:n]

    def deal_with_increment(self, n):
        new_deck = [None] * self.deck_size
        for i in range(self.deck_size):            
            new_deck[(i * n) % self.deck_size] = self.deck[i]
        self.deck = new_deck

    def execute_instructions(self):
        for (i, v) in self.instructions:            
            if i == "d":
                if v == None:
                    self.deal_into_new_stack()
                else:
                    self.deal_with_increment(v)
            elif i == "c":
                self.cut(v)
            else:
                assert(False)


    def part1(self):
        self.execute_instructions()
        if self.is_test:
            output = ""
            for c in self.deck:
                output += str(c) + " "
            output.strip()
            return output.strip()
        else:
            return self.deck.index(2019)

    def get_a_and_b_prime(self, instruction):
        if instruction[0] == "d":
            if instruction[1] == None:
                return (-1, -1)
            else:
                return (instruction[1], 0)
        elif instruction[0] == "c":
            return (1, -instruction[1])
        else:
            assert(False)

    def compute_a_and_b_for_one_pass(self):
        # Hard stuff, lets figure this out
        # The question asks for what card ends up at position 2020
        # So we need to work backwards through the instructions and undo them
        # each instruction is a simple function for Ax + B mod L
        # deal into new stack:
        #   A = -1, B = 0
        # cut:
        #   A = 1, B = -n
        # deal with increment:
        #   A = n, B = 0
        # 
        # To compose two instructions:
        #   A'(Ax + B) + B'
        # or 
        #   A'Ax + A'B + B'
        # or:
        #   A''x + B''
        # A'' = A'A
        # B'' = A'B + B'
        # A and B can be modded to keep stuff small?        
        a = 1
        b = 0
        for i in self.instructions:
            (ap, bp) = self.get_a_and_b_prime(i)
            a = (a * ap) % self.deck_size
            b = (ap * b + bp) % self.deck_size
        return (a, b)
    


    def compute_a_and_b_for_n(self, a, b, n):
        # Ok, so this is just applying the same function over again
        # (ax+b)^m % n
        # A' = A*A
        # B' = AB + B
        #  x' = A^n * x + B * (A^n - 1) / (A - 1)
        

        Ma = pow(a, n, self.deck_size)
        Mb = (b * (Ma - 1) * inv(a-1, self.deck_size)) % self.deck_size        
        return (Ma, Mb)
    
    def part2(self):
        # NOT 58230119277487
        # NOT 78349116882913
        # NOT 42388840936310
        # NOT 26523858479940
        # NOT 17309137410242
        # YES 79608410258462

        self.deck_size = DECK_SIZE2
        (a, b) = self.compute_a_and_b_for_one_pass()
        print("a,b: ", a, b)
        (Ma, Mb) = self.compute_a_and_b_for_n(a, b, SHUFFLES)
        print("Ma, Mb : ",Ma,Mb)

        x = (Ma*2020 + Mb) % self.deck_size
        y = ((2020 - Mb) * inv(Ma, self.deck_size)) % self.deck_size
        print(x,y)
        ans = cheat(self.instructions)
        print("Cheat: ", ans)
        return y
    
def inv(a, n): 
    return pow(a, n-2, n)