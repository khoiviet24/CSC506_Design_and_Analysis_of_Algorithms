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

        for i in range(0, 2000):
            n = random.randint(1, 1000)
            self.random_list.append(n)

        label = ttk.Label(self, text="Sort Comparison", font=LARGE_FONT)
        label.place(x=250, y=10)

        self.results_label = ttk.Label(self, text='Sorted Data', font= REGULAR_FONT)
        self.results_label.place(x=50, y=100)
        self.output_label = ttk.Label(self, text='', font= REGULAR_FONT)
        self.output_label.place(x=50, y=130)

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

        def quicksort_partition(arr, limit):
            if len(arr) <= limit:
                insertion_sort(arr)
            else:
                pivot = arr[len(arr) // 2]
                left = [x for x in arr if x < pivot]
                middle = [x for x in arr if x == pivot]
                right = [x for x in arr if x > pivot]
                arr[:] = quicksort(left) + middle + quicksort(right)

            return arr

        def compare_sorts():
            x_axis = ['Quicksort', 'Partition=10', 'Partition=20', 'Partition=50']
            quicksort_time = timeit.timeit(lambda: quicksort(self.random_list.copy()), number=1)
            quicksort_10_time = timeit.timeit(lambda: quicksort_partition(self.random_list.copy(), 10), number=1)
            quicksort_20_time = timeit.timeit(lambda: quicksort_partition(self.random_list.copy(), 20), number=1)
            quicksort_50_time = timeit.timeit(lambda: quicksort_partition(self.random_list.copy(), 50), number=1)

            y_axis = [quicksort_time, quicksort_10_time, quicksort_20_time, quicksort_50_time]

            result_string = ('Quicksort: ' + str(quicksort_time) + " ns\n" + 'Partition = 10: ' +
                             str(quicksort_10_time) + ' ns\n' + 'Partition = 20: ' + str(quicksort_20_time) + ' ns\n' +
                             'Partition = 50: ' + str(quicksort_50_time) + ' ns\n')

            self.output_label.config(text=result_string)

            plt.bar(x_axis, y_axis)
            plt.title('Quicksort Comparison')
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
