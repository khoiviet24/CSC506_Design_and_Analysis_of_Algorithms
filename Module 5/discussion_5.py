import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import random
import timeit
import matplotlib.pyplot as plt

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class HashTable:
    def __init__(self):
        self.size = 0
        self.table = []

    def hash_function(self, key):
        return hash(key) % self.size

    def set_size(self, size):
        self.size = size
        self.table = [None] * size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            self.table[index].append((key, value))

    def get(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def __str__(self):
        result = ""
        for bucket in self.table:
            if bucket is not None:
                for key, value in bucket:
                    result += f"Student ID: {key}, Name: {value}\n"
        return result


class HashDictSetComparisonApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x600")

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.student_data = [(12345, 'John Smith'), (67890, 'Jane Doe'), (54321, 'Alice Johnson'),
                             (98765, 'Bob Williams'), (24680, 'Eve Brown'), (13579, 'Charlie Davis'),
                             (11223, 'Grace Wilson'), (44556, 'David Lee'), (99999, 'Olivia Martinez'),
                             (77777, 'Sophia Anderson')]
        self.student_dict = {}
        self.student_set = set()
        self.student_hash = HashTable()

        label = ttk.Label(self, text="Hash and Dictionary Comparison", font=LARGE_FONT)
        label.place(x=100, y=10)

        self.results_label = ttk.Label(self, text='Results', font=REGULAR_FONT)
        self.results_label.place(x=50, y=100)
        self.output_label = ttk.Label(self, text='', font=REGULAR_FONT)
        self.output_label.place(x=50, y=130)

        def fill_dict():
            self.student_dict = {student_id: name for student_id, name in self.student_data}

        def print_dict():
            print("\nRetrieving data from dictionary:")
            for student_id, name in self.student_dict.items():
                print('Student ID: ' + str(student_id) + ', Name: ' + str(name))

        def fill_hash():
            self.student_hash.set_size(len(self.student_data) * 2)
            for student_id, name in self.student_data:
                self.student_hash.insert(student_id, name)

        def print_hash():
            print("\nRetrieving data from hash:")
            # for student_id, name in self.student_hash:
                # print(f"Student ID: {student_id}, Name: {self.student_hash.get(student_id)}")
            print(self.student_hash)

        def compare_fill():
            x_axis = ['Dictionary', 'Hash Table']
            fill_dict_time = timeit.timeit(lambda: fill_dict(), number=1)
            fill_hash_time = timeit.timeit(lambda: fill_hash(), number=1)

            y_axis = [fill_dict_time, fill_hash_time]

            result_string = ('Dictionary: ' + str(fill_dict_time) + " ns\n" + 'Hash Table: ' + str(fill_hash_time) +
                             ' ns\n')

            self.output_label.config(text=result_string)

            plt.bar(x_axis, y_axis)
            plt.title('Fill Data Structure')
            plt.xlabel('Data Type')
            plt.ylabel('Time (ns)')
            plt.show()

        def compare_print():
            x_axis = ['Dictionary', 'Hash Table']
            print_dict_time = timeit.timeit(lambda: print_dict(), number=1)
            print_hash_time = timeit.timeit(lambda: print_hash(), number=1)

            y_axis = [print_dict_time, print_hash_time]

            result_string = ('Dictionary: ' + str(print_dict_time) + " ns\n" + 'Hash Table: ' + str(print_hash_time) +
                             ' ns\n')

            self.output_label.config(text=result_string)

            plt.bar(x_axis, y_axis)
            plt.title('Print Data Structure')
            plt.xlabel('Data Type')
            plt.ylabel('Time (ns)')
            plt.show()

        compare_button = ttk.Button(self, text="Compare", command=lambda: compare_fill())
        compare_button.place(x=50, y=350, width=100, height=50)
        compare_button = ttk.Button(self, text="Compare", command=lambda: compare_print())
        compare_button.place(x=50, y=430, width=100, height=50)
        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=510, width=100, height=50)


# main
def main():
    app = HashDictSetComparisonApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
