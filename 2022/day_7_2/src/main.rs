use std::{cell::RefCell, collections::HashMap, rc::Rc};

#[derive(Debug)]
struct Directory {
    name: String,
    size: RefCell<u32>,
    files: RefCell<HashMap<String, Rc<File>>>,
    directories: RefCell<HashMap<String, Rc<Directory>>>,
}
#[derive(Debug)]
struct File {
    name: String,
    size: u32,
}

fn find_deletion_candidate_size(dir: Rc<Directory>, threshold: u32) -> u32 {
    let mut candidate_dirs_sum = *dir.size.borrow();

    for (n, d) in dir.directories.borrow().iter() {
        if *d.size.borrow() >= threshold {
            let subdir_value = find_deletion_candidate_size(d.clone(), threshold);

            if subdir_value < candidate_dirs_sum {
                candidate_dirs_sum = subdir_value;
            }
        }
    }

    return candidate_dirs_sum;
}

fn print_tree(dir: &Directory, preamble: &String) {
    println!("{} {} (dir)", preamble, dir.name);
    let my_preamble = format!("  {}", preamble);
    for (n, d) in dir.directories.borrow().iter() {
        print_tree(d, &my_preamble);
    }
    for (n, f) in dir.files.borrow().iter() {
        println!("{} {} (file, size={})", my_preamble, n, f.size);
    }
}

fn calc_dir_sizes(dir: Rc<Directory>) -> u32 {
    let mut my_size = 0;
    let mut candidate_dirs_sum = 0;

    for (n, d) in dir.directories.borrow().iter() {
        candidate_dirs_sum = calc_dir_sizes(d.clone());
        my_size += *d.size.borrow();
    }
    for (n, f) in dir.files.borrow().iter() {
        my_size += f.size;
    }

    *dir.size.borrow_mut() = my_size;
    if my_size <= 100000 {
        candidate_dirs_sum += my_size;
    }
    return candidate_dirs_sum;
}

fn solve_puzzle(input_string: &String) -> u32 {
    let mut stack: Vec<Rc<Directory>> = Vec::new();

    let root_dir = Rc::new(Directory {
        name: String::from("/"),
        size: RefCell::new(0),
        files: RefCell::new(HashMap::new()),
        directories: RefCell::new(HashMap::new()),
    });

    let mut current_dir = root_dir.clone();

    for line in input_string.lines() {
        match line.chars().nth(0).unwrap() {
            '$' => {
                // Command
                match line.get(2..4).unwrap() {
                    "cd" => {
                        let dir_name = line.get(5..).unwrap();
                        match dir_name {
                            "/" => current_dir = root_dir.clone(),
                            ".." => current_dir = stack.pop().unwrap().clone(),
                            _ => {
                                if !current_dir.directories.borrow().contains_key(dir_name) {
                                    let new_dir = Rc::new(Directory {
                                        name: dir_name.to_string(),
                                        size: RefCell::new(0),
                                        directories: RefCell::new(HashMap::new()),
                                        files: RefCell::new(HashMap::new()),
                                    });
                                    current_dir
                                        .directories
                                        .borrow_mut()
                                        .insert(dir_name.to_string(), new_dir);
                                }
                                stack.push(current_dir.clone());
                                let child = current_dir
                                    .directories
                                    .borrow()
                                    .get(dir_name)
                                    .unwrap()
                                    .clone();
                                current_dir = child;
                            }
                        };
                    }
                    "ls" => {
                        // Nothing to do
                    }
                    _ => panic!("Invalid command"),
                }
            }
            'd' => {
                //
                // Found a new directory
                //
                let dir_name = line.get(4..).unwrap();
                if current_dir.directories.borrow().contains_key(dir_name) {
                    println!("Found a directory we already knew about {}", dir_name);
                } else {
                    let new_dir = Rc::new(Directory {
                        name: dir_name.to_string(),
                        size: RefCell::new(0),
                        directories: RefCell::new(HashMap::new()),
                        files: RefCell::new(HashMap::new()),
                    });
                    current_dir
                        .directories
                        .borrow_mut()
                        .insert(dir_name.to_string(), new_dir);
                }
            }
            _ => {
                // Found file
                let (size, filename) = sscanf::sscanf!(line, "{} {}", u32, str).unwrap();
                if current_dir.files.borrow().contains_key(filename) {
                    println!("Found a file we already knew about {}", filename);
                } else {
                    let new_file = Rc::new(File {
                        name: filename.to_string(),
                        size: size,
                    });
                    current_dir
                        .files
                        .borrow_mut()
                        .insert(filename.to_string(), new_file);
                }
            }
        }
    }

    let _result = calc_dir_sizes(root_dir.clone());
    print_tree(&root_dir, &" - ".to_string());

    let threshold = *root_dir.size.borrow() - (70000000 - 30000000);

    let result = find_deletion_candidate_size(root_dir, threshold);

    result
}

fn main() {
    let expected_sample_output = 24933642;

    let (day, part) = sscanf::sscanf!(env!("CARGO_PKG_NAME"), "day_{}_{}", u32, u32).unwrap();
    println!("Day {} : Part {}!", day, part);

    let test_input_string = std::fs::read_to_string(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("sample.txt"),
    )
    .unwrap();

    let real_input_string =
        std::fs::read_to_string(std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("input.txt"))
            .unwrap();

    println!("Testing Sample Data:");
    let result = solve_puzzle(&test_input_string);
    println!("Sample Result : {}", result);

    if result != expected_sample_output {
        println!("Wrong Answer!!!!! {}", result);
    } else {
        println!("Testing Real Data:");
        let result = solve_puzzle(&real_input_string);
        println!("Real Result : {}", result);
    }
}
