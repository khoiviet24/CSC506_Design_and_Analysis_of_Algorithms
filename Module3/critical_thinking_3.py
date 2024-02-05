import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import random
import timeit
import matplotlib.pyplot as plt

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class HybridSortApp(tk.Tk):

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
        self.random_list = []

        for i in range(0, 500):
            n = random.randint(1, 1000)
            self.random_list.append(n)

        label = ttk.Label(self, text="Sort Comparison", font=LARGE_FONT)
        label.place(x=250, y=10)

        self.results_label = ttk.Label(self, text='Results', font=REGULAR_FONT)
        self.results_label.place(x=50, y=100)
        self.output_label = ttk.Label(self, text='', font=REGULAR_FONT)
        self.output_label.place(x=50, y=130)

        def selection_sort(arr):
            for i in range(len(arr)):
                min_index = i

                for j in range(i + 1, len(arr)):
                    if arr[j] < arr[min_index]:
                        min_index = j
                (arr[i], arr[min_index]) = (arr[min_index], arr[i])

        def insertion_sort(arr):
            for i in range(1, len(arr)):
                key = arr[i]
                j = i - 1

                while j >= 0 and key < arr[j]:
                    arr[j + 1] = arr[j]
                    j -= 1

                arr[j + 1] = key

        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            else:
                pivot = arr[len(arr) // 2]
                left = [x for x in arr if x < pivot]
                middle = [x for x in arr if x == pivot]
                right = [x for x in arr if x > pivot]
                arr[:] = quicksort(left) + middle + quicksort(right)

            return arr

        def merge(arr, left_half, right_half):
            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            # Check for any remaining elements in left_half
            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            # Check for any remaining elements in right_half
            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

        def merge_sort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2
                left_half = arr[:mid]
                right_half = arr[mid:]

                merge_sort(left_half)
                merge_sort(right_half)
                merge(arr, left_half, right_half)

        def compare_sorts():
            x_axis = ['Selection', 'Insertion', 'Quicksort', 'Merge']
            selection_sort_time = timeit.timeit(lambda: selection_sort(self.random_list.copy()), number=1)
            insertion_sort_time = timeit.timeit(lambda: insertion_sort(self.random_list.copy()), number=1)
            quicksort_time = timeit.timeit(lambda: quicksort(self.random_list.copy()), number=1)
            merge_sort_time = timeit.timeit(lambda: merge_sort(self.random_list.copy()), number=1)

            y_axis = [selection_sort_time, insertion_sort_time, quicksort_time, merge_sort_time]

            result_string = ('Selection Sort: ' + str(selection_sort_time) + " ns\n" + 'Insertion Sort: ' +
                             str(insertion_sort_time) + ' ns\n' + 'Quicksort: ' + str(quicksort_time) + ' ns\n' +
                             'Merge Sort: ' + str(merge_sort_time) + ' ns\n')

            self.output_label.config(text=result_string)

            plt.bar(x_axis, y_axis)
            plt.title('Sort Comparison')
            plt.xlabel('Sort Type')
            plt.ylabel('Time (ns)')
            plt.show()

        compare_button = ttk.Button(self, text="Compare", command=lambda: compare_sorts())
        compare_button.place(x=50, y=400, width=100, height=50)
        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=480, width=100, height=50)


# main
def main():
    # print_welcome_menu()
    app = HybridSortApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
