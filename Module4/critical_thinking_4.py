import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import tkinter.scrolledtext as st

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class OrderedVsUnorderedListApp(tk.Tk):

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


class BaseList:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        if item not in self.items:
            tkinter.messagebox.showinfo("Invalid Delete", str(item) + " is not in the list")
            return
        self.items.remove(item)

    def search(self, item):
        if item in self.items:
            return self.items.index(item)
        else:
            return -1

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

    def print(self):
        res = ""
        for i in range(len(self.items)):
            res += str(i) + ": " + str(self.items[i]) + "\n"

        return res


class UnorderedList(BaseList):
    # No need to override methods, as unordered list uses the same methods as BaseList
    pass


class OrderedList(BaseList):
    def add(self, item):
        # Override add method to maintain order
        low = 0
        high = len(self.items) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.items[mid] < item:
                low = mid + 1
            else:
                high = mid - 1

        self.items.insert(low, item)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.unordered_list = UnorderedList()
        self.ordered_list = OrderedList()

        label = ttk.Label(self, text="Unordered and Ordered Lists", font=LARGE_FONT)
        label.place(x=100, y=10)

        def on_entry_click_add(event):
            if self.add_entry.get() == 'Enter value':
                self.add_entry.delete(0, tk.END)
                self.add_entry.config(foreground='black')

        def on_focus_out_add(event):
            if not self.add_entry.get():
                self.add_entry.insert(0, 'Enter value')
                self.add_entry.config(foreground='grey')

        def on_entry_click_delete(event):
            if self.delete_entry.get() == 'Enter value':
                self.delete_entry.delete(0, tk.END)
                self.delete_entry.config(foreground='black')

        def on_focus_out_delete(event):
            if not self.delete_entry.get():
                self.delete_entry.insert(0, 'Enter value')
                self.delete_entry.config(foreground='grey')

        def on_entry_click_search(event):
            if self.search_entry.get() == 'Enter value':
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(foreground='black')

        def on_focus_out_search(event):
            if not self.search_entry.get():
                self.search_entry.insert(0, 'Enter value')
                self.search_entry.config(foreground='grey')

        self.unordered_label = ttk.Label(self, text='Unordered List', font=REGULAR_FONT)
        self.unordered_label.place(x=200, y=100)
        self.unordered_text_area = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.unordered_text_area.place(x=200, y=150)

        self.ordered_label = ttk.Label(self, text='Ordered List', font=REGULAR_FONT)
        self.ordered_label.place(x=425, y=100)
        self.ordered_text_area = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.ordered_text_area.place(x=425, y=150)

        default_value_text = "Enter value"
        self.add_entry = ttk.Entry(self, width=15, foreground='grey')
        self.add_entry.insert(0, default_value_text)
        self.add_entry.bind('<FocusIn>', on_entry_click_add)
        self.add_entry.bind('<FocusOut>', on_focus_out_add)
        self.add_entry.place(x=50, y=150)
        self.add_button = ttk.Button(self, text='Add', command=lambda: get_add())
        self.add_button.place(x=50, y=180, width=100, height=50)

        self.delete_entry = ttk.Entry(self, width=15, foreground='grey')
        self.delete_entry.insert(0, default_value_text)
        self.delete_entry.bind('<FocusIn>', on_entry_click_delete)
        self.delete_entry.bind('<FocusOut>', on_focus_out_delete)
        self.delete_entry.place(x=50, y=280)
        self.delete_button = ttk.Button(self, text='Delete', command=lambda: get_delete())
        self.delete_button.place(x=50, y=310, width=100, height=50)

        self.search_entry = ttk.Entry(self, width=15, foreground='grey')
        self.search_entry.insert(0, default_value_text)
        self.search_entry.bind('<FocusIn>', on_entry_click_search)
        self.search_entry.bind('<FocusOut>', on_focus_out_search)
        self.search_entry.place(x=50, y=410)
        self.search_button = ttk.Button(self, text='Search', command=lambda: get_search())
        self.search_button.place(x=50, y=440, width=100, height=50)

        self.search_output_label = ttk.Label(self, text='', font=REGULAR_FONT)
        self.search_output_label.place(x=50, y=500)

        def get_add():
            try:
                num_to_add = int(self.add_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Add Value", "Please enter a valid number to add.")
                return

            self.unordered_list.add(num_to_add)
            self.unordered_text_area.delete(1.0, tk.END)
            self.unordered_text_area.insert(tk.INSERT, self.unordered_list.print())

            self.ordered_list.add(num_to_add)
            self.ordered_text_area.delete(1.0, tk.END)
            self.ordered_text_area.insert(tk.INSERT, self.ordered_list.print())

            self.add_entry.delete(0, tk.END)
            self.add_entry.config(foreground='grey')
            self.add_entry.insert(0, default_value_text)

        def get_delete():
            try:
                num_to_delete = int(self.delete_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Delete Value",
                                            "Please enter a valid number to delete.")
                return

            self.unordered_list.remove(num_to_delete)
            self.unordered_text_area.delete(1.0, tk.END)
            self.unordered_text_area.insert(tk.INSERT, self.unordered_list.print())

            self.ordered_list.remove(num_to_delete)
            self.ordered_text_area.delete(1.0, tk.END)
            self.ordered_text_area.insert(tk.INSERT, self.ordered_list.print())

            self.delete_entry.delete(0, tk.END)
            self.delete_entry.config(foreground='grey')
            self.delete_entry.insert(0, default_value_text)

        def get_search():
            try:
                num_to_search = int(self.search_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Invalid Search Value",
                                            "Please enter a valid number to search.")
                return

            unordered_index = self.unordered_list.search(num_to_search)
            ordered_index = self.ordered_list.search(num_to_search)
            res_str = ''

            if unordered_index == -1:
                res_str += str(num_to_search) + " is not in the list."
                self.search_output_label.config(text=res_str)
            else:
                res_str += str(num_to_search) + " is at index " + str(unordered_index) + " in the unordered list.\n"
                res_str += str(num_to_search) + " is at index " + str(ordered_index) + " in the ordered list.\n"
                self.search_output_label.config(text=res_str)

            self.unordered_text_area.delete(1.0, tk.END)
            self.unordered_text_area.insert(tk.INSERT, self.unordered_list.print())

            self.ordered_text_area.delete(1.0, tk.END)
            self.ordered_text_area.insert(tk.INSERT, self.ordered_list.print())

            self.search_entry.delete(0, tk.END)
            self.search_entry.config(foreground='grey')
            self.search_entry.insert(0, default_value_text)

        def clear_all():
            self.unordered_list = []
            self.ordered_list = []
            self.unordered_text_area.delete(1.0, tk.END)
            self.ordered_text_area.delete(1.0, tk.END)
            self.search_output_label.config(text='')

        clear_button = ttk.Button(self, text="Clear Lists", command=lambda: clear_all())
        clear_button.place(x=200, y=400, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=750, y=520, width=100, height=50)


# main
def main():
    app = OrderedVsUnorderedListApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
