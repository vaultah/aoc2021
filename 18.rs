use std::cell::RefCell;
use std::io::{self, BufRead};
use std::rc::Rc;

type RcNode = Rc<RefCell<Node>>;

struct Node {
    left: Option<RcNode>,
    right: Option<RcNode>,
    parent: Option<RcNode>,
    value: Option<i32>,
    index: Option<usize>,
}

impl Default for Node {
    fn default() -> Self {
        Node {
            left: None,
            right: None,
            parent: None,
            value: None,
            index: None,
        }
    }
}

fn add(a: &RcNode, b: &RcNode) -> RcNode {
    let parent = Rc::new(RefCell::new(Node {
        left: Some(a.clone()),
        right: Some(b.clone()),
        ..Default::default()
    }));
    a.borrow_mut().parent = Some(parent.clone());
    b.borrow_mut().parent = Some(parent.clone());
    parent
}

fn label(root: &RcNode) -> Vec<RcNode> {
    let mut rv = Vec::new();
    let mut stack = Vec::new();

    stack.push(root.clone());

    while let Some(node) = stack.pop() {
        let mut node_ref = node.borrow_mut();

        if let Some(temp) = &node_ref.right {
            stack.push(temp.clone());
        }

        if let Some(temp) = &node_ref.left {
            stack.push(temp.clone());
        }

        if node_ref.value.is_some() {
            node_ref.index = Some(rv.len());
            rv.push(node.clone());
        }
    }
    rv
}

fn explode(number: &RcNode, vec: &Vec<RcNode>) -> bool {
    let mut stack = Vec::new();
    stack.push((number.clone(), 0));

    while let Some(result) = stack.pop() {
        let (node, depth) = result;
        let node_ref = node.borrow();

        if node_ref.value.is_none() && depth == 4 {
            let left_ref = node_ref.left.as_ref().unwrap().borrow();
            let left_index = left_ref.index.unwrap();
            if left_index > 0 {
                let mut prev_ref = vec[left_index - 1].borrow_mut();
                prev_ref.value = Some(prev_ref.value.unwrap() + left_ref.value.unwrap());
            }

            let right_ref = node_ref.right.as_ref().unwrap().borrow();
            let right_index = right_ref.index.unwrap();
            if right_index < vec.len() - 1 {
                let mut next_ref = vec[right_index + 1].borrow_mut();
                next_ref.value = Some(next_ref.value.unwrap() + right_ref.value.unwrap());
            }

            let parent_rc = node_ref.parent.as_ref().unwrap();
            let replacement_node = Rc::new(RefCell::new(Node {
                parent: Some(parent_rc.clone()),
                value: Some(0),
                ..Default::default()
            }));

            let mut parent_ref = parent_rc.borrow_mut();
            if Rc::ptr_eq(&parent_ref.left.as_ref().unwrap(), &node) {
                parent_ref.left = Some(replacement_node);
            } else {
                parent_ref.right = Some(replacement_node);
            }

            return true;
        }

        if let Some(temp) = &node_ref.right {
            stack.push((temp.clone(), depth + 1));
        }

        if let Some(temp) = &node_ref.left {
            stack.push((temp.clone(), depth + 1));
        }
    }
    false
}

fn split(number: &RcNode) -> bool {
    let mut stack = Vec::new();
    stack.push(number.clone());

    while let Some(result) = stack.pop() {
        let node_ref = result.borrow();

        if let Some(value) = node_ref.value {
            if value > 9 {
                let left_replacement = Rc::new(RefCell::new(Node {
                    value: Some(value / 2),
                    ..Default::default()
                }));
                let right_replacement = Rc::new(RefCell::new(Node {
                    value: Some(value / 2 + value % 2),
                    ..Default::default()
                }));

                let parent_rc = node_ref.parent.as_ref().unwrap();
                let replacement_node = Rc::new(RefCell::new(Node {
                    left: Some(left_replacement.clone()),
                    right: Some(right_replacement.clone()),
                    parent: Some(parent_rc.clone()),
                    ..Default::default()
                }));

                left_replacement.borrow_mut().parent = Some(replacement_node.clone());
                right_replacement.borrow_mut().parent = Some(replacement_node.clone());

                let mut parent_ref = parent_rc.borrow_mut();
                if Rc::ptr_eq(&parent_ref.left.as_ref().unwrap(), &result) {
                    parent_ref.left = Some(replacement_node);
                } else {
                    parent_ref.right = Some(replacement_node);
                }

                return true;
            }
        }

        if let Some(temp) = &node_ref.right {
            stack.push(temp.clone());
        }

        if let Some(temp) = &node_ref.left {
            stack.push(temp.clone());
        }
    }
    false
}

fn reduce(number: &RcNode, vec: &Vec<RcNode>) -> bool {
    explode(number, vec) || split(number)
}

fn magnitude(number: &RcNode) -> i32 {
    let node_ref = number.borrow();
    match node_ref.value {
        Some(value) => value,
        None => {
            3 * magnitude(&node_ref.left.as_ref().unwrap())
                + 2 * magnitude(&node_ref.right.as_ref().unwrap())
        }
    }
}

fn parse(string: &str) -> RcNode {
    let mut counter = 0;
    let mut index = 0;

    for (i, c) in string.chars().enumerate() {
        if c == ']' {
            counter -= 1;
        } else if c == '[' {
            counter += 1;
        } else if c == ',' && counter == 1 {
            index = i;
            break;
        }
    }

    if index == 0 {
        Rc::new(RefCell::new(Node {
            value: Some(string.parse().unwrap()),
            ..Default::default()
        }))
    } else {
        let left = parse(&string[1..index]);
        let right = parse(&string[index + 1..string.len() - 1]);
        let node = Rc::new(RefCell::new(Node {
            left: Some(left.clone()),
            right: Some(right.clone()),
            ..Default::default()
        }));
        left.borrow_mut().parent = Some(node.clone());
        right.borrow_mut().parent = Some(node.clone());
        node
    }
}

fn main() {
    let mut maybe_node: Option<RcNode> = None;
    let mut number_strings = Vec::new();

    for line in io::stdin().lock().lines() {
        let input = line.unwrap();
        let trimmed = input.trim();
        number_strings.push(trimmed.to_string());

        let mut result = parse(trimmed);

        if let Some(last_node) = maybe_node {
            result = add(&last_node, &result);
            let mut vec = label(&result);

            while reduce(&result, &vec) {
                vec = label(&result);
            }
        }

        maybe_node = Some(result);
    }
    println!("Last magnitude is {}", magnitude(&maybe_node.unwrap()));

    let mut maximum_magnitude = 0;
    let mut i = 0;

    while i < number_strings.len() {
        let mut j = 0;

        while j < number_strings.len() {
            if i != j {
                let (first, second) = (parse(&number_strings[i]), parse(&number_strings[j]));
                let result = add(&first, &second);
                let mut vec = label(&result);
                while reduce(&result, &vec) {
                    vec = label(&result);
                }

                let current_magnitude = magnitude(&result);
                if current_magnitude > maximum_magnitude {
                    maximum_magnitude = current_magnitude;
                }
            }
            j += 1;
        }
        i += 1;
    }
    println!("Maximum magnitude {}", maximum_magnitude);
}
