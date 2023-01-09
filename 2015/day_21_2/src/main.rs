use std::cmp::max;

const WEAPONS: &str = "Dagger      8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0";
const ARMOR: &str = "None        0      0       0
Leather     13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5";
const RINGS: &str = "none_1     0      0       0
none_2      0      0       0
Damage_1    25     1       0
Damage_2    50     2       0
Damage_3   100     3       0
Defense_1   20     0       1
Defense_2   40     0       2
Defense_3   80     0       3";

struct Character {
    hit_points: i32,
    damage: u32,
    armor: u32,
}

struct Item {
    name: String,
    cost: u32,
    damage_modifier: u32,
    armor_modifier: u32,
}

impl Item {
    fn new(name: &str, cost: u32, damage: u32, armor: u32) -> Self {
        Self {
            name: name.to_string(),
            cost,
            damage_modifier: damage,
            armor_modifier: armor,
        }
    }
    fn new_from_string(item_string: &str) -> Self {
        let mut things = item_string.split_ascii_whitespace();
        let name = things.next().unwrap();
        let cost: u32 = things.next().unwrap().parse().unwrap();
        let damage: u32 = things.next().unwrap().parse().unwrap();
        let armor: u32 = things.next().unwrap().parse().unwrap();
        Self::new(name, cost, damage, armor)
    }
}

#[derive(Default)]
struct Store {
    weapons: Vec<Item>,
    armor: Vec<Item>,
    rings: Vec<Item>,
}

impl Store {
    fn new() -> Self {
        let mut store: Self = Default::default();
        for line in WEAPONS.lines() {
            store.weapons.push(Item::new_from_string(line));
        }
        for line in ARMOR.lines() {
            store.armor.push(Item::new_from_string(line));
        }
        for line in RINGS.lines() {
            store.rings.push(Item::new_from_string(line));
        }
        store
    }
}

fn attack(attacker: &Character, defender: &Character) -> i32 {
    max(1, attacker.damage.saturating_sub(defender.armor)) as i32
}

fn battle(player: &Character, enemy: &Character) -> bool {
    let mut player_hp = player.hit_points;
    let mut enemy_hp = enemy.hit_points;

    loop {
        enemy_hp -= attack(player, enemy);
        if enemy_hp <= 0 {
            return true;
        }
        player_hp -= attack(enemy, player);
        if player_hp <= 0 {
            return false;
        }
    }
}

fn solve_puzzle(enemy: Character) -> u32 {
    let store = Store::new();
    let mut player = Character {
        hit_points: 100,
        damage: 0,
        armor: 0,
    };
    let mut max_cost = 0;

    for weapon in store.weapons.iter() {
        let mut cost = weapon.cost;

        player.damage += weapon.damage_modifier;
        for armor in store.armor.iter() {
            player.armor += armor.armor_modifier;
            cost += armor.cost;

            for ring1 in store.rings.iter() {
                player.damage += ring1.damage_modifier;
                player.armor += ring1.armor_modifier;
                cost += ring1.cost;

                for ring2 in store.rings.iter() {
                    if ring2.name == ring1.name {
                        continue;
                    }
                    player.damage += ring2.damage_modifier;
                    player.armor += ring2.armor_modifier;
                    cost += ring2.cost;

                    if cost > max_cost {
                        if !battle(&player, &enemy) {
                            println!("Player loses at {} cost", cost);
                            max_cost = cost;
                        }
                    }

                    cost -= ring2.cost;
                    player.armor -= ring2.armor_modifier;
                    player.damage -= ring2.damage_modifier;
                }

                cost -= ring1.cost;
                player.armor -= ring1.armor_modifier;
                player.damage -= ring1.damage_modifier;
            }

            cost -= armor.cost;
            player.armor -= armor.armor_modifier;
        }
        player.damage -= weapon.damage_modifier;
    }

    max_cost
}

fn main() {
    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    if !battle(
        &Character {
            hit_points: 8,
            damage: 5,
            armor: 5,
        },
        &Character {
            hit_points: 12,
            damage: 7,
            armor: 2,
        },
    ) {
        println!("Battle test failed");
        return;
    }

    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(Character {
        hit_points: 103,
        damage: 9,
        armor: 2,
    });
    println!("Real Result : {}", result);
}
