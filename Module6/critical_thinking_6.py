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
        self.height = 1

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


class AVLTreeApp(tk.Tk):

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


class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursively(self.root, key)

    def _insert_recursively(self, node, key):
        if not node:
            return Node(key)

        if key == node.key:
            return node
        elif key < node.key:
            node.left = self._insert_recursively(node.left, key)
        else:
            node.right = self._insert_recursively(node.right, key)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        # Left-Left Case
        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)

        # Right-Right Case
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)

        # Left-Right Case
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Left Case
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, key):
        self.root = self._delete_recursively(self.root, key)

    def _delete_recursively(self, node, key):
        if not node:
            tkinter.messagebox.showinfo("Invalid Delete", "Value is not in the input array.")
            return

        if key < node.key:
            node.left = self._delete_recursively(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursively(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                # Node with two children: Get the inorder successor (smallest in the right subtree)
                successor = self._get_min_value_node(node.right)
                # Copy the inorder successor's content to this node
                node.key = successor.key
                # Delete the inorder successor
                node.right = self._delete_recursively(node.right, successor.key)

        if not node:
            return node  # If the tree had only one node, return

        # Update height of current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check if node is unbalanced
        balance = self._get_balance(node)

        # Left-Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        # Right-Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        # Left-Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right-Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def inorder_traversal(self, node):
        if node:
            self.inorder_traversal(node.left)
            # print(node.key, end=' ')
            self.inorder_traversal(node.right)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.array = [1, 7, 4, 23, 8, 9, 4, 3, 5, 7, 9, 67, 6345, 324]
        array_to_str = ', '.join([str(elem) for elem in self.array])

        def on_entry_click_delete(event):
            if self.delete_entry.get() == 'Enter value':
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, 'Enter value')
                self.delete_entry.config(foreground='grey')

        def on_entry_click_insert(event):
            if self.insert_entry.get() == 'Enter value':
                self.insert_entry.delete(0, tk.END)
                self.insert_entry.config(foreground='black')

        def on_focus_out_insert(event):
            if not self.insert_entry.get():
                self.insert_entry.insert(0, 'Enter value')
                self.insert_entry.config(foreground='grey')

        label = ttk.Label(self, text="AVL Tree", font=LARGE_FONT)
        label.place(x=350, y=10)

        self.array_label = ttk.Label(self, text='Input Array', font=REGULAR_FONT)
        self.array_label.place(x=50, y=100)
        self.array_text = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.array_text.insert(tk.INSERT, array_to_str)
        self.array_text.place(x=50, y=150)

        self.avl_label = ttk.Label(self, text='AVL', font=REGULAR_FONT)
        self.avl_label.place(x=275, y=100)
        self.avl_text = st.ScrolledText(self, width=25, height=10, font=REGULAR_FONT)
        self.avl_text.place(x=275, y=150)

        default_value_text = "Enter value"
        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind('<FocusIn>', on_entry_click_delete)
        self.delete_entry.bind('<FocusOut>', on_focus_out_delete)
        self.delete_entry.place(x=200, y=400)
        self.delete_button = ttk.Button(self, text='Delete', command=lambda: get_delete())
        self.delete_button.place(x=200, y=430, width=100, height=50)

        self.insert_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_entry.insert(0, default_value_text)
        self.insert_entry.bind('<FocusIn>', on_entry_click_insert)
        self.insert_entry.bind('<FocusOut>', on_focus_out_insert)
        self.insert_entry.place(x=50, y=400)
        self.insert_button = ttk.Button(self, text='Insert', command=lambda: get_insert())
        self.insert_button.place(x=50, y=430, width=100, height=50)

        def generate_avl():
            self.avl_text.delete(1.0, tk.END)
            array_to_avl_text = self.array_text.get('1.0', tk.END)
            print(array_to_avl_text)
            if not array_to_avl_text:
                tkinter.messagebox.showinfo("Empty Array", "No more values to insert into AVL.")
                return
            avl_nums = array_to_avl_text.split(', ')
            avl_array = [int(num) for num in avl_nums]

            avl = AVLTree()

            for num in avl_array:
                avl.insert(num)

            avl_display = avl.root.display()
            self.avl_text.insert(tk.INSERT, avl_display)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Delete Value",
                                            "Please enter a valid number to delete.")
                return

            try:
                self.array.remove(num_to_delete)
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Delete", "Value is not in the input array.")
                return
            new_array_to_str = ', '.join([str(elem) for elem in self.array])
            self.array_text.delete(1.0, tk.END)
            self.array_text.insert(tk.INSERT, new_array_to_str)

            generate_avl()

            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_insert():
            try:
                num_to_insert = int(self.insert_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Insert Value", "Please enter a valid number to insert.")
                return

            self.array.append(num_to_insert)
            new_array_to_str = ', '.join([str(elem) for elem in self.array])
            self.array_text.delete(1.0, tk.END)
            self.array_text.insert(tk.INSERT, new_array_to_str)

            generate_avl()

            self.insert_entry.delete(0, tk.END)
            self.insert_entry.config(foreground='grey')
            self.insert_entry.insert(0, default_value_text)

        generate_button = ttk.Button(self, text="Generate AVL", command=lambda: generate_avl())
        generate_button.place(x=50, y=520, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=750, y=520, width=100, height=50)


# main
def main():
    app = AVLTreeApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
