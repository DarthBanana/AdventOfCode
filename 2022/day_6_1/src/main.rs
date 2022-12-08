fn solve_puzzle(input_string: &String) {

    for line in input_string.lines() {
        let mut marker = 3;
        'outer : loop { 
            marker += 1;
            let substr = line.get((marker - 4)..(marker)).unwrap();            
            for (i,char) in substr.chars().enumerate() {                
                let tail = substr.get((i+1)..).unwrap();
                if tail.contains(char) {
                    continue 'outer;
                }
            }
            break;            
        }
        println!("Start of packet : {}", marker);
        
    }
    
}

fn main() {
    println!("Day 6 : Part 1!");
    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();
    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    println!("Sample:");
    solve_puzzle(&test_input_string);

    println!("Real:");
    solve_puzzle(&real_input_string);
}
