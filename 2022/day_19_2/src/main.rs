use std::{
    cmp::max,
    ops::{Add, Mul, Sub},
};

#[derive(Default, Copy, Clone)]
struct Robot {
    produces: Resources,
    needs: Resources,
}
#[derive(Default, Debug, Clone, Copy)]
struct Resources {
    ore: u32,
    clay: u32,
    obsidian: u32,
    geode: u32,
}
struct State {
    max_geodes_found: u32,
}

impl Add for Resources {
    type Output = Resources;

    fn add(self, other: Resources) -> Resources {
        Resources {
            ore: self.ore + other.ore,
            clay: self.clay + other.clay,
            obsidian: self.obsidian + other.obsidian,
            geode: self.geode + other.geode,
        }
    }
}

impl Sub for Resources {
    type Output = Resources;

    fn sub(self, other: Resources) -> Resources {
        Resources {
            ore: self.ore - other.ore,
            clay: self.clay - other.clay,
            obsidian: self.obsidian - other.obsidian,
            geode: self.geode - other.geode,
        }
    }
}
impl Mul<u32> for Resources {
    type Output = Resources;

    fn mul(self, other: u32) -> Resources {
        Resources {
            ore: self.ore * other,
            clay: self.clay * other,
            obsidian: self.obsidian * other,
            geode: self.geode * other,
        }
    }
}

#[derive(Default)]
struct Blueprint {
    id: u32,
    robots: Vec<Robot>,
    production_limits: Resources,
}

fn exceeds_limits(production: &Resources, limits: &Resources) -> bool {
    if production.ore > limits.ore
        || production.clay > limits.clay
        || production.obsidian > limits.obsidian
        || production.geode > limits.geode
    {
        return true;
    }
    return false;
}

fn time_needed_to_build_robot(robot: &Robot, avail: &Resources, production: &Resources) -> u32 {
    let mut time = 0;
    if avail.ore < robot.needs.ore {
        if production.ore == 0 {
            return u32::MAX;
        }
        let delta = robot.needs.ore - avail.ore;
        let mut minutes = delta / production.ore;
        if (delta % production.ore) > 0 {
            minutes += 1;
        }
        time = max(time, minutes);
    }

    if avail.clay < robot.needs.clay {
        if production.clay == 0 {
            return u32::MAX;
        }
        let delta = robot.needs.clay - avail.clay;
        let mut minutes = delta / production.clay;
        if (delta % production.clay) > 0 {
            minutes += 1;
        }
        time = max(time, minutes);
    }

    if avail.obsidian < robot.needs.obsidian {
        if production.obsidian == 0 {
            return u32::MAX;
        }
        let delta = robot.needs.obsidian - avail.obsidian;
        let mut minutes = delta / production.obsidian;
        if (delta % production.obsidian) > 0 {
            minutes += 1;
        }
        time = max(time, minutes);
    }
    time + 1
}

fn find_most_geodes(
    blueprint: &Blueprint,
    production: &Resources,
    resources: &Resources,
    time_left: u32,
    state: &mut State,
) {
    assert!(!exceeds_limits(production, &blueprint.production_limits));
    state.max_geodes_found = max(
        state.max_geodes_found,
        resources.geode + production.geode * (time_left),
    );

    //
    // See if we are out of time
    //
    if time_left == 0 {
        return;
    }

    let mut theor_max = 0;
    for i in 0..=time_left {
        theor_max += i;
    }
    theor_max += production.geode * time_left + resources.geode;
    if theor_max < state.max_geodes_found {
        return;
    }

    for robot in blueprint.robots.iter() {
        let time = time_needed_to_build_robot(&robot, resources, production);
        if time > time_left {
            continue;
        }
        let new_resources = (*resources + *production * time) - robot.needs;
        let new_production = *production + robot.produces;
        if exceeds_limits(&new_production, &blueprint.production_limits) {
            continue;
        }

        find_most_geodes(
            blueprint,
            &new_production,
            &new_resources,
            time_left - time,
            state,
        );
    }
}

fn get_blueprint_from_line(line: &str) -> Blueprint {
    let mut ore_robot: Robot = Default::default();
    ore_robot.produces.ore = 1;
    let mut clay_robot: Robot = Default::default();
    clay_robot.produces.clay = 1;
    let mut obsidian_robot: Robot = Default::default();
    obsidian_robot.produces.obsidian = 1;
    let mut geode_robot: Robot = Default::default();
    geode_robot.produces.geode = 1;
    let mut blueprint: Blueprint = Default::default();
    (blueprint.id, ore_robot.needs.ore, clay_robot.needs.ore, obsidian_robot.needs.ore, obsidian_robot.needs.clay, geode_robot.needs.ore, geode_robot.needs.obsidian) = sscanf::sscanf!(line, "Blueprint {}: Each ore robot costs {} ore. Each clay robot costs {} ore. Each obsidian robot costs {} ore and {} clay. Each geode robot costs {} ore and {} obsidian.", u32, u32, u32,u32,u32,u32,u32).unwrap();

    let mut ore_needs = vec![
        ore_robot.needs.ore,
        clay_robot.needs.ore,
        obsidian_robot.needs.ore,
        geode_robot.needs.ore,
    ];
    ore_needs.sort();
    let max_ore = *ore_needs.last().unwrap();
    blueprint.production_limits = Resources {
        ore: max_ore,
        clay: obsidian_robot.needs.clay,
        obsidian: geode_robot.needs.obsidian,
        geode: u32::MAX,
    };
    blueprint.robots.push(geode_robot);
    blueprint.robots.push(obsidian_robot);
    blueprint.robots.push(clay_robot);
    blueprint.robots.push(ore_robot);
    blueprint
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut result = 1;
    let mut line_count = 0;
    let resources: Resources = Default::default();
    let production = Resources {
        ore: 1,
        clay: 0,
        obsidian: 0,
        geode: 0,
    };

    let mut state = State {
        max_geodes_found: 0,
    };
    for line in input_string.lines() {
        if line_count >= 3 {
            break;
        }
        let blueprint = get_blueprint_from_line(line);
        state.max_geodes_found = 0;
        println!("Finding geodes for blueprint {}", blueprint.id);
        find_most_geodes(&blueprint, &production, &resources, 32, &mut state);
        println!(
            "Found {} for blueprint {}",
            state.max_geodes_found, blueprint.id
        );
        result *= state.max_geodes_found;
        line_count += 1;
    }

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 62 * 56;

    //
    // Print the specific puzzle info
    //
    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    //
    // Read in the sample input
    //
    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();

    //
    // Read in the real input
    //
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    //
    // Solve for the sample input
    //
    println!("Testing Sample Data:");
    let result = solve_puzzle(&test_input_string);
    println!("Sample Result : {}", result);

    //
    // Check if the sample input matches the expected result
    //
    if result != expected_sample_output {
        println!("Wrong Answer!!!!! {}", result);
        return;
    }

    //
    // Solve for the real input, only in the case that the result
    // for the sample input was correct
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(&real_input_string);
    println!("Real Result : {}", result);
}
