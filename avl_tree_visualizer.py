"""
AVL Tree Implementation with GUI (CustomTkinter) for CSC6023 - Advanced Algorithms
by Jose Mondragon

This program implements an AVL (Adelson-Velsky and Landis) tree with:
1. A graphical interface for visualization of the tree structure
2. Asks the user for positive integer numbers repeatedly
3. Inserts the number into the tree if it doesn't exist
4. Deletes the number from the tree if it already exists
5. Prints the tree after each operation
6. Ends when the user enters a non-positive integer

The implementation maintains the AVL property: the heights of the 
two child subtrees of any node differ by at most one.

Enhanced with:
- Complete pydoc documentation
- Improved GUI with information popup
- Better error handling and user feedback
"""

import customtkinter as ctk
import tkinter as tk
import math


class TreeNode(object):
    """
    Represents a single node in the AVL tree.
    
    An AVL tree node contains data, references to left and right children,
    and height information needed for tree balancing operations.
    
    Attributes:
        data (int): The integer value stored in this node
        left (TreeNode): Reference to the left child node
        right (TreeNode): Reference to the right child node  
        height (int): Height of this node in the tree (leaf nodes have height 1)
        
    Example:
        >>> node = TreeNode(10)
        >>> node.data
        10
        >>> node.height
        1
        >>> node.left is None
        True
    """
    
    def __init__(self, data):
        """
        Initialize a new tree node with the given data.
        
        Args:
            data (int): The integer value to store in this node
            
        Note:
            New nodes are created as leaf nodes with height 1 and no children.
        """
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(object):
    """
    Implementation of an AVL (Adelson-Velsky and Landis) self-balancing binary search tree.
    
    An AVL tree is a binary search tree where the heights of the two child subtrees 
    of any node differ by at most one. This guarantees O(log n) performance for
    search, insertion, and deletion operations.
    
    The tree automatically maintains balance through rotations whenever an operation
    would cause the tree to become unbalanced.
    
    Attributes:
        root (TreeNode): The root node of the tree, None if tree is empty
        
    Example:
        >>> tree = AVLTree()
        >>> tree.insert(10)
        >>> tree.insert(5)
        >>> tree.search(10)
        True
        >>> tree.search(15)
        False
    """
    
    def __init__(self):
        """Initialize an empty AVL tree."""
        self.root = None

    def search(self, data):
        """
        Search for a value in the AVL tree.
        
        Args:
            data (int): The value to search for
            
        Returns:
            bool: True if the value exists in the tree, False otherwise
            
        Time Complexity:
            O(log n) where n is the number of nodes in the tree
            
        Example:
            >>> tree = AVLTree()
            >>> tree.insert(10)
            >>> tree.search(10)
            True
            >>> tree.search(5)
            False
        """
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, root, data):
        """
        Recursively search for a value starting from the given root.
        
        Args:
            root (TreeNode): The root of the subtree to search
            data (int): The value to search for
            
        Returns:
            bool: True if found, False otherwise
        """
        if not root:
            return False
        elif root.data == data:
            return True
        elif data < root.data:
            return self._search_recursive(root.left, data)
        else:
            return self._search_recursive(root.right, data)
    
    def contains(self, data):
        """
        Check if a value exists in the tree (alias for search).
        
        Args:
            data (int): The value to check for
            
        Returns:
            bool: True if the value exists, False otherwise
        """
        return self.search(data)
            
    def insert(self, data):
        """
        Insert a value into the AVL tree.
        
        If the value already exists, no changes are made to the tree.
        After insertion, the tree is automatically rebalanced if necessary.
        
        Args:
            data (int): The value to insert
            
        Time Complexity:
            O(log n) where n is the number of nodes in the tree
            
        Example:
            >>> tree = AVLTree()
            >>> tree.insert(10)
            >>> tree.insert(5)
            >>> tree.contains(10)
            True
        """
        self.root = self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, root, data):
        """
        Recursively insert a value and rebalance the tree.
        
        Args:
            root (TreeNode): The root of the current subtree
            data (int): The value to insert
            
        Returns:
            TreeNode: The new root of the subtree after insertion and balancing
        """
        # Find the correct location and insert the node
        if not root:
            return TreeNode(data)
        elif data < root.data:
            root.left = self._insert_recursive(root.left, data)
        else:
            root.right = self._insert_recursive(root.right, data)

        root.height = 1 + max(self._get_height(root.left),
                              self._get_height(root.right))

        # Update the balance factor and balance the tree
        balance_factor = self._get_balance(root)
        
        # Left Left Case
        if balance_factor > 1 and data < root.left.data:
            return self._right_rotate(root)

        # Right Right Case
        if balance_factor < -1 and data > root.right.data:
            return self._left_rotate(root)

        # Left Right Case
        if balance_factor > 1 and data > root.left.data:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)

        # Right Left Case
        if balance_factor < -1 and data < root.right.data:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    def delete(self, data):
        """
        Delete a value from the AVL tree.
        
        If the value doesn't exist, no changes are made to the tree.
        After deletion, the tree is automatically rebalanced if necessary.
        
        Args:
            data (int): The value to delete
            
        Time Complexity:
            O(log n) where n is the number of nodes in the tree
            
        Example:
            >>> tree = AVLTree()
            >>> tree.insert(10)
            >>> tree.delete(10)
            >>> tree.contains(10)
            False
        """
        self.root = self._delete_recursive(self.root, data)
    
    def _delete_recursive(self, root, data):
        """
        Recursively delete a value and rebalance the tree.
        
        Args:
            root (TreeNode): The root of the current subtree
            data (int): The value to delete
            
        Returns:
            TreeNode: The new root of the subtree after deletion and balancing
        """
        # Find the node to be deleted and remove it
        if not root:
            return root
        elif data < root.data:
            root.left = self._delete_recursive(root.left, data)
        elif data > root.data:
            root.right = self._delete_recursive(root.right, data)
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
                
            # Node with two children
            # Get the inorder successor (smallest in the right subtree)
            temp = self._get_min_value_node(root.right)
            
            # Copy the inorder successor's data to this node
            root.data = temp.data
            
            # Delete the inorder successor
            root.right = self._delete_recursive(root.right, temp.data)
        
        # If the tree had only one node, return
        if root is None:
            return root
            
        # Update the height of the current node
        root.height = 1 + max(self._get_height(root.left),
                              self._get_height(root.right))
                              
        # Get the balance factor
        balance_factor = self._get_balance(root)
        
        # Balance the tree
        # Left Left Case
        if balance_factor > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)
            
        # Left Right Case
        if balance_factor > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
            
        # Right Right Case
        if balance_factor < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)
            
        # Right Left Case
        if balance_factor < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)
            
        return root

    def _left_rotate(self, z):
        """
        Perform a left rotation to rebalance the tree.
        
        Left rotation is used when the right subtree is heavier than the left subtree.
        
        Args:
            z (TreeNode): The node around which to perform the rotation
            
        Returns:
            TreeNode: The new root of the rotated subtree
            
        Note:
            This is a fundamental AVL tree operation that maintains the BST property
            while reducing the height of unbalanced subtrees.
        """
        y = z.right
        T2 = y.left
        
        # Perform rotation
        y.left = z
        z.right = T2
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))
                           
        # Return the new root
        return y

    def _right_rotate(self, z):
        """
        Perform a right rotation to rebalance the tree.
        
        Right rotation is used when the left subtree is heavier than the right subtree.
        
        Args:
            z (TreeNode): The node around which to perform the rotation
            
        Returns:
            TreeNode: The new root of the rotated subtree
            
        Note:
            This is a fundamental AVL tree operation that maintains the BST property
            while reducing the height of unbalanced subtrees.
        """
        y = z.left
        T3 = y.right
        
        # Perform rotation
        y.right = z
        z.left = T3
        
        # Update heights
        z.height = 1 + max(self._get_height(z.left),
                           self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left),
                           self._get_height(y.right))
                           
        # Return the new root
        return y

    def _get_height(self, root):
        """
        Get the height of a node.
        
        Args:
            root (TreeNode): The node to check (can be None)
            
        Returns:
            int: Height of the node, or 0 if node is None
            
        Note:
            Height is defined as the longest path from the node to a leaf.
            Leaf nodes have height 1, empty trees have height 0.
        """
        if not root:
            return 0
        return root.height

    def _get_balance(self, root):
        """
        Calculate the balance factor of a node.
        
        Args:
            root (TreeNode): The node to check (can be None)
            
        Returns:
            int: Balance factor (left height - right height)
            
        Note:
            A balance factor of -1, 0, or 1 indicates a balanced node.
            Values outside this range indicate the tree needs rebalancing.
        """
        if not root:
            return 0
        return self._get_height(root.left) - self._get_height(root.right)

    def _get_min_value_node(self, root):
        """
        Find the node with the minimum value in a subtree.
        
        Args:
            root (TreeNode): The root of the subtree to search
            
        Returns:
            TreeNode: The node containing the minimum value
            
        Note:
            In a BST, the minimum value is always the leftmost node.
        """
        if root is None or root.left is None:
            return root
        return self._get_min_value_node(root.left)

    def get_nodes_by_level(self):
        """
        Get all nodes organized by their level in the tree.
        
        Returns:
            list: List of lists, where each inner list contains all nodes at that level
                 Level 0 contains the root, level 1 contains the root's children, etc.
                 
        Example:
            For a tree with root 10, left child 5, right child 15:
            >>> tree.get_nodes_by_level()
            [[TreeNode(10)], [TreeNode(5), TreeNode(15)]]
            
        Note:
            This is useful for visualization and level-order traversal of the tree.
        """
        if not self.root:
            return []
            
        levels = []
        self._collect_nodes_by_level(self.root, 0, levels)
        return levels
    
    def _collect_nodes_by_level(self, node, level, levels):
        """
        Recursively collect nodes at each level.
        
        Args:
            node (TreeNode): Current node being processed
            level (int): Current level in the tree (0 = root level)
            levels (list): List of lists to store nodes by level
        """
        if not node:
            return
            
        # Extend the levels list if necessary
        while len(levels) <= level:
            levels.append([])
            
        levels[level].append(node)
        
        # Recursively collect nodes from left and right subtrees
        self._collect_nodes_by_level(node.left, level+1, levels)
        self._collect_nodes_by_level(node.right, level+1, levels)
    
    def print_tree(self):
        """
        Print a visual representation of the tree structure to the console.
        
        The tree is displayed with the root at the top and branches extending downward.
        'R----' indicates the root or a right child, 'L----' indicates a left child.
        
        Example output:
            R----10
                 L----5
                 R----15
                      L----12
                      R----18
        """
        if not self.root:
            print("Tree is empty")
            return
        print("AVL Tree Structure:")
        self._print_helper(self.root, "", True)
    
    def _print_helper(self, curr_ptr, indent, last):
        """
        Recursive helper function for printing the tree structure.
        
        Args:
            curr_ptr (TreeNode): Current node being printed
            indent (str): Current indentation string for formatting
            last (bool): True if this is the last child at its level
        """
        if curr_ptr:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
                
            print(curr_ptr.data)
            self._print_helper(curr_ptr.left, indent, False)
            self._print_helper(curr_ptr.right, indent, True)


