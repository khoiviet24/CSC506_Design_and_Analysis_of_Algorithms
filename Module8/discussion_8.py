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
        self.num_trials = 100
        self.num_elements = 200
        self.input_array = []

        for _ in range(self.num_trials):
            temp_array = [random.randint(1, 1000) for _ in range(self.num_elements)]
            self.input_array.append(temp_array)

        label = ttk.Label(self, text="Sort Performance Comparison", font=LARGE_FONT)
        label.place(x=350, y=10)

        self.insert_results_label = ttk.Label(self, text='Sort Results', font=REGULAR_FONT)
        self.insert_results_label.place(x=50, y=100)
        self.insert_results_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.insert_results_text.place(x=50, y=150)

        self.insert_stats_label = ttk.Label(self, text='Sort Statistical Analysis', font=REGULAR_FONT)
        self.insert_stats_label.place(x=50, y=250)
        self.insert_stats_text = ttk.Label(self, text='', font=REGULAR_FONT)
        self.insert_stats_text.place(x=50, y=300)

        def bubble_sort(arr):
            n = len(arr)
            for i in range(n):
                swapped = False
                for j in range(0, n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
                        swapped = True

                if not swapped:
                    break

            # return arr
            return

        def bidirectional_bubble_sort(arr):
            n = len(arr)
            left = 0
            right = n - 1
            while left < right:
                swapped = False
                # Bubble up
                for i in range(left, right):
                    if arr[i] > arr[i + 1]:
                        arr[i], arr[i + 1] = arr[i + 1], arr[i]
                        swapped = True
                right -= 1
                if not swapped:
                    break

                # Bubble down
                for i in range(right, left, -1):
                    if arr[i] < arr[i - 1]:
                        arr[i], arr[i - 1] = arr[i - 1], arr[i]
                        swapped = True
                left += 1
                if not swapped:
                    break

            # return arr
            return

        def time_bubble_sort():
            bubble_sort_times = []
            for arr in enumerate(self.input_array):
                arr_copy = list(arr[1])
                start_time = time.time_ns()
                bubble_sort(arr_copy)
                end_time = time.time_ns()

                bubble_sort_times.append(end_time - start_time)

            return bubble_sort_times

        def time_bidirectional_bubble_sort():
            bidirectional_bubble_sort_times = []
            for arr in enumerate(self.input_array):
                arr_copy = list(arr[1])
                start_time = time.time_ns()
                bidirectional_bubble_sort(arr_copy)
                end_time = time.time_ns()

                bidirectional_bubble_sort_times.append(end_time - start_time)

            return bidirectional_bubble_sort_times

        def merge_sort(arr):
            if len(arr) <= 1:
                return arr

            # Split the array into two halves
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            # Recursively sort each half
            left_half = merge_sort(left_half)
            right_half = merge_sort(right_half)

            # Merge the sorted halves
            return merge(left_half, right_half)

        def merge(left, right):
            if left is None:
                return right
            elif right is None:
                return left
            merged = []
            left_idx, right_idx = 0, 0

            # Compare elements from both lists and merge them into a new list in sorted order
            while left_idx < len(left) and right_idx < len(right):
                if left[left_idx] < right[right_idx]:
                    merged.append(left[left_idx])
                    left_idx += 1
                else:
                    merged.append(right[right_idx])
                    right_idx += 1

            # Append any remaining elements from the left and right lists
            merged.extend(left[left_idx:])
            merged.extend(right[right_idx:])

            # return merged
            return

        def time_merge_sort():
            merge_sort_times = []
            for arr in enumerate(self.input_array):
                arr_copy = list(arr[1])
                start_time = time.time_ns()
                merge_sort(arr_copy)
                end_time = time.time_ns()

                merge_sort_times.append(end_time - start_time)

            return merge_sort_times

        def show_bst_times_insert():
            bubble_sort_times = time_bubble_sort()
            bidirectional_bubble_sort_times = time_bidirectional_bubble_sort()
            merge_sort_times = time_merge_sort()

            median_bubble = np.median(bubble_sort_times) / 10000000
            median_bidirectional_bubble = np.median(bidirectional_bubble_sort_times) / 10000000
            median_merge = np.median(merge_sort_times) / 10000000

            str_result = ('Average Bubble: ' + str(median_bubble) + ' ns\n' + 'Average Bidirectional Bubble: ' +
                          str(median_bidirectional_bubble) + ' ns\n' + 'Average Merge: ' + str(median_merge) +
                          ' ns')
            self.insert_results_text.config(text=str_result)

            f_statistic, p_value = f_oneway(bubble_sort_times, bidirectional_bubble_sort_times,
                                            merge_sort_times)
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
            plt.boxplot([bubble_sort_times, bidirectional_bubble_sort_times, merge_sort_times], vert=False, labels=
            ['Bubble Sort', 'Bidirectional Bubble Sort', 'Merge Sort'])
            plt.title(f"Time to sort ({self.num_elements} elements, {self.num_trials} trials)")
            plt.xlabel("Time (ns)")
            plt.ylabel("Sort Type")
            plt.show()

        show_tree_button = ttk.Button(self, text="      Sort \nComparison", command=lambda: show_bst_times_insert())
        show_tree_button.place(x=50, y=750, width=100, height=50)
        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        back_button.place(x=50, y=800, width=100, height=50)


# main
def main():
    app = SearchTreeApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
