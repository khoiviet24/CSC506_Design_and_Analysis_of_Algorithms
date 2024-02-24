import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import tkinter.scrolledtext as st

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def display(self):
        lines, *_ = self._display_aux()
        res=""
        for line in lines:
            print(line)
            res += " " + line + "\n"

        return res

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

class MinHeapApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("900x600")

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_frame(self, frame_class):
        return self.frames[frame_class]


class MinHeap:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """
        Insert a value into the heap while maintaining the heap property.
        """
        if not self.root:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)
            self._heapify_up(key)

    def _insert_recursive(self, current_node, key):
        if not current_node.left:
            current_node.left = Node(key)
        elif not current_node.right:
            current_node.right = Node(key)
        else:
            # Traverse down the tree using a breadth-first approach to find the next available position
            queue = [current_node.left, current_node.right]
            while queue:
                node = queue.pop(0)
                if not node.left:
                    node.left = Node(key)
                    return
                elif not node.right:
                    node.right = Node(key)
                    return
                else:
                    queue.append(node.left)
                    queue.append(node.right)

    def _heapify_up(self, key):
        """
        Restore heap property by percolating up.
        """
        current_node = self._find_node(self.root, key)
        while current_node:
            parent_node = self._find_parent(self.root, key)
            if parent_node and current_node.key < parent_node.key:
                current_node.key, parent_node.key = parent_node.key, current_node.key
                current_node = parent_node
            else:
                break

    def _find_node(self, current_node, key):
        """
        Find the node with the given key in the tree.
        """
        if not current_node:
            return None
        if current_node.key == key:
            return current_node
        left_node = self._find_node(current_node.left, key)
        right_node = self._find_node(current_node.right, key)
        return left_node or right_node

    def _find_parent(self, current_node, key):
        """
        Find the parent node of the node with the given key in the tree.
        """
        if not current_node:
            return None
        if (current_node.left and current_node.left.key == key) or (current_node.right and current_node.right.key == key):
            return current_node
        parent_left = self._find_parent(current_node.left, key)
        parent_right = self._find_parent(current_node.right, key)
        return parent_left or parent_right

    def extract_min(self):
        """
        Extract the minimum value from the heap while maintaining the heap property.
        """
        if not self.root:
            return None

        min_key = self.root.key

        # Find the rightmost leaf node at the deepest level
        last_node = None
        queue = [self.root]
        while queue:
            current_node = queue.pop(0)
            last_node = current_node
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        # Replace the root key with the key of the rightmost leaf node
        self.root.key = last_node.key

        # Remove the rightmost leaf node
        self._remove_rightmost_leaf(self.root, last_node)

        # Restore heap property
        self._heapify_down(self.root)

        return min_key

    def _remove_rightmost_leaf(self, current_node, target_node):
        if not current_node:
            return
        if current_node.left == target_node:
            current_node.left = None
            return
        if current_node.right == target_node:
            current_node.right = None
            return
        self._remove_rightmost_leaf(current_node.left, target_node)
        self._remove_rightmost_leaf(current_node.right, target_node)

    def _heapify_down(self, current_node):
        """
        Restore heap property by percolating down.
        """
        if not current_node:
            return

        left_child = current_node.left
        right_child = current_node.right
        smallest = current_node

        if left_child and left_child.key < smallest.key:
            smallest = left_child
        if right_child and right_child.key < smallest.key:
            smallest = right_child

        if smallest != current_node:
            current_node.key, smallest.key = smallest.key, current_node.key
            self._heapify_down(smallest)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.ordered_array = [25, 44, 55, 99, 30, 37, 15, 2, 4]
        self.ordered_array_copy = self.ordered_array.copy()
        array_to_str = ', '.join([str(elem) for elem in self.ordered_array])
        self.min_heap = MinHeap()

        label = ttk.Label(self, text="Min Heap", font=LARGE_FONT)
        label.place(x=350, y=10)

        self.ordered_array_label = ttk.Label(self, text='Ordered Array', font=REGULAR_FONT)
        self.ordered_array_label.place(x=50, y=100)
        self.ordered_array_text = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.ordered_array_text.insert(tk.INSERT, array_to_str)
        self.ordered_array_text.place(x=50, y=150)

        self.min_heap_label = ttk.Label(self, text='Min Heap', font=REGULAR_FONT)
        self.min_heap_label.place(x=275, y=100)
        self.min_heap_text = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.min_heap_text.place(x=275, y=150)

        def step_heap():
            if not self.ordered_array_copy:
                tkinter.messagebox.showinfo("Empty Array", "No more values to insert into heap.")
                return

            self.min_heap_text.delete(1.0, tk.END)
            self.ordered_array_text.delete(1.0, tk.END)
            val_to_insert = self.ordered_array_copy.pop(0)
            new_array_to_str = ', '.join([str(elem) for elem in self.ordered_array_copy])
            self.min_heap.insert(val_to_insert)
            min_heap_display = self.min_heap.root.display()
            self.min_heap_text.insert(tk.INSERT, min_heap_display)
            self.ordered_array_text.insert(tk.INSERT, new_array_to_str)

        step_button = ttk.Button(self, text="Step", command=lambda: step_heap())
        step_button.place(x=50, y=520, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=750, y=520, width=100, height=50)


# main
def main():
    app = MinHeapApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
