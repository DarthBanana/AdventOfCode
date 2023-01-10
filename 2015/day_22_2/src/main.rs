use std::cmp::max;

struct Character {
    hit_points: i32,
    damage: u32,
    armor: u32,
}

#[derive(PartialEq, Eq, Debug, Clone, Copy)]
enum SpellType {
    NoSpell,
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
}

const REAL_ENEMY: Character = Character {
    hit_points: 71,
    damage: 10,
    armor: 0,
};

struct Spell {
    spell_type: SpellType,
    cost: u32,
}

const SPELLS: [Spell; 6] = [
    Spell {
        spell_type: SpellType::MagicMissile,
        cost: 53,
    },
    Spell {
        spell_type: SpellType::Drain,
        cost: 73,
    },
    Spell {
        spell_type: SpellType::Shield,
        cost: 113,
    },
    Spell {
        spell_type: SpellType::Poison,
        cost: 173,
    },
    Spell {
        spell_type: SpellType::Recharge,
        cost: 229,
    },
    Spell {
        spell_type: SpellType::NoSpell,
        cost: 0,
    },
];

fn attack(attacker: &Character, defender: &Character) -> i32 {
    max(1, attacker.damage.saturating_sub(defender.armor)) as i32
}

fn next_turn(
    turn: u32,
    enemy: &Character,
    mana_avail: u32,
    mana_spent: u32,
    player_hp: i32,
    enemy_hp: i32,
    active_spells: [u32; 6],
    min_mana: &mut u32,
    player_turn: bool,
) {
    let mut new_active_spells = active_spells;
    let mut player = Character {
        hit_points: player_hp,
        damage: 0,
        armor: 0,
    };

    let mut new_enemy_hp = enemy_hp;
    let mut new_mana_avail = mana_avail;

    if enemy_hp <= 0 {
        *min_mana = mana_spent;
        println!("Player wins: {}", *min_mana);
        return;
    }

    if mana_spent >= *min_mana {
        return;
    }

    if player_turn {
        player.hit_points -= 1;
        if player.hit_points <= 0 {
            return;
        }
    }

    // Apply effects
    for i in 0..new_active_spells.len() {
        if new_active_spells[i] > 0 {
            new_active_spells[i] -= 1;
            match SPELLS[i].spell_type {
                SpellType::Shield => player.armor += 7,
                SpellType::Poison => new_enemy_hp -= 3,
                SpellType::Recharge => new_mana_avail += 101,
                _ => panic!(),
            }
        }
    }
    if new_enemy_hp <= 0 {
        *min_mana = mana_spent;
        println!("Player wins: {}", *min_mana);
        return;
    }

    if player_turn {
        for i in 0..SPELLS.len() {
            let mut next_iteration_enemy_hp = new_enemy_hp;
            let mut next_iteration_player_hp = player.hit_points;
            let mut next_iteration_active_spells = new_active_spells;
            let s = &SPELLS[i];

            //
            // Apparently doing nothing isn't allowed though it gets to the finish
            // line cheaper.
            //
            if s.cost == 0 {
                continue;
            }

            if s.cost > new_mana_avail {
                continue;
            }
            if new_active_spells[i] > 0 {
                continue;
            }

            match s.spell_type {
                SpellType::NoSpell => (),
                SpellType::MagicMissile => next_iteration_enemy_hp -= 4,
                SpellType::Drain => {
                    next_iteration_enemy_hp -= 2;
                    next_iteration_player_hp += 2;
                }
                SpellType::Shield => next_iteration_active_spells[i] = 6,
                SpellType::Poison => next_iteration_active_spells[i] = 6,
                SpellType::Recharge => next_iteration_active_spells[i] = 5,
            }

            next_turn(
                turn + 1,
                enemy,
                new_mana_avail - s.cost,
                mana_spent + s.cost,
                next_iteration_player_hp,
                next_iteration_enemy_hp,
                next_iteration_active_spells,
                min_mana,
                false,
            );
        }
    } else {
        let mut new_player_hp = player.hit_points;
        new_player_hp -= attack(enemy, &player);
        if new_player_hp <= 0 {
            return;
        }
        next_turn(
            turn + 1,
            enemy,
            new_mana_avail,
            mana_spent,
            new_player_hp,
            new_enemy_hp,
            new_active_spells,
            min_mana,
            true,
        );
    }
}

fn solve_puzzle(enemy: &Character, hp: i32, mana: u32) -> u32 {
    let mut min_mana = u32::MAX;
    let active_spells: [u32; 6] = [0; 6];

    next_turn(
        1,
        enemy,
        mana,
        0,
        hp,
        enemy.hit_points,
        active_spells,
        &mut min_mana,
        true,
    );

    min_mana
}

fn main() {
    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    // Real answer is greater than 1771
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&REAL_ENEMY, 50, 500);
    println!("Real Result : {}", result);
}
