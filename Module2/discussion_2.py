import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import random
from random import shuffle
import time

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class SearchComparisonApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1100x600")

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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.sorted_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.unsorted_data = self.sorted_data.copy()
        random.shuffle(self.unsorted_data)

        label = ttk.Label(self, text="Search Comparison", font=LARGE_FONT)
        label.place(x=350, y=10)

        self.sorted_label = ttk.Label(self, text="Sorted Data", font=REGULAR_FONT)
        self.sorted_label.place(x=50, y=100)
        sorted_data_string = ', '.join(str(x) for x in self.sorted_data)
        self.sorted_data_label = ttk.Label(self, text= sorted_data_string, font=REGULAR_FONT)
        self.sorted_data_label.place(x=50, y=130)

        self.unsorted_label = ttk.Label(self, text="Unsorted Data", font=REGULAR_FONT)
        self.unsorted_label.place(x=50, y=180)
        unsorted_data_string = ', '.join(str(x) for x in self.unsorted_data)
        self.unsorted_data_label = ttk.Label(self, text=unsorted_data_string, font=REGULAR_FONT)
        self.unsorted_data_label.place(x=50, y=210)

        self.num_label = ttk.Label(self, text="Please enter a number to find in the arrays.", font=REGULAR_FONT)
        self.num_label.place(x=50, y=260)
        self.num_entry = ttk.Entry(self, width=20)
        self.num_entry.place(x=50, y=290)

        self.sorted_result_label = ttk.Label(self, width=60, font=REGULAR_FONT)
        self.sorted_result_label.place(x=200, y=330)
        self.unsorted_result_label = ttk.Label(self, width=60, font=REGULAR_FONT)
        self.unsorted_result_label.place(x=650, y=330)

        def get_user_input():
            try:
                user_input = int(self.num_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Input Error", "Please enter a valid number.")
                return

            return user_input

        def binary_search(arr, input_num):
            lower = 0
            upper = len(arr) - 1

            while lower <= upper:
                middle = (lower + upper) // 2
                if arr[middle] == input_num:
                    return middle
                elif arr[middle] < input_num:
                    lower = middle + 1
                else:
                    upper = middle - 1

            return -1

        def linear_search(arr, input_num):
            for index, element in enumerate(arr):
                if element == input_num:
                    return index

            return -1

        def median_of_three(a, b, c):
            return sorted([a, b, c])[1]

        def quicksort(arr):
            if len(arr) <= 1:
                return arr

            pivot = median_of_three(arr[0], arr[len(arr)//2], arr[-1])

            left = [x for x in arr if x < pivot]
            middle = [x for x in arr if x == pivot]
            right = [x for x in arr if x > pivot]

            return quicksort(left) + middle + quicksort(right)

        def print_results():
            user_input = get_user_input()

            sorted_binary_search_start = time.time_ns()
            sorted_binary_search_result = binary_search(self.sorted_data, user_input)
            sorted_binary_search_end = time.time_ns()
            sorted_binary_search_result_time = sorted_binary_search_end - sorted_binary_search_start

            sorted_linear_search_start = time.time_ns()
            sorted_linear_search_result = linear_search(self.sorted_data, user_input)
            sorted_linear_search_end = time.time_ns()
            sorted_linear_search_result_time = sorted_linear_search_end - sorted_linear_search_start

            sorted_binary_search_result_string = "Binary: The value " + str(user_input)
            if sorted_binary_search_result == -1:
                sorted_binary_search_result_string += " is not in the array.\n"
            else:
                sorted_binary_search_result_string += " is at index " + str(sorted_binary_search_result) + ".\n"
            sorted_binary_search_result_string += "Time: " + str(sorted_binary_search_result_time) + "ns\n"

            sorted_linear_search_result_string = "Linear: The value " + str(user_input)
            if sorted_linear_search_result == -1:
                sorted_linear_search_result_string += " is not in the array.\n"
            else:
                sorted_linear_search_result_string += " is at index " + str(sorted_linear_search_result) + ".\n"
            sorted_linear_search_result_string += "Time: " + str(sorted_linear_search_result_time) + "ns\n"

            self.sorted_result_label.config(text="Sorted" + "\n\n" + sorted_binary_search_result_string + "\n" +
                                            sorted_linear_search_result_string)

            unsorted_binary_search_start = time.time_ns()
            unsorted_binary_search_result = binary_search(self.unsorted_data, user_input)
            unsorted_binary_search_end = time.time_ns()
            unsorted_binary_search_result_time = unsorted_binary_search_end - unsorted_binary_search_start

            unsorted_linear_search_start = time.time_ns()
            unsorted_linear_search_result = linear_search(self.unsorted_data, user_input)
            unsorted_linear_search_end = time.time_ns()
            unsorted_linear_search_result_time = unsorted_linear_search_end - unsorted_linear_search_start

            unsorted_binary_search_result_string = "Binary: The value " + str(user_input)
            if unsorted_binary_search_result == -1:
                unsorted_binary_search_result_string += " is not in the array.\n"
            else:
                unsorted_binary_search_result_string += " is at index " + str(unsorted_binary_search_result) + ".\n"
            unsorted_binary_search_result_string += "Time: " + str(unsorted_binary_search_result_time) + "ns\n"

            unsorted_linear_search_result_string = "Linear: The value " + str(user_input)
            if unsorted_linear_search_result == -1:
                unsorted_linear_search_result_string += " is not in the array.\n"
            else:
                unsorted_linear_search_result_string += " is at index " + str(unsorted_linear_search_result) + ".\n"
            unsorted_linear_search_result_string += "Time: " + str(unsorted_linear_search_result_time) + "ns\n"

            self.unsorted_result_label.config(text="Unsorted" + "\n\n" + unsorted_binary_search_result_string + "\n" +
                                                 unsorted_linear_search_result_string)

        find_button = ttk.Button(self, text="Find", command=lambda: print_results())
        find_button.place(x=50, y=450, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=510, width=100, height=50)


# main
def main():
    # print_welcome_menu()
    app = SearchComparisonApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
