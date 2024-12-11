# Zoo-Keeper-App
Python program demonstrating OOP inheritance via a zoo management system. Features include animal classes with unique behaviors and attributes, such as Mammals, Birds, and Reptiles, derived from a base Animal class. The project showcases polymorphism and encapsulation, simulating feeding schedules, habitat details, and animal-specific traits.

# ZooKeeper Management System

A Python program demonstrating object-oriented programming (OOP) principles such as inheritance, polymorphism, and encapsulation through a zoo management system. The program models various animal species and their unique behaviors, simulating real-world interactions within a zoo.

---

## Features

- **Animal Hierarchy:**
  - Base `Animal` class with shared attributes and behaviors.
  - Specialized subclasses for specific types, such as `Mammals`, `Birds`, and `Reptiles`.

- **Encapsulation:**
  - Private and protected attributes to maintain integrity.
  - Getter and setter methods to access animal-specific details.

- **Polymorphism:**
  - Shared methods implemented differently for each subclass (e.g., feeding schedules and sounds).

- **Zoo Simulation:**
  - Feeding schedules for different animals.
  - Habitat information and animal-specific traits.

---

## Project Structure

- **`Animal` Class:**
  - Serves as the base class for all animals, defining common attributes like name, age, and species.

- **`Mammals`, `Birds`, and `Reptiles` Classes:**
  - Extend the `Animal` class and implement unique behaviors.

- **Simulation Functions:**
  - Handle feeding schedules, habitat management, and animal interaction.

---

## How to Run

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/zookeeper-management.git
   cd zookeeper-management
   ```

2. **Run the Program:**
   ```bash
   python3 zooKeeperOOPInheritance.py
   ```

3. **Follow the CLI Prompts:**
   - Explore animal data.
   - Simulate feeding or manage habitat details.

---

## Example Usage

- Display animal details:
  ```
  Name: Leo
  Species: Lion
  Age: 5
  Feeding Schedule: Twice daily
  ```

- Add a new animal to the zoo:
  ```
  Enter animal name: Polly
  Enter species: Parrot
  Enter age: 2
  Habitat: Tropical
  ```

- Simulate feeding:
  ```
  Feeding all animals...
  Leo (Lion) is being fed.
  Polly (Parrot) is being fed.
  ```

---

## Technologies Used

- Python 3.10+
- Object-Oriented Programming (OOP)

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

