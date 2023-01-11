fn get_code_number_from_coordinates(x: u64, y: u64) -> u64 {
    let mut value: u64 = 0;
    for i in 1..=x {
        value += i;
    }
    for i in 1..y {
        value += x + (i - 1);
    }
    value
}

fn get_code_from_number(num: u64) -> u64 {
    let mut value: u64 = 20151125;
    let a = 252533;
    let b = 33554393;
    //
    // n' = (n*a)%b
    //
    for _i in 1..num {
        value = (value * a) % b;
    }
    value
}

fn solve_puzzle(x: u64, y: u64) -> u64 {
    let num = get_code_number_from_coordinates(x, y);
    get_code_from_number(num)
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
    //
    println!("Testing Real Data:");
    let result = solve_puzzle(3019, 3010);
    println!("Real Result : {}", result);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn get_coord_to_value(path: &str) -> Vec<(u64, u64, u64)> {
        let mut list: Vec<(u64, u64, u64)> = Vec::new();
        let test_input_string =
            std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join(path))
                .unwrap();
        let mut y = 1;

        for line in test_input_string.lines() {
            let mut x = 1;
            for s in line.split_ascii_whitespace() {
                let v = sscanf::sscanf!(s, "{}", u64).unwrap();
                list.push((x, y, v));
                x += 1;
            }
            y += 1;
        }
        list
    }

    #[test]
    fn check_coord_to_number() {
        let tests = get_coord_to_value("index.txt");
        for (x, y, v) in tests {
            let result = get_code_number_from_coordinates(x, y);
            assert_eq!(
                result, v,
                "({}, {}) returned {} rather than {}",
                x, y, result, v
            );
        }
    }
    #[test]
    fn check_index_to_code() {
        assert_eq!(get_code_from_number(1), 20151125);
        assert_eq!(get_code_from_number(2), 31916031);
        assert_eq!(get_code_from_number(3), 18749137);
    }

    #[test]
    fn check_coord_to_code() {
        let tests = get_coord_to_value("codes.txt");
        for (x, y, v) in tests {
            let index = get_code_number_from_coordinates(x, y);
            let result = get_code_from_number(index);
            assert_eq!(
                result, v,
                "({}, {}) returned {} rather than {}",
                x, y, result, v
            );
        }
    }
}
