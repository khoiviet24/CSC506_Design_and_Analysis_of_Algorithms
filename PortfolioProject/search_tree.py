import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import tkinter.scrolledtext as st
import timeit
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)
_DEBUG = False


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


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.modifications = []

    def insert(self, key):
        self.modifications.append(['Insert', key])
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def delete(self, key):
        self.modifications.append(['Delete', key])
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, root, key, timestamp=False):
        if root is None:
            if not timestamp:
                self.modifications.pop(-1)
                tkinter.messagebox.showinfo("Invalid Value", "Value not found in tree.")
            return root

        if key < root.key:
            root.left = self._delete_recursive(root.left, key, timestamp)
        elif key > root.key:
            root.right = self._delete_recursive(root.right, key, timestamp)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            root.key = self._min_value_node(root.right).key
            root.right = self._delete_recursive(root.right, root.key, timestamp)

        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def snapshot(self, ts=None):
        if _DEBUG:
            print(self.modifications)
        if ts is not None:
            snapshot = self.modifications.copy()[:ts+1]
        else:
            snapshot = self.modifications.copy()
        if _DEBUG and ts != 0:
            print(snapshot)
        processed = []
        for element in snapshot:
            if element[0] == 'Insert':
                processed.append(element[1])
            elif element[0] == 'Delete':
                processed.remove(element[1])
            elif element[0] == 'Delete_Timestamp':
                del processed[element[1]]

        return self._print_snapshot(processed)

    def _print_snapshot(self, temp_list):
        temp_tree = FullyRetroactiveBinarySearchTree()
        for key in temp_list:
            temp_tree.insert(key)

        return temp_tree.root.display()

    def pred(self, x):
        #  Returns the largest element stored in the subtree with values less than or equal to x.
        return self._pred(self.root, x)

    def _pred(self, root, x):
        if root is None:
            return None

        if root.key <= x:
            right_result = self._pred(root.right, x)
            if right_result is not None:
                return right_result
            else:
                return root.key
        else:
            return self._pred(root.left, x)

    def get_modifications(self):
        res = ''
        for i in range(len(self.modifications)):
            res += str(i) + ": " + str(self.modifications[i]) + "\n"

        return res


class PartiallyRetroactiveBinarySearchTree(BinarySearchTree):

    def insert_ago(self, key, tminus):
        self.modifications.insert(len(self.modifications)-tminus, ['Insert', key])
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def delete_timestamp(self, timestamp):
        # If timestamp corresponds to an insert, remove it
        key_to_remove = self.modifications[timestamp][1]
        self.modifications.append(['Delete_Timestamp', timestamp])
        self.root = self._delete_recursive(self.root, key_to_remove, True)


class FullyRetroactiveBinarySearchTree(BinarySearchTree):

    def insert_timestamp(self, key, timestamp):
        if timestamp > len(self.modifications):
            self.modifications.append(['Insert', key])
            tkinter.messagebox.showinfo("Invalid Timestamp", "Timestamp not valid. Inserting at the end.")
        else:
            self.modifications.insert(timestamp, ['Insert', key])
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def delete_timestamp(self, timestamp):
        if timestamp > len(self.modifications):
            tkinter.messagebox.showinfo("Invalid Timestamp", "Timestamp is not valid.")
            return

        # If timestamp corresponds to an insert, remove it
        key_to_remove = self.modifications[timestamp][1]
        self.modifications.append(['Delete_Timestamp', timestamp])
        self.root = self._delete_recursive(self.root, key_to_remove, True)


class RollbackBST(BinarySearchTree):
    def rollback(self, timestamp):
        while len(self.modifications) > timestamp+1:
            operation, key = self.modifications.pop()
            if operation == 'insert':
                self._delete_recursive(self.root, key)
            elif operation == 'delete':
                self._insert_recursives(self.root, key)


class SearchTreeApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1300x900")

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        for F in (StartPage, FullyRetroactiveBinarySearchTreePage, PartiallyRetroactiveBinarySearchTreePage,
                  BinarySearchTreePage, RollbackBSTPage, PerformanceComparisonPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_frame(self, frame_class):
        return self.frames[frame_class]


class FullyRetroactiveBinarySearchTreePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fr_tree = FullyRetroactiveBinarySearchTree()

        label = ttk.Label(self, text="Retroactive Search Tree", font=LARGE_FONT)
        label.place(x=350, y=10)

        def on_entry_click_insert(event):
            if self.insert_entry.get() == "Enter value":
                self.insert_entry.delete(0, tk.END)
                self.insert_entry.config(foreground='black')

        def on_focus_out_insert(event):
            if not self.insert_entry.get():
                self.insert_entry.insert(0, "Enter value")
                self.insert_entry.config(foreground='grey')

        def on_entry_click_insert_ago_val(event):
            if self.insert_ago_val_entry.get() == "Enter value":
                self.insert_ago_val_entry.delete(0, tk.END)
                self.insert_ago_val_entry.config(foreground='black')

        def on_focus_out_insert_ago_val(event):
            if not self.insert_ago_val_entry.get():
                self.insert_ago_val_entry.insert(0, "Enter value")
                self.insert_ago_val_entry.config(foreground='grey')

        def on_entry_click_insert_ago_ts(event):
            if self.insert_ago_ts_entry.get() == "Enter timestamp":
                self.insert_ago_ts_entry.delete(0, tk.END)
                self.insert_ago_ts_entry.config(foreground='black')

        def on_focus_out_insert_ago_ts(event):
            if not self.insert_ago_ts_entry.get():
                self.insert_ago_ts_entry.insert(0, "Enter timestamp")
                self.insert_ago_ts_entry.config(foreground='grey')

        def on_entry_click_delete_ts(event):
            if self.delete_ts_entry.get() == "Enter timestamp":
                self.delete_ts_entry.delete(0, tk.END)
                self.delete_ts_entry.config(foreground='black')

        def on_focus_out_delete_ts(event):
            if not self.delete_ts_entry.get():
                self.delete_ts_entry.insert(0, "Enter timestamp")
                self.delete_ts_entry.config(foreground='grey')

        def on_entry_click_delete(event):
            if self.delete_entry.get() == "Enter value":
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, "Enter value")
                self.delete_entry.config(foreground='grey')

        def on_entry_click_pred(event):
            if self.pred_entry.get() == "Enter value":
                self.pred_entry.delete(0, tk.END)
                self.pred_entry.config(foreground='black')

        def on_focus_out_pred(event):
            if not self.pred_entry.get():
                self.pred_entry.insert(0, "Enter value")
                self.pred_entry.config(foreground='grey')

        def on_entry_click_tree_ts(event):
            if self.tree_ts_entry.get() == "Enter timestamp":
                self.tree_ts_entry.delete(0, tk.END)
                self.tree_ts_entry.config(foreground='black')

        def on_focus_out_tree_ts(event):
            if not self.tree_ts_entry.get():
                self.tree_ts_entry.insert(0, "Enter timestamp")
                self.tree_ts_entry.config(foreground='grey')

        def clear_modifications():
            self.fr_tree.modifications = []
            self.text_area.delete(1.0, tk.END)

        self.modifications_label = ttk.Label(self, text='Modifications', font=REGULAR_FONT)
        self.modifications_label.place(x=700, y=100)
        self.text_area = st.ScrolledText(self, width=40, height=10, font=REGULAR_FONT)
        self.text_area.place(x=700, y=150)
        self.clear_button = ttk.Button(self, text="Clear", command=lambda: clear_modifications())
        self.clear_button.place(x=700, y=400, width=100, height=50)

        default_value_text = "Enter value"
        self.insert_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_entry.insert(0, default_value_text)
        self.insert_entry.bind("<FocusIn>", on_entry_click_insert)
        self.insert_entry.bind("<FocusOut>", on_focus_out_insert)
        self.insert_entry.place(x=50, y=150)
        self.insert_button = ttk.Button(self, text="Insert", command=lambda: get_insert())
        self.insert_button.place(x=50, y=180, width=100, height=50)

        self.insert_ago_val_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_ago_val_entry.insert(0, default_value_text)
        self.insert_ago_val_entry.bind("<FocusIn>", on_entry_click_insert_ago_val)
        self.insert_ago_val_entry.bind("<FocusOut>", on_focus_out_insert_ago_val)
        self.insert_ago_val_entry.place(x=50, y=280)

        default_ts_text = "Enter timestamp"
        self.insert_ago_ts_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_ago_ts_entry.insert(0, default_ts_text)
        self.insert_ago_ts_entry.bind("<FocusIn>", on_entry_click_insert_ago_ts)
        self.insert_ago_ts_entry.bind("<FocusOut>", on_focus_out_insert_ago_ts)
        self.insert_ago_ts_entry.place(x=50, y=310)
        self.insert_ago_button = ttk.Button(self, text="  Insert At \nTimestamp",
                                            command=lambda: get_insert_timestamp())
        self.insert_ago_button.place(x=50, y=340, width=100, height=50)

        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind("<FocusIn>", on_entry_click_delete)
        self.delete_entry.bind("<FocusOut>", on_focus_out_delete)
        self.delete_entry.place(x=50, y=440)
        self.delete_button = ttk.Button(self, text="Delete", command=lambda: get_delete())
        self.delete_button.place(x=50, y=470, width=100, height=50)

        self.delete_ts_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_ts_entry.insert(0, default_ts_text)
        self.delete_ts_entry.bind("<FocusIn>", on_entry_click_delete_ts)
        self.delete_ts_entry.bind("<FocusOut>", on_focus_out_delete_ts)
        self.delete_ts_entry.place(x=50, y=570)
        self.delete_ts_button = ttk.Button(self, text="    Delete \nTimestamp", command=lambda: get_delete_ts())
        self.delete_ts_button.place(x=50, y=600, width=100, height=50)

        self.pred_entry = ttk.Entry(self, width=15, foreground='grey')
        self.pred_entry.insert(0, default_value_text)
        self.pred_entry.bind("<FocusIn>", on_entry_click_pred)
        self.pred_entry.bind("<FocusOut>", on_focus_out_pred)
        self.pred_entry.place(x=250, y=150)
        self.pred_button = ttk.Button(self, text="Find Pred", command=lambda: get_pred())
        self.pred_button.place(x=250, y=180, width=100, height=50)
        self.pred_label = ttk.Label(self, text="", font=REGULAR_FONT)
        self.pred_label.place(x=250, y=250)

        self.tree_ts_entry = ttk.Entry(self, width=15, foreground='grey')
        self.tree_ts_entry.insert(0, default_ts_text)
        self.tree_ts_entry.bind("<FocusIn>", on_entry_click_tree_ts)
        self.tree_ts_entry.bind("<FocusOut>", on_focus_out_tree_ts)
        self.tree_ts_entry.place(x=250, y=570)
        self.tree_ts_button = ttk.Button(self, text="   Show Tree \n At Timestamp", command=lambda: show_tree_at_ts())
        self.tree_ts_button.place(x=250, y=600, width=100, height=50)

        def get_insert():
            try:
                num_to_insert = int(self.insert_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.fr_tree.insert(num_to_insert)
            mod_text = self.fr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_entry.delete(0, tk.END)
            self.insert_entry.config(foreground='grey')
            self.insert_entry.insert(0, default_value_text)

        def get_insert_timestamp():
            try:
                num_to_insert = int(self.insert_ago_val_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            try:
                ts_to_insert = int(self.insert_ago_ts_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid timestamp to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.fr_tree.insert_timestamp(num_to_insert, ts_to_insert)
            mod_text = self.fr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_ago_val_entry.delete(0, tk.END)
            self.insert_ago_val_entry.config(foreground='grey')
            self.insert_ago_val_entry.insert(0, default_value_text)
            self.insert_ago_ts_entry.delete(0, tk.END)
            self.insert_ago_ts_entry.config(foreground='grey')
            self.insert_ago_ts_entry.insert(0, default_ts_text)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.fr_tree.delete(num_to_delete)
            mod_text = self.fr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_delete_ts():
            try:
                ts_to_delete = int(self.delete_ts_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Timestamp",
                                            "Please enter a valid timestamp to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.fr_tree.delete_timestamp(ts_to_delete)
            mod_text = self.fr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_ts_entry.delete(0, tk.END)
            self.delete_ts_entry.config(foreground='grey')
            self.delete_ts_entry.insert(0, default_ts_text)

        def get_pred():
            try:
                num_to_find_pred = int(self.pred_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to find pred.")
                return

            pred_res = self.fr_tree.pred(num_to_find_pred)
            res_str = "The Pred of " + str(num_to_find_pred) + ": " + str(pred_res)
            self.pred_label.config(text=res_str)
            self.pred_entry.delete(0, tk.END)
            self.pred_entry.config(foreground='grey')
            self.pred_entry.insert(0, default_value_text)

        def show_tree_at_ts():
            try:
                tree_ts = int(self.tree_ts_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Timestamp",
                                            "Please enter a valid timestamp.")
                return

            if len(self.fr_tree.modifications) == 0:
                tkinter.messagebox.showinfo("Empty Tree", "No tree to display.")
                return

            top = tk.Toplevel(controller)
            top.geometry("800x800")
            top.title("Fully Retroactive Binary Search Tree At Timestamp " + str(tree_ts))

            tree_text = self.fr_tree.snapshot(tree_ts)

            tree_display = st.ScrolledText(top, width=55, height=30, font=REGULAR_FONT)
            tree_display.place(x=50, y=50)

            tree_display.delete(1.0, tk.END)
            tree_display.insert(tk.INSERT, tree_text)

        def show_tree():
            if len(self.fr_tree.modifications) == 0:
                tkinter.messagebox.showinfo("Empty Tree", "No tree to display.")
                return

            top = tk.Toplevel(controller)
            top.geometry("800x800")
            top.title("Fully Retroactive Binary Search Tree")

            tree_text = self.fr_tree.snapshot()

            tree_display = st.ScrolledText(top, width=55, height=30, font=REGULAR_FONT)
            tree_display.place(x=50, y=50)

            tree_display.delete(1.0, tk.END)
            tree_display.insert(tk.INSERT, tree_text)

        show_tree_button = ttk.Button(self, text="Show Tree", command=lambda: show_tree())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


class PartiallyRetroactiveBinarySearchTreePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pr_tree = PartiallyRetroactiveBinarySearchTree()

        label = ttk.Label(self, text="Partially Retroactive Search Tree", font=LARGE_FONT)
        label.place(x=250, y=10)

        def on_entry_click_insert(event):
            if self.insert_entry.get() == "Enter value":
                self.insert_entry.delete(0, tk.END)
                self.insert_entry.config(foreground='black')

        def on_focus_out_insert(event):
            if not self.insert_entry.get():
                self.insert_entry.insert(0, "Enter value")
                self.insert_entry.config(foreground='grey')

        def on_entry_click_insert_ago_val(event):
            if self.insert_ago_val_entry.get() == "Enter value":
                self.insert_ago_val_entry.delete(0, tk.END)
                self.insert_ago_val_entry.config(foreground='black')

        def on_focus_out_insert_ago_val(event):
            if not self.insert_ago_val_entry.get():
                self.insert_ago_val_entry.insert(0, "Enter value")
                self.insert_ago_val_entry.config(foreground='grey')

        def on_entry_click_insert_ago_ts(event):
            if self.insert_ago_ts_entry.get() == "Enter timestamp":
                self.insert_ago_ts_entry.delete(0, tk.END)
                self.insert_ago_ts_entry.config(foreground='black')

        def on_focus_out_insert_ago_ts(event):
            if not self.insert_ago_ts_entry.get():
                self.insert_ago_ts_entry.insert(0, "Enter timestamp")
                self.insert_ago_ts_entry.config(foreground='grey')

        def on_entry_click_delete_ts(event):
            if self.delete_ts_entry.get() == "Enter timestamp":
                self.delete_ts_entry.delete(0, tk.END)
                self.delete_ts_entry.config(foreground='black')

        def on_focus_out_delete_ts(event):
            if not self.delete_ts_entry.get():
                self.delete_ts_entry.insert(0, "Enter timestamp")
                self.delete_ts_entry.config(foreground='grey')

        def on_entry_click_delete(event):
            if self.delete_entry.get() == "Enter value":
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, "Enter value")
                self.delete_entry.config(foreground='grey')

        def on_entry_click_pred(event):
            if self.pred_entry.get() == "Enter value":
                self.pred_entry.delete(0, tk.END)
                self.pred_entry.config(foreground='black')

        def on_focus_out_pred(event):
            if not self.pred_entry.get():
                self.pred_entry.insert(0, "Enter value")
                self.pred_entry.config(foreground='grey')

        def clear_modifications():
            self.pr_tree.modifications = []
            self.text_area.delete(1.0, tk.END)

        self.modifications_label = ttk.Label(self, text='Modifications', font=REGULAR_FONT)
        self.modifications_label.place(x=700, y=100)
        self.text_area = st.ScrolledText(self, width=40, height=10, font=REGULAR_FONT)
        self.text_area.place(x=700, y=150)
        self.clear_button = ttk.Button(self, text="Clear", command=lambda: clear_modifications())
        self.clear_button.place(x=700, y=400, width=100, height=50)

        default_value_text = "Enter value"
        self.insert_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_entry.insert(0, default_value_text)
        self.insert_entry.bind("<FocusIn>", on_entry_click_insert)
        self.insert_entry.bind("<FocusOut>", on_focus_out_insert)
        self.insert_entry.place(x=50, y=150)
        self.insert_button = ttk.Button(self, text="Insert", command=lambda: get_insert())
        self.insert_button.place(x=50, y=180, width=100, height=50)

        self.insert_ago_val_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_ago_val_entry.insert(0, default_value_text)
        self.insert_ago_val_entry.bind("<FocusIn>", on_entry_click_insert_ago_val)
        self.insert_ago_val_entry.bind("<FocusOut>", on_focus_out_insert_ago_val)
        self.insert_ago_val_entry.place(x=50, y=280)

        default_ts_text = "Enter timestamp"
        self.insert_ago_ts_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_ago_ts_entry.insert(0, default_ts_text)
        self.insert_ago_ts_entry.bind("<FocusIn>", on_entry_click_insert_ago_ts)
        self.insert_ago_ts_entry.bind("<FocusOut>", on_focus_out_insert_ago_ts)
        self.insert_ago_ts_entry.place(x=50, y=310)
        self.insert_ago_button = ttk.Button(self, text="  Insert At \nTimestamp",
                                            command=lambda: get_insert_timestamp())
        self.insert_ago_button.place(x=50, y=340, width=100, height=50)

        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind("<FocusIn>", on_entry_click_delete)
        self.delete_entry.bind("<FocusOut>", on_focus_out_delete)
        self.delete_entry.place(x=50, y=440)
        self.delete_button = ttk.Button(self, text="Delete", command=lambda: get_delete())
        self.delete_button.place(x=50, y=470, width=100, height=50)

        self.delete_ts_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_ts_entry.insert(0, default_ts_text)
        self.delete_ts_entry.bind("<FocusIn>", on_entry_click_delete_ts)
        self.delete_ts_entry.bind("<FocusOut>", on_focus_out_delete_ts)
        self.delete_ts_entry.place(x=50, y=570)
        self.delete_ts_button = ttk.Button(self, text="    Delete \nTimestamp", command=lambda: get_delete_ts())
        self.delete_ts_button.place(x=50, y=600, width=100, height=50)

        self.pred_entry = ttk.Entry(self, width=15, foreground='grey')
        self.pred_entry.insert(0, default_value_text)
        self.pred_entry.bind("<FocusIn>", on_entry_click_pred)
        self.pred_entry.bind("<FocusOut>", on_focus_out_pred)
        self.pred_entry.place(x=250, y=150)
        self.pred_button = ttk.Button(self, text="Find Pred", command=lambda: get_pred())
        self.pred_button.place(x=250, y=180, width=100, height=50)
        self.pred_label = ttk.Label(self, text="", font=REGULAR_FONT)
        self.pred_label.place(x=250, y=250)

        def get_insert():
            try:
                num_to_insert = int(self.insert_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.pr_tree.insert(num_to_insert)
            mod_text = self.pr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_entry.delete(0, tk.END)
            self.insert_entry.config(foreground='grey')
            self.insert_entry.insert(0, default_value_text)

        def get_insert_timestamp():
            try:
                num_to_insert = int(self.insert_ago_val_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            try:
                ts_to_insert = int(self.insert_ago_ts_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid timestamp to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.pr_tree.insert_ago(num_to_insert, ts_to_insert)
            mod_text = self.pr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_ago_val_entry.delete(0, tk.END)
            self.insert_ago_val_entry.config(foreground='grey')
            self.insert_ago_val_entry.insert(0, default_value_text)
            self.insert_ago_ts_entry.delete(0, tk.END)
            self.insert_ago_ts_entry.config(foreground='grey')
            self.insert_ago_ts_entry.insert(0, default_ts_text)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.pr_tree.delete(num_to_delete)
            mod_text = self.pr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_delete_ts():
            try:
                ts_to_delete = int(self.delete_ts_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Timestamp",
                                            "Please enter a valid timestamp to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.pr_tree.delete_timestamp(ts_to_delete)
            mod_text = self.pr_tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_ts_entry.delete(0, tk.END)
            self.delete_ts_entry.config(foreground='grey')
            self.delete_ts_entry.insert(0, default_ts_text)

        def get_pred():
            try:
                num_to_find_pred = int(self.pred_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to find pred.")
                return

            pred_res = self.pr_tree.pred(num_to_find_pred)
            res_str = "The Pred of " + str(num_to_find_pred) + ": " + str(pred_res)
            self.pred_label.config(text=res_str)
            self.pred_entry.delete(0, tk.END)
            self.pred_entry.config(foreground='grey')
            self.pred_entry.insert(0, default_value_text)

        def show_tree():
            if len(self.pr_tree.modifications) == 0:
                tkinter.messagebox.showinfo("Empty Tree", "No tree to display.")
                return

            top = tk.Toplevel(controller)
            top.geometry("800x800")
            top.title("Partially Retroactive Binary Search Tree")

            tree_text = self.pr_tree.snapshot()

            tree_display = st.ScrolledText(top, width=55, height=30, font=REGULAR_FONT)
            tree_display.place(x=50, y=50)

            tree_display.delete(1.0, tk.END)
            tree_display.insert(tk.INSERT, tree_text)

        show_tree_button = ttk.Button(self, text="Show Tree", command=lambda: show_tree())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


class BinarySearchTreePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tree = BinarySearchTree()

        label = ttk.Label(self, text="Binary Search Tree", font=LARGE_FONT)
        label.place(x=420, y=10)

        def on_entry_click_insert(event):
            if self.insert_entry.get() == "Enter value":
                self.insert_entry.delete(0, tk.END)
                self.insert_entry.config(foreground='black')

        def on_focus_out_insert(event):
            if not self.insert_entry.get():
                self.insert_entry.insert(0, "Enter value")
                self.insert_entry.config(foreground='grey')

        def on_entry_click_delete(event):
            if self.delete_entry.get() == "Enter value":
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, "Enter value")
                self.delete_entry.config(foreground='grey')

        def on_entry_click_pred(event):
            if self.pred_entry.get() == "Enter value":
                self.pred_entry.delete(0, tk.END)
                self.pred_entry.config(foreground='black')

        def on_focus_out_pred(event):
            if not self.pred_entry.get():
                self.pred_entry.insert(0, "Enter value")
                self.pred_entry.config(foreground='grey')

        def clear_modifications():
            self.tree.modifications = []
            self.text_area.delete(1.0, tk.END)

        self.modifications_label = ttk.Label(self, text='Modifications', font=REGULAR_FONT)
        self.modifications_label.place(x=700, y=100)
        self.text_area = st.ScrolledText(self, width=40, height=10, font=REGULAR_FONT)
        self.text_area.place(x=700, y=150)
        self.clear_button = ttk.Button(self, text="Clear", command=lambda: clear_modifications())
        self.clear_button.place(x=700, y=400, width=100, height=50)

        default_value_text = "Enter value"
        self.insert_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_entry.insert(0, default_value_text)
        self.insert_entry.bind("<FocusIn>", on_entry_click_insert)
        self.insert_entry.bind("<FocusOut>", on_focus_out_insert)
        self.insert_entry.place(x=50, y=150)
        self.insert_button = ttk.Button(self, text="Insert", command=lambda: get_insert())
        self.insert_button.place(x=50, y=180, width=100, height=50)

        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind("<FocusIn>", on_entry_click_delete)
        self.delete_entry.bind("<FocusOut>", on_focus_out_delete)
        self.delete_entry.place(x=50, y=280)
        self.delete_button = ttk.Button(self, text="Delete", command=lambda: get_delete())
        self.delete_button.place(x=50, y=310, width=100, height=50)

        self.pred_entry = ttk.Entry(self, width=15, foreground='grey')
        self.pred_entry.insert(0, default_value_text)
        self.pred_entry.bind("<FocusIn>", on_entry_click_pred)
        self.pred_entry.bind("<FocusOut>", on_focus_out_pred)
        self.pred_entry.place(x=250, y=150)
        self.pred_button = ttk.Button(self, text="Find Pred", command=lambda: get_pred())
        self.pred_button.place(x=250, y=180, width=100, height=50)
        self.pred_label = ttk.Label(self, text="", font=REGULAR_FONT)
        self.pred_label.place(x=250, y=250)

        def get_insert():
            try:
                num_to_insert = int(self.insert_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.tree.insert(num_to_insert)
            mod_text = self.tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_entry.delete(0, tk.END)
            self.insert_entry.config(foreground='grey')
            self.insert_entry.insert(0, default_value_text)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.tree.delete(num_to_delete)
            mod_text = self.tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_pred():
            try:
                num_to_find_pred = int(self.pred_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to find pred.")
                return

            pred_res = self.tree.pred(num_to_find_pred)
            res_str = "The Pred of " + str(num_to_find_pred) + ": " + str(pred_res)
            self.pred_label.config(text=res_str)
            self.pred_entry.delete(0, tk.END)
            self.pred_entry.config(foreground='grey')
            self.pred_entry.insert(0, default_value_text)

        def show_tree():
            if len(self.tree.modifications) == 0:
                tkinter.messagebox.showinfo("Empty Tree", "No tree to display.")
                return

            top = tk.Toplevel(controller)
            top.geometry("800x800")
            top.title("Binary Search Tree")

            tree_text = self.tree.snapshot()

            tree_display = st.ScrolledText(top, width=55, height=30, font=REGULAR_FONT)
            tree_display.place(x=50, y=50)

            tree_display.delete(1.0, tk.END)
            tree_display.insert(tk.INSERT, tree_text)

        show_tree_button = ttk.Button(self, text="Show Tree", command=lambda: show_tree())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


class RollbackBSTPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.tree = RollbackBST()

        label = ttk.Label(self, text="Rollback Binary Search Tree", font=LARGE_FONT)
        label.place(x=350, y=10)

        def on_entry_click_insert(event):
            if self.insert_entry.get() == "Enter value":
                self.insert_entry.delete(0, tk.END)
                self.insert_entry.config(foreground='black')

        def on_focus_out_insert(event):
            if not self.insert_entry.get():
                self.insert_entry.insert(0, "Enter value")
                self.insert_entry.config(foreground='grey')

        def on_entry_click_delete(event):
            if self.delete_entry.get() == "Enter value":
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, "Enter value")
                self.delete_entry.config(foreground='grey')

        def on_entry_click_rollback(event):
            if self.rollback_entry.get() == "Enter value":
                self.rollback_entry.delete(0, tk.END)
                self.rollback_entry.config(foreground='black')

        def on_focus_out_rollback(event):
            if not self.rollback_entry.get():
                self.rollback_entry.insert(0, "Enter value")
                self.rollback_entry.config(foreground='grey')

        def on_entry_click_pred(event):
            if self.pred_entry.get() == "Enter value":
                self.pred_entry.delete(0, tk.END)
                self.pred_entry.config(foreground='black')

        def on_focus_out_pred(event):
            if not self.pred_entry.get():
                self.pred_entry.insert(0, "Enter value")
                self.pred_entry.config(foreground='grey')

        def clear_modifications():
            self.tree.modifications = []
            self.text_area.delete(1.0, tk.END)

        self.modifications_label = ttk.Label(self, text='Modifications', font=REGULAR_FONT)
        self.modifications_label.place(x=700, y=100)
        self.text_area = st.ScrolledText(self, width=40, height=10, font=REGULAR_FONT)
        self.text_area.place(x=700, y=150)
        self.clear_button = ttk.Button(self, text="Clear", command=lambda: clear_modifications())
        self.clear_button.place(x=700, y=400, width=100, height=50)

        default_value_text = "Enter value"
        self.insert_entry = ttk.Entry(self, width=15, foreground='grey')
        self.insert_entry.insert(0, default_value_text)
        self.insert_entry.bind("<FocusIn>", on_entry_click_insert)
        self.insert_entry.bind("<FocusOut>", on_focus_out_insert)
        self.insert_entry.place(x=50, y=150)
        self.insert_button = ttk.Button(self, text="Insert", command=lambda: get_insert())
        self.insert_button.place(x=50, y=180, width=100, height=50)

        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind("<FocusIn>", on_entry_click_delete)
        self.delete_entry.bind("<FocusOut>", on_focus_out_delete)
        self.delete_entry.place(x=50, y=280)
        self.delete_button = ttk.Button(self, text="Delete", command=lambda: get_delete())
        self.delete_button.place(x=50, y=310, width=100, height=50)

        self.rollback_entry = ttk.Entry(self, width=15, foreground='grey')
        self.rollback_entry.insert(0, default_value_text)
        self.rollback_entry.bind("<FocusIn>", on_entry_click_rollback)
        self.rollback_entry.bind("<FocusOut>", on_focus_out_rollback)
        self.rollback_entry.place(x=50, y=410)
        self.rollback_button = ttk.Button(self, text="Rollback", command=lambda: get_rollback())
        self.rollback_button.place(x=50, y=440, width=100, height=50)

        self.pred_entry = ttk.Entry(self, width=15, foreground='grey')
        self.pred_entry.insert(0, default_value_text)
        self.pred_entry.bind("<FocusIn>", on_entry_click_pred)
        self.pred_entry.bind("<FocusOut>", on_focus_out_pred)
        self.pred_entry.place(x=250, y=150)
        self.pred_button = ttk.Button(self, text="Find Pred", command=lambda: get_pred())
        self.pred_button.place(x=250, y=180, width=100, height=50)
        self.pred_label = ttk.Label(self, text="", font=REGULAR_FONT)
        self.pred_label.place(x=250, y=250)

        def get_insert():
            try:
                num_to_insert = int(self.insert_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to insert.")
                return

            self.text_area.delete(1.0, tk.END)
            self.tree.insert(num_to_insert)
            mod_text = self.tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.insert_entry.delete(0, tk.END)
            self.insert_entry.config(foreground='grey')
            self.insert_entry.insert(0, default_value_text)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to delete.")
                return

            self.text_area.delete(1.0, tk.END)
            self.tree.delete(num_to_delete)
            mod_text = self.tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_rollback():
            try:
                rollback_ts = int(self.rollback_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to rollback.")
                return

            self.text_area.delete(1.0, tk.END)
            self.tree.rollback(rollback_ts)
            mod_text = self.tree.get_modifications()
            self.text_area.insert(tk.INSERT, mod_text)
            self.rollback_entry.delete(0, tk.END)
            self.rollback_entry.config(foreground='grey')
            self.rollback_entry.insert(0, default_value_text)

        def get_pred():
            try:
                num_to_find_pred = int(self.pred_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Number", "Please enter a valid number to find pred.")
                return

            pred_res = self.tree.pred(num_to_find_pred)
            res_str = "The Pred of " + str(num_to_find_pred) + ": " + str(pred_res)
            self.pred_label.config(text=res_str)
            self.pred_entry.delete(0, tk.END)
            self.pred_entry.config(foreground='grey')
            self.pred_entry.insert(0, default_value_text)

        def show_tree():
            if len(self.tree.modifications) == 0:
                tkinter.messagebox.showinfo("Empty Tree", "No tree to display.")
                return

            top = tk.Toplevel(controller)
            top.geometry("800x800")
            top.title("Rollback Binary Search Tree")

            tree_text = self.tree.snapshot()

            tree_display = st.ScrolledText(top, width=55, height=30, font=REGULAR_FONT)
            tree_display.place(x=50, y=50)

            tree_display.delete(1.0, tk.END)
            tree_display.insert(tk.INSERT, tree_text)

        show_tree_button = ttk.Button(self, text="Show Tree", command=lambda: show_tree())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


class PerformanceComparisonPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.num_trials = 100
        self.num_elements = 500
        self.keys = [random.randint(1, 1000) for element in range(self.num_elements)]

        label = ttk.Label(self, text="Performance Comparison", font=LARGE_FONT)
        label.place(x=350, y=10)

        self.rollback_results_label = ttk.Label(self, text='Rollback Results', font=REGULAR_FONT)
        self.rollback_results_label.place(x=50, y=100)
        self.rollback_results_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.rollback_results_text.place(x=50, y=150)

        self.rollback_stats_label = ttk.Label(self, text='Rollback Statistical Analysis', font=REGULAR_FONT)
        self.rollback_stats_label.place(x=50, y=250)
        self.rollback_stats_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.rollback_stats_text.place(x=50, y=300)

        self.insert_results_label = ttk.Label(self, text='Insert Results', font=REGULAR_FONT)
        self.insert_results_label.place(x=50, y=400)
        self.insert_results_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.insert_results_text.place(x=50, y=450)

        self.insert_stats_label = ttk.Label(self, text='Insert Statistical Analysis', font=REGULAR_FONT)
        self.insert_stats_label.place(x=50, y=550)
        self.insert_stats_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.insert_stats_text.place(x=50, y=600)

        def time_pr_bst_insert():
            pr_bst_times = []
            temp_pr_bst = PartiallyRetroactiveBinarySearchTree()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_pr_bst.insert(key)
                end_time = time.time_ns()

                pr_bst_times.append(end_time - start_time)

            return pr_bst_times

        def time_fr_bst_insert():
            fr_bst_times = []
            temp_fr_bst = FullyRetroactiveBinarySearchTree()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_fr_bst.insert(key)
                end_time = time.time_ns()

                fr_bst_times.append(end_time - start_time)

            return fr_bst_times

        def time_rollback_bst_insert():
            rollback_bst_times = []
            temp_rollback_bst = RollbackBST()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_rollback_bst.insert(key)
                end_time = time.time_ns()

                rollback_bst_times.append(end_time - start_time)

            return rollback_bst_times

        def show_bst_times_insert():
            pr_bst_times = time_pr_bst_insert()
            fr_bst_times = time_fr_bst_insert()
            rollback_bst_times = time_rollback_bst_insert()

            median_bst = np.median(rollback_bst_times) / 10000000
            median_pr_bst = np.median(pr_bst_times) / 10000000
            median_fr_bst = np.median(fr_bst_times) / 10000000

            str_result = ('Average FR_BST: ' + str(median_fr_bst) + ' ns\n' + 'Average PR_BST: ' +
                          str(median_pr_bst) + ' ns\n' + 'Average BST     : ' + str(median_bst) + ' ns')
            self.insert_results_text.config(text=str_result)

            f_statistic, p_value = f_oneway(rollback_bst_times, pr_bst_times, fr_bst_times)
            alpha = 0.05
            stat_res_str = ""
            if p_value < alpha:
                stat_res_str += "The p_value is " + str(p_value) + "\n"
                stat_res_str += "The differences in means are statistically significant (reject null hypothesis)."
            else:
                stat_res_str += "The p_value is " + str(p_value) + "\n"
                stat_res_str += ("The differences in means are not statistically significant "
                                 "(fail to reject null hypothesis).")

            self.insert_stats_text.config(text=stat_res_str)

            plt.figure(figsize=(8, 6))
            plt.boxplot([rollback_bst_times, pr_bst_times, fr_bst_times], vert=False, labels=
            ['Rollback BST', 'Partially Retroactive BST', 'Fully Retroactive BST'])
            plt.title(f"Time to Create BST ({self.num_elements} elements, {self.num_trials} trials)")
            plt.xlabel("Time (ns)")
            plt.ylabel("Data Structure")
            plt.show()

        def time_bst_rollback():
            bst_times = []
            temp_bst = RollbackBST()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_bst.insert(key)

                temp_bst.rollback(200)
                end_time = time.time_ns()

                bst_times.append(end_time - start_time)

            return bst_times

        def time_pr_bst_rollback():
            pr_bst_times = []
            temp_pr_bst = PartiallyRetroactiveBinarySearchTree()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_pr_bst.insert(key)

                temp_tree = temp_pr_bst.snapshot(200)
                end_time = time.time_ns()

                pr_bst_times.append(end_time - start_time)

            return pr_bst_times

        def time_fr_bst_rollback():
            fr_bst_times = []
            temp_fr_bst = FullyRetroactiveBinarySearchTree()
            for trial in range(self.num_trials):
                start_time = time.time_ns()
                for key in self.keys:
                    temp_fr_bst.insert(key)

                temp_tree = temp_fr_bst.snapshot(200)
                end_time = time.time_ns()

                fr_bst_times.append(end_time - start_time)

            return fr_bst_times

        def show_bst_times_revert():
            bst_times = time_bst_rollback()
            pr_bst_times = time_pr_bst_rollback()
            fr_bst_times = time_fr_bst_rollback()

            median_bst = np.median(bst_times) / 10000000
            median_pr_bst = np.median(pr_bst_times) / 10000000
            median_fr_bst = np.median(fr_bst_times) / 10000000

            str_result = ('Average FR_BST: ' + str(median_fr_bst) + ' ns\n' + 'Average PR_BST: ' +
                          str(median_pr_bst) + ' ns\n' + 'Average BST     : ' + str(median_bst) + ' ns')
            self.rollback_results_text.config(text=str_result)

            f_statistic, p_value = f_oneway(bst_times, pr_bst_times, fr_bst_times)
            alpha = 0.05
            stat_res_str = ""
            if p_value < alpha:
                stat_res_str += "The p_value is " + str(p_value) + "\n"
                stat_res_str += "The differences in means are statistically significant (reject null hypothesis)."
            else:
                stat_res_str += "The p_value is " + str(p_value) + "\n"
                stat_res_str += ("The differences in means are not statistically significant "
                                "(fail to reject null hypothesis).")

            self.rollback_stats_text.config(text=stat_res_str)

            plt.figure(figsize=(8, 6))
            plt.boxplot([bst_times, pr_bst_times, fr_bst_times], vert=False, labels=
            ['Rollback BST', 'Partially Retroactive BST', 'Fully Retroactive BST'])
            plt.title(f"Time to Create BST ({self.num_elements} elements, {self.num_trials} trials, rollback 200)")
            plt.xlabel("Time (ns)")
            plt.ylabel("Data Structure")
            plt.show()

        show_rollback_button = ttk.Button(self, text="    Rollback \nComparison",
                                          command=lambda: show_bst_times_revert())
        show_rollback_button.place(x=50, y=700, width=100, height=50)
        show_tree_button = ttk.Button(self, text="      Insert \nComparison", command=lambda: show_bst_times_insert())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Portfolio Project", font=LARGE_FONT)
        label.place(x=460, y=10)

        fr_button = ttk.Button(self, text="Fully Retroactive",
                               command=lambda: controller.show_frame(FullyRetroactiveBinarySearchTreePage))
        fr_button.place(x=550, y=200, width=200, height=50)

        pr_button = ttk.Button(self, text="Partially Retroactive",
                               command=lambda: controller.show_frame(PartiallyRetroactiveBinarySearchTreePage))
        pr_button.place(x=550, y=300, width=200, height=50)

        bst_button = ttk.Button(self, text="Binary Search Tree",
                               command=lambda: controller.show_frame(BinarySearchTreePage))
        bst_button.place(x=550, y=400, width=200, height=50)

        rbst_button = ttk.Button(self, text="Rollback Binary Search Tree",
                                command=lambda: controller.show_frame(RollbackBSTPage))
        rbst_button.place(x=550, y=500, width=200, height=50)

        compare_button = ttk.Button(self, text="Performance Comparison",
                                 command=lambda: controller.show_frame(PerformanceComparisonPage))
        compare_button.place(x=550, y=600, width=200, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=550, y=700, width=200, height=50)


# main
def main():
    app = SearchTreeApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