class TreeVisualizer(ctk.CTk):
    """
    Main GUI application for visualizing and interacting with the AVL tree.
    
    This class provides a modern graphical interface using CustomTkinter that allows
    users to insert and delete values from an AVL tree while seeing the tree structure
    visualized in real-time.
    
    Features:
        - Real-time tree visualization with colored nodes
        - Insert/delete operations based on value existence
        - Information popup explaining AVL trees
        - Console output option for debugging
        - Modern dark theme interface
        
    Attributes:
        tree (AVLTree): The AVL tree instance being visualized
        canvas (CTkCanvas): Canvas widget for drawing the tree
        entry (CTkEntry): Input field for entering values
        status_label (CTkLabel): Label showing current operation status
    """
    
    def __init__(self):
        """
        Initialize the tree visualizer application.
        
        Sets up the GUI components, creates an empty AVL tree, and displays
        the initial interface ready for user interaction.
        """
        super().__init__()
        self.tree = AVLTree()
        self.operation_log = []  # Track operations for explanations
        self.zoom_scale = 1.0
        self.current_explanation_window = None  # Track current popup window
        self.title("AVL Tree Visualizer by Jose Mondragon")
        self.geometry("1100x900")
        
        # Set the window icon and make it resizable
        self.resizable(True, True)
        
        # Create and pack the main components
        self._create_header()
        self._create_canvas()
        self._create_controls()
        self._create_status_bar()
        
        # Initial tree rendering
        self.redraw_tree()

    def _create_header(self):
        """Create the header section with title and info button."""
        header_frame = ctk.CTkFrame(self)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="AVL Tree Visualizer", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Info button
        info_button = ctk.CTkButton(
            header_frame,
            text="ℹ️ What is AVL?",
            command=self._show_algorithm_info,
            width=120,
            height=32,
            font=ctk.CTkFont(size=12)
        )
        info_button.pack(side="right", padx=20, pady=15)

    def _create_canvas(self):
        """Create the main canvas for tree visualization."""
        canvas_frame = ctk.CTkFrame(self)
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        canvas_label = ctk.CTkLabel(canvas_frame, text="Tree Visualization", font=ctk.CTkFont(size=14, weight="bold"))
        canvas_label.pack(pady=(10, 5))
        
        self.canvas = ctk.CTkCanvas(
            canvas_frame, 
            width=1000, 
            height=450, 
            bg="#2c2c2c", 
            highlightthickness=0
        )
        self.canvas.pack(pady=(0, 10))

    def _create_controls(self):
        """Create the control panel with input and buttons."""
        control_frame = ctk.CTkFrame(self)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Instructions
        instruction_label = ctk.CTkLabel(
            control_frame, 
            text="Enter a positive integer to insert/delete from the tree:",
            font=ctk.CTkFont(size=12)
        )
        instruction_label.pack(pady=(15, 5))
        
        # Input section
        input_frame = ctk.CTkFrame(control_frame)
        input_frame.pack(pady=10)
        
        self.entry = ctk.CTkEntry(
            input_frame, 
            placeholder_text="Enter a positive integer",
            width=200,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        self.entry.pack(side="left", padx=10, pady=10)
        self.entry.bind("<Return>", self.handle_input)

        self.submit_button = ctk.CTkButton(
            input_frame, 
            text="Insert/Delete", 
            command=self.handle_input,
            width=120,
            height=35
        )
        self.submit_button.pack(side="left", padx=5, pady=10)

        # Additional controls
        extra_controls_frame = ctk.CTkFrame(control_frame)
        extra_controls_frame.pack(pady=(0, 15))
        
        self.clear_button = ctk.CTkButton(
            extra_controls_frame,
            text="Clear Tree",
            command=self._clear_tree,
            width=100,
            height=30
        )
        self.clear_button.pack(side="left", padx=5, pady=5)
        
        self.print_button = ctk.CTkButton(
            extra_controls_frame,
            text="Print to Console",
            command=self._print_to_console,
            width=130,
            height=30
        )
        self.print_button.pack(side="left", padx=5, pady=5)

        self.exit_button = ctk.CTkButton(
            extra_controls_frame, 
            text="Exit", 
            command=self.destroy,
            width=80,
            height=30
        )
        self.exit_button.pack(side="left", padx=5, pady=5)

        # Add zoom controls
        zoom_frame = ctk.CTkFrame(control_frame)
        zoom_frame.pack(pady=(0, 10))

        zoom_label = ctk.CTkLabel(zoom_frame, text="Zoom:", font=ctk.CTkFont(size=12))
        zoom_label.pack(side="left", padx=5)

        self.zoom_in_button = ctk.CTkButton(
            zoom_frame,
            text="➕ Zoom In",
            command=self._zoom_in,
            width=90,
            height=30
        )
        self.zoom_in_button.pack(side="left", padx=5)

        self.zoom_out_button = ctk.CTkButton(
            zoom_frame,
            text="➖ Zoom Out", 
            command=self._zoom_out,
            width=90,
            height=30
        )
        self.zoom_out_button.pack(side="left", padx=5)

        self.zoom_reset_button = ctk.CTkButton(
            zoom_frame,
            text="🔄 Reset",
            command=self._zoom_reset,
            width=80,
            height=30
        )
        self.zoom_reset_button.pack(side="left", padx=5)

        self.zoom_label = ctk.CTkLabel(zoom_frame, text="100%", font=ctk.CTkFont(size=12))
        self.zoom_label.pack(side="left", padx=10)

    def _create_status_bar(self):
        """Create the status bar for user feedback."""
        self.status_label = ctk.CTkLabel(
            self, 
            text="Ready - Enter a positive integer to begin",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(pady=(0, 15))

    def _show_algorithm_info(self):
        """
        Display an information popup explaining the AVL tree algorithm.
        
        Shows a detailed explanation of what AVL trees are, their properties,
        and why they're useful in computer science.
        """
        info_window = ctk.CTkToplevel(self)
        info_window.title("About AVL Trees")
        info_window.geometry("650x520")
        info_window.resizable(True, True)
        
        # Make it modal
        info_window.transient(self)
        info_window.grab_set()
        
        # Center the window
        info_window.update_idletasks()
        x = (info_window.winfo_screenwidth() // 2) - (650 // 2)
        y = (info_window.winfo_screenheight() // 2) - (520 // 2)
        info_window.geometry(f"650x520+{x}+{y}")
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(info_window)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            scrollable_frame, 
            text="AVL Trees Explained", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 15))
        
        # Information text
        info_text = """
🌳 What is an AVL Tree?

An AVL tree is a self-balancing binary search tree named after its inventors Adelson-Velsky and Landis (1962). It's one of the most important data structures in computer science.

📊 Key Properties:

• Binary Search Tree: For any node, all values in the left subtree are smaller, and all values in the right subtree are larger.

• Self-Balancing: The tree automatically maintains balance after every insertion and deletion operation.

• Height Balance: For any node, the heights of its left and right subtrees differ by at most 1.

• Guaranteed Performance: All operations (search, insert, delete) run in O(log n) time.

⚖️ How Does Balancing Work?

The tree uses four types of rotations to maintain balance:
• Left Rotation: When the right side becomes too heavy
• Right Rotation: When the left side becomes too heavy  
• Left-Right Rotation: Combination for complex imbalances
• Right-Left Rotation: Combination for complex imbalances

🎯 Why Are AVL Trees Important?

1. Consistent Performance: Unlike regular binary search trees that can degrade to O(n) in worst case, AVL trees guarantee O(log n).

2. Real-World Applications:
   • Database indexing systems
   • Memory management in operating systems
   • Symbol tables in compilers
   • Graphics and computational geometry

3. Foundation Knowledge: Understanding AVL trees helps with other balanced trees like Red-Black trees.

🔄 How This Visualizer Works:

• Enter a positive integer in the input field
• If the number exists: it will be DELETED
• If the number doesn't exist: it will be INSERTED
• The tree automatically rebalances after each operation
• Root node is shown in darker blue
• Regular nodes are shown in lighter blue
• Red arrows show parent-child relationships

💡 Try It Out!

Insert numbers like: 10, 5, 15, 3, 7, 12, 18
Watch how the tree stays balanced automatically!

For more advanced algorithms, see CSC6023 course materials.
        """
        
        info_label = ctk.CTkLabel(
            scrollable_frame, 
            text=info_text, 
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=550
        )
        info_label.pack(pady=(0, 15))
        
        # Close button
        close_button = ctk.CTkButton(
            info_window,
            text="Close",
            command=info_window.destroy,
            width=100
        )
        close_button.pack(pady=10)

    def _clear_tree(self):
        """
        Clear all nodes from the tree and update the display.
        
        Resets the tree to an empty state and refreshes the visualization.
        """
        # Close any existing explanation window
        if self.current_explanation_window and self.current_explanation_window.winfo_exists():
            self.current_explanation_window.destroy()
            self.current_explanation_window = None
            
        self.tree = AVLTree()
        self.operation_log = []  # Reset operation tracking
        self.redraw_tree()
        self._update_status("Tree cleared successfully", "success")

    def _print_to_console(self):
        """
        Print the current tree structure to the console.
        
        Useful for debugging and getting a text representation of the tree structure.
        """
        print("\n" + "="*50)
        print("Current AVL Tree Structure:")
        print("="*50)
        self.tree.print_tree()
        print("="*50 + "\n")
        self._update_status("Tree structure printed to console", "info")

    def _zoom_in(self):
        """Zoom in the tree visualization."""
        self.zoom_scale = min(2.0, self.zoom_scale * 1.2)
        self.zoom_label.configure(text=f"{int(self.zoom_scale * 100)}%")
        self.redraw_tree()

    def _zoom_out(self):
        """Zoom out the tree visualization."""
        self.zoom_scale = max(0.5, self.zoom_scale / 1.2)
        self.zoom_label.configure(text=f"{int(self.zoom_scale * 100)}%")
        self.redraw_tree()

    def _zoom_reset(self):
        """Reset zoom to 100%."""
        self.zoom_scale = 1.0
        self.zoom_label.configure(text="100%")
        self.redraw_tree()

    def _update_status(self, message, status_type="info"):
        """
        Update the status bar with a message.
        
        Args:
            message (str): The message to display
            status_type (str): Type of message - "info", "success", "error", or "warning"
        """
        colors = {
            "info": "white",
            "success": "#4BEB4B",  
            "error": "#F51C3D",    
            "warning": "#EE850D"  
        }
        
        self.status_label.configure(text=message, text_color=colors.get(status_type, "white"))

    def handle_input(self, event=None):
        """
        Handle user input for inserting or deleting values.
        
        This method processes the user's input, validates it, and performs
        the appropriate operation (insert if value doesn't exist, delete if it does).
        
        Args:
            event: Optional event parameter (used when called by key binding)
        """
        try:
            # Close any existing explanation window when new input is entered
            if self.current_explanation_window and self.current_explanation_window.winfo_exists():
                self.current_explanation_window.destroy()
                self.current_explanation_window = None
            
            user_input = self.entry.get().strip()
            
            # Validate input
            if not user_input:
                self._update_status("Please enter a number", "warning")
                return
                
            num = int(user_input)
            
            if num <= 0:
                self._update_status("Please enter a positive integer", "warning")
                self.destroy()  # Exit as per original specification
                return
            
            # Reset operation tracking
            self.operation_log = []
            
            # Determine operation based on existence
            if self.tree.contains(num):
                # Track deletion process
                self._track_deletion(num)
                self.tree.delete(num)
                operation = "deleted"
                self._update_status(f"Successfully deleted {num} from the tree", "success")
                self._show_operation_explanation(num, "delete")
            else:
                # Track insertion process
                self._track_insertion(num)
                self.tree.insert(num)
                operation = "inserted"
                self._update_status(f"Successfully inserted {num} into the tree", "success")
                self._show_operation_explanation(num, "insert")
            
            # Update visualization and clear input
            self.redraw_tree()
            self.entry.delete(0, ctk.END)
            
        except ValueError:
            self._update_status(f"'{user_input}' is not a valid integer", "error")
        except Exception as e:
            self._update_status(f"An error occurred: {str(e)}", "error")

    def _track_insertion(self, value):
        """
        Track the insertion process to explain what happens step by step.
        
        Args:
            value (int): The value being inserted
        """
        self.operation_log = []
        
        if not self.tree.root:
            self.operation_log.append(f"🌳 Tree is empty, so {value} becomes the root node.")
            return
        
        # Track the path from root to insertion point
        current = self.tree.root
        path = []
        
        while current:
            path.append(current.data)
            if value < current.data:
                self.operation_log.append(f"📍 {value} < {current.data}, so we go LEFT from {current.data}")
                if not current.left:
                    self.operation_log.append(f"✅ Found empty left position under {current.data}, placing {value} here.")
                    break
                current = current.left
            elif value > current.data:
                self.operation_log.append(f"📍 {value} > {current.data}, so we go RIGHT from {current.data}")
                if not current.right:
                    self.operation_log.append(f"✅ Found empty right position under {current.data}, placing {value} here.")
                    break
                current = current.right
            else:
                self.operation_log.append(f"⚠️ {value} already exists in the tree, no insertion needed.")
                return
        
        self.operation_log.append(f"🔄 After insertion, the tree will check if rebalancing is needed...")
        self.operation_log.append(f"⚖️ AVL property: height difference between left/right subtrees must be ≤ 1")

    def _track_deletion(self, value):
        """
        Track the deletion process to explain what happens step by step.
        
        Args:
            value (int): The value being deleted
        """
        self.operation_log = []
        
        # Find the node to be deleted
        current = self.tree.root
        parent = None
        
        # Track path to the node
        while current and current.data != value:
            parent = current
            if value < current.data:
                self.operation_log.append(f"🔍 Looking for {value}: {value} < {current.data}, go LEFT")
                current = current.left
            else:
                self.operation_log.append(f"🔍 Looking for {value}: {value} > {current.data}, go RIGHT")
                current = current.right
        
        if not current:
            self.operation_log.append(f"❌ {value} not found in tree!")
            return
        
        self.operation_log.append(f"✅ Found {value} in the tree!")
        
        # Analyze deletion case
        if not current.left and not current.right:
            self.operation_log.append(f"📝 Case 1: {value} is a LEAF node (no children)")
            self.operation_log.append(f"🗑️ Simply remove {value} from the tree")
        elif not current.left or not current.right:
            child = current.left if current.left else current.right
            self.operation_log.append(f"📝 Case 2: {value} has ONE child ({child.data})")
            self.operation_log.append(f"🔄 Replace {value} with its child {child.data}")
        else:
            # Find successor
            successor = current.right
            while successor.left:
                successor = successor.left
            self.operation_log.append(f"📝 Case 3: {value} has TWO children")
            self.operation_log.append(f"🔄 Find inorder successor (smallest in right subtree): {successor.data}")
            self.operation_log.append(f"📋 Replace {value} with {successor.data}, then delete the successor")
        
        self.operation_log.append(f"⚖️ After deletion, check AVL balance and rebalance if needed...")

    def _show_operation_explanation(self, value, operation_type):
        """
        Show a popup explaining what happened during the insert/delete operation.
        
        Args:
            value (int): The value that was inserted or deleted
            operation_type (str): Either "insert" or "delete"
        """
        # Create explanation window
        explanation_window = ctk.CTkToplevel(self)
        explanation_window.title(f"AVL Tree Operation: {operation_type.title()} {value}")
        explanation_window.geometry("400x400")
        explanation_window.resizable(True, True)
        
        # Store reference to current window
        self.current_explanation_window = explanation_window
        
        # Make it appear on top but not modal
        explanation_window.transient(self)
        explanation_window.lift()
        explanation_window.focus_set()
        
        # Center the window
        explanation_window.update_idletasks()
        x = (explanation_window.winfo_screenwidth()) - (400 // 2)
        y = (explanation_window.winfo_screenheight() // 2) - (400 // 2)
        explanation_window.geometry(f"400x400+{x}+{y}")
        
        # Handle window closing
        def on_close():
            self.current_explanation_window = None
            explanation_window.destroy()
        
        explanation_window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(explanation_window)
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title
        title_text = f"🔄 {operation_type.title()}ing {value} from AVL Tree"
        title = ctk.CTkLabel(
            scrollable_frame, 
            text=title_text, 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(0, 15))
        
        # Operation explanation
        explanation_text = "\n".join(self.operation_log)
        
        # Add general AVL info
        if operation_type == "insert":
            additional_info = f"""

🎯 Why This Placement?
In a Binary Search Tree (BST), we follow a simple rule:
• If new value < current node → go LEFT
• If new value > current node → go RIGHT
• Place the new node when we find an empty spot

⚖️ AVL Balancing:
After insertion, the tree checks each node's balance factor:
• Balance Factor = Height(Left) - Height(Right)
• If any node has |Balance Factor| > 1, rotations are performed
• This keeps the tree height around log₂(n) for optimal performance

🔄 Possible Rotations:
• Left Rotation: When right side gets too heavy
• Right Rotation: When left side gets too heavy
• Left-Right: Complex case needing two rotations
• Right-Left: Complex case needing two rotations
"""
        else:  # delete
            additional_info = f"""

🗑️ Deletion Strategy:
AVL deletion follows BST rules with three cases:
1. Leaf node: Just remove it
2. One child: Replace node with its child
3. Two children: Replace with inorder successor

🔄 Why Inorder Successor?
The inorder successor is the smallest value in the right subtree.
It's guaranteed to be larger than all left subtree values and smaller
than all other right subtree values, maintaining BST property.

⚖️ Rebalancing After Deletion:
After removing a node, the tree might become unbalanced.
The same rotation rules apply to restore the AVL property.
"""
        
        full_explanation = explanation_text + additional_info
        
        explanation_label = ctk.CTkLabel(
            scrollable_frame, 
            text=full_explanation, 
            font=ctk.CTkFont(size=11),
            justify="left",
            wraplength=460
        )
        explanation_label.pack(pady=(0, 15))
        
        # Add current tree info
        levels = self.tree.get_nodes_by_level()
        tree_height = len(levels) if levels else 0
        node_count = sum(len(level) for level in levels) if levels else 0
        
        tree_stats = f"""
📊 Current Tree Statistics:
• Total Nodes: {node_count}
• Tree Height: {tree_height}
• Theoretical Minimum Height: {max(1, int(__import__('math').log2(node_count + 1))) if node_count > 0 else 0}
• Well Balanced: {'✅ Yes' if tree_height <= max(1, int(1.44 * __import__('math').log2(node_count + 1))) or node_count <= 1 else '❌ No'}
"""
        
        stats_label = ctk.CTkLabel(
            scrollable_frame, 
            text=tree_stats, 
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        stats_label.pack(pady=(10, 15))
        
        # Close button
        close_button = ctk.CTkButton(
            explanation_window,
            text="Got It! Continue →",
            command=on_close,
            width=150,
            height=35
        )
        close_button.pack(pady=15)

    def redraw_tree(self):
        """
        Redraw the entire tree visualization on the canvas.
        
        This method clears the canvas and draws the current state of the tree,
        including all nodes and connections. It calculates positions for nodes
        respecting parent-child relationships.
        """
        self.canvas.delete("all")
        
        if not self.tree.root:
            # Draw empty tree message
            canvas_width = self.canvas.winfo_width() or 850
            canvas_height = self.canvas.winfo_height() or 450
            self.canvas.create_text(
                canvas_width//2 + 150, canvas_height//2 + 50,
                text="Tree is empty\nEnter a positive integer to start",
                fill="white", 
                font=("Arial", 16),
                anchor="center",
                justify="center"
            )
            return

        canvas_width = self.canvas.winfo_width() or 850
        canvas_height = self.canvas.winfo_height() or 450
        
        # Calculate positions using proper tree structure
        positions = {}
        self._calculate_positions(self.tree.root, canvas_width//2, 50, canvas_width//6, positions)

        # Draw connections first (so they appear behind nodes)
        for node, (x1, y1) in positions.items():
            # Calculate scaled radius based on zoom
            node_radius = int(20 * self.zoom_scale)
            line_width = max(1, int(2 * self.zoom_scale))  # Scale line width too
            
            # Helper function to draw arrow from parent to child
            def draw_arrow_to_child(child_node):
                if child_node and child_node in positions:
                    x2, y2 = positions[child_node]
                    
                    # Calculate angle between parent and child
                    dx = x2 - x1
                    dy = y2 - y1
                    angle = math.atan2(dy, dx)
                    
                    # Calculate arrow start point (edge of parent node)
                    start_x = x1 + node_radius * math.cos(angle)
                    start_y = y1 + node_radius * math.sin(angle)
                    
                    # Calculate arrow end point (edge of child node)
                    end_x = x2 - node_radius * math.cos(angle)
                    end_y = y2 - node_radius * math.sin(angle)
                    
                    # Draw the arrow line
                    self.canvas.create_line(
                        start_x, start_y, end_x, end_y, 
                        fill="#ED6942", 
                        width=line_width, 
                        arrow=tk.LAST,
                        arrowshape=(10 * self.zoom_scale, 12 * self.zoom_scale, 5 * self.zoom_scale)
                    )
            
            # Draw arrows to both children
            draw_arrow_to_child(node.left)
            draw_arrow_to_child(node.right)

        # Draw nodes
        for node, (x, y) in positions.items():
            radius = int(20 * self.zoom_scale)  # Scale node radius
            color = "#0a77ca" if node == self.tree.root else "#79baec"
            
            # Draw node circle
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius, 
                fill=color, outline="#2c2c2c", width=2
            )
            
            # Draw node value
            self.canvas.create_text(
                x, y, text=str(node.data), 
                fill="white", font=("Arial", 12, "bold")
            )

    def _calculate_positions(self, node, x, y, x_offset, positions):
        """
        Recursively calculate node positions based on tree structure.
        
        Args:
            node: Current node being positioned
            x: X coordinate for this node
            y: Y coordinate for this node  
            x_offset: Horizontal spacing for children
            positions: Dictionary to store calculated positions
        """
        if not node:
            return
            
        # Apply zoom scale
        scaled_y_offset = 60 * self.zoom_scale  # Changed from 80 to 60
        scaled_x_offset = x_offset * self.zoom_scale
        
        positions[node] = (x, y)
        
        if node.left:
            self._calculate_positions(node.left, x - scaled_x_offset, y + scaled_y_offset, 
                                    scaled_x_offset * 0.6, positions)
        
        if node.right:
            self._calculate_positions(node.right, x + scaled_x_offset, y + scaled_y_offset, 
                                    scaled_x_offset * 0.6, positions)

def main():
    """
    Main entry point for the AVL Tree Visualizer application.
    
    Sets up the CustomTkinter appearance and theme, then launches the
    main visualizer window. The application runs until the user closes
    the window or enters a non-positive integer.
    """
    # Set appearance and theme for modern look
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = TreeVisualizer()
    app.mainloop()


if __name__ == "__main__":
    main()
