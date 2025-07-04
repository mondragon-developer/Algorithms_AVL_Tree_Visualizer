# AVL Tree Visualizer

An interactive educational tool for visualizing AVL (Adelson-Velsky and Landis) tree operations with a modern GUI built using Python and CustomTkinter. This application provides a real-time visual representation of AVL tree operations, helping students and developers understand how self-balancing binary search trees work.

---

## Table of Contents

- [Description](#descriptiondescription)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Real-World Applications](#real-world-applications)
- [Author](#author)
- [License](#license)
- [Acknowledgments](#acknowledgments)
- [Screenshots](#screenshots)

---

## Description

This application was created for the CSC6023 - Advanced Algorithms course, a graduate-level class in a Master of Science program in Computer Science and Software Engineering, to demonstrate the core principles of AVL trees. It allows users to insert and delete nodes and watch the tree automatically rebalance itself to maintain optimal performance. The tool includes step-by-step explanations for each operation, making it an excellent companion for learning this fundamental data structure.

The script is fully documented following PyDoc standards, ensuring that the code is readable and maintainable.

---

## Features

- **Interactive Visualization**: Real-time graphical representation of the tree structure.
- **Smart Insert/Delete**: Automatically inserts a value if it doesn't exist or deletes it if it does.
- **Zoom and Pan Controls**: Easily navigate large trees with zoom-in/out and reset functionality.
- **Step-by-Step Explanations**: A popup window details the logic behind each insertion, deletion, and rebalancing rotation.
- **Educational Information**: A built-in tutorial explains what AVL trees are, their properties, and their importance.
- **Console Output**: Print the tree structure to the console in a readable format for debugging purposes.
- **Modern UI**: Built with a clean, dark theme using the CustomTkinter library.

---

## Requirements

To run this application, you will need:

- Python 3.7 or higher
- `customtkinter` library
- `tkinter` (typically included with standard Python installations)

---

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/mondragon-developer/Algorithms_AVL_Tree_Visualizer.git
    cd Algorithms_AVL_Tree_Visualizer
    ```

2.  **Install the required library:**

    ```bash
    pip install customtkinter
    ```

3.  **Run the application:**

    ```bash
    python avl_tree_visualizer.py
    ```

---

## Usage

1.  **Start the Application**: Run the script to open the main window.
2.  **Enter a Value**: Type a positive integer into the input field.
3.  **Perform an Operation**:
    - If the value is **not** in the tree, it will be **inserted**.
    - If the value **is** in the tree, it will be **deleted**.
4.  **View Explanations**: A popup window will appear on the side, explaining the steps taken during the operation.
5.  **Use the Controls**:
    - **Zoom**: Use the zoom buttons to adjust the size of the tree visualization.
    - **Clear**: Resets the tree to an empty state.
    - **Print to Console**: Outputs the current tree structure to your terminal.
    - **What is AVL?**: Opens a detailed information panel about the algorithm.
    - **Exit**: Close the application by entering a non-positive integer or clicking the "Exit" button.

---

## How It Works

The application is built on the core principles of AVL trees, which are a type of self-balancing binary search tree.

### AVL Tree Properties

- **Binary Search Tree (BST)**: For any given node, all values in its left subtree are smaller, and all values in its right subtree are larger.
- **Self-Balancing**: The height difference between the left and right subtrees of any node (the "balance factor") is never more than 1. This ensures that the tree's height remains logarithmic, `O(log n)`.

### Automatic Rebalancing

If an insertion or deletion causes a node's balance factor to become greater than 1, the tree performs **rotations** to restore balance:

- **Left Rotation**: Used when a node's right subtree becomes too "heavy."
- **Right Rotation**: Used when a node's left subtree becomes too "heavy."
- **Left-Right and Right-Left Rotations**: These are double rotations used to fix more complex imbalance cases.

---

## Real-World Applications

AVL trees are highly efficient for lookups and are used in many practical applications, including:

- **Database Systems**: For indexing data to allow for fast retrieval.
- **File Systems**: Managing directory structures.
- **Compilers**: Implementing symbol tables.
- **Network Routers**: Storing and searching IP routing tables.

---

## Author

- **Jose Mondragon**
- _Project for CSC6023 - Advanced Algorithms_

---

## License

This project is open source and available under the **MIT License**. See the `LICENSE` file for more details.

---

## Acknowledgments

- This project was built using [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library by Tom Schimansky.
- Inspired by the need for clear, interactive tools in computer science education.

---

## Screenshots

-[image1.png](https://github.com/mondragon-developer/Algorithms_AVL_Tree_Visualizer/issues/1#issue-3203674732) 
-[image2.png](https://github.com/mondragon-developer/Algorithms_AVL_Tree_Visualizer/issues/2#issue-3203676095) 
-[image3.png](https://github.com/mondragon-developer/Algorithms_AVL_Tree_Visualizer/issues/3#issue-3203677192)
