#[derive(Default, Copy, Clone)]
struct Item {
    value: i64,
    prev: usize,
    next: usize,
}

#[derive(Default, Clone)]
struct EncryptedFile {
    list: Vec<Item>,
    val_0_index: usize,
}

impl EncryptedFile {
    fn init_from_file(&mut self, input_string: &String) {
        let mut index = 0;
        for line in input_string.lines() {
            let value: i32 = line.parse().unwrap();
            if value == 0 {
                self.val_0_index = index;
            }
            let mut new_item = Item {
                value: value as i64 * 811589153,
                prev: 0,
                next: index + 1,
            };
            if index > 0 {
                new_item.prev = index - 1;
            }
            index += 1;
            self.list.push(new_item);
        }
        //
        // Fix up the tail and head pointers
        //
        self.list.get_mut(0).unwrap().prev = self.list.len() - 1;
        self.list.last_mut().unwrap().next = 0;
    }

    fn remove_item(&mut self, index: usize) {
        let cur = self.list.get(index).unwrap();
        let prev_index = cur.prev;
        let next_index = cur.next;
        let prev = self.list.get_mut(prev_index).unwrap();
        prev.next = next_index;
        let next = self.list.get_mut(next_index).unwrap();
        next.prev = prev_index;
    }

    fn insert_item_after(&mut self, index: usize, after_item: usize) {
        let prev = self.list.get_mut(after_item).unwrap();
        let next_index = prev.next;
        prev.next = index;
        let next = self.list.get_mut(next_index).unwrap();
        next.prev = index;
        assert!(index != after_item);
        let cur = self.list.get_mut(index).unwrap();
        cur.prev = after_item;
        cur.next = next_index;
    }

    fn move_item(&mut self, index: usize, distance: i64) {
        //
        // Do the modular math here
        //
        let new_distance = distance % (self.list.len() as i64 - 1);
        let mut destination = index;
        if new_distance == 0 {
            return;
        }
        self.remove_item(index);
        if new_distance > 0 {
            for _i in 0..new_distance {
                destination = self.list[destination].next;
            }
        } else if new_distance < 0 {
            for _i in 0..new_distance.abs() {
                destination = self.list[destination].prev;
            }
            //
            // One more to get to the preceding node
            //
            destination = self.list[destination].prev;
        }
        assert!(index != destination);

        self.insert_item_after(index, destination);
    }

    fn mix(&mut self) {
        for i in 0..self.list.len() {
            self.move_item(i, self.list[i].value);
        }
    }

    fn get_grove_coordinates(&self) -> (i64, i64, i64) {
        let mut found_count = 0;
        let index_1 = 1000 % self.list.len();
        let index_2 = 2000 % self.list.len();
        let index_3 = 3000 % self.list.len();
        let mut result = (0, 0, 0);
        let mut current_index = self.val_0_index;
        for i in 0..self.list.len() {
            let item = &self.list[current_index];
            if i == index_1 {
                result.0 = item.value;
                found_count += 1;
            }
            if i == index_2 {
                result.1 = item.value;
                found_count += 1;
            }
            if i == index_3 {
                result.2 = item.value;
                found_count += 1;
            }
            if found_count == 3 {
                break;
            }
            current_index = item.next;
        }
        assert!(found_count == 3);
        println!("({}, {}, {})", result.0, result.1, result.2);
        result
    }
}

fn solve_puzzle(input_string: &String) -> i64 {
    let mut file: EncryptedFile = Default::default();
    file.init_from_file(input_string);
    for _i in 0..10 {
        file.mix();
    }
    let coords = file.get_grove_coordinates();

    let result = coords.0 + coords.1 + coords.2;

    result
}

fn main() {
    //
    // !!!! Update with the expected result for the sample data !!!!
    //
    let expected_sample_output = 1623178306;

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
