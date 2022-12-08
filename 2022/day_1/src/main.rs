fn part1(input_string: &String) {
    println!("Part1");

    let mut current_elf_calories = 0;
    let mut max_elf_calories = 0;
    for line in input_string.lines() {
        if let Ok(value) = line.parse::<u32>() {
            current_elf_calories += value;
        } else {
            if current_elf_calories > max_elf_calories {
                max_elf_calories = current_elf_calories;
            }
            current_elf_calories = 0;
        }
    }
    if current_elf_calories > max_elf_calories {
        max_elf_calories = current_elf_calories;
    }

    println!("result is {}", max_elf_calories);
}

fn part2(input_string: &String) {
    println!("Part2");
    let mut elves = Vec::new();

    let mut current_elf_calories = 0;
    for line in input_string.lines() {
        if let Ok(value) = line.parse::<u32>() {
            current_elf_calories += value;
        } else {
            elves.push(current_elf_calories);
            current_elf_calories = 0;
        }
    }
    elves.push(current_elf_calories);

    elves.sort();
    elves.reverse();
    println!("top 3 : {}, {}, and {}", elves[0], elves[1], elves[2]);
    let sum: u32 = elves.iter().take(3).sum();
    println!("sum : {}", sum);
}

fn main() {
    println!("Day1!");

    let input_result = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    );
    let test_input_string = input_result.unwrap();
    let input_result =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"));
    let real_input_string = input_result.unwrap();
    part1(&test_input_string);
    part1(&real_input_string);
    part2(&test_input_string);
    part2(&real_input_string);
}
