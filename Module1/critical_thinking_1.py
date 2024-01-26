import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class NextLargerApp(tk.Tk):

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

        label = ttk.Label(self, text="Next Larger Value", font=LARGE_FONT)
        label.place(x=250, y=10)

        self.num_label = ttk.Label(self, text="Please enter a number with exactly one of each digit from 0-9",
                                          font=REGULAR_FONT)
        self.num_label.place(x=50, y=150)
        self.num_entry = ttk.Entry(self, width=20)
        self.num_entry.place(x=50, y=180)

        def get_user_input():
            try:
                user_input = int(self.num_entry.get())
            except ValueError:
                tkinter.messagebox.showinfo("Input Error",
                                            "Please enter a number with exactly one of each digit from 0-9")
                return

            num_str = str(user_input)
            # Check if the length is 10 (indicating all digits are present) and there are no duplicates
            if not len(num_str) == 10 and len(set(num_str)) == 10:
                tkinter.messagebox.showinfo("Input Error",
                                            "Please enter a number with exactly one of each digit from 0-9")
                return

            return user_input

        def find_next_larger(input_num):
            input_num_list = list(map(int, str(input_num)))

            # Find the first pair of adjacent digits where the left digit is smaller than the right digit
            # Start from the second to last digit, iterate left
            i = len(input_num_list) - 2
            while i >= 0 and input_num_list[i] > input_num_list[i+1]:
                i -= 1

            if i == -1:
                tkinter.messagebox.showinfo("Next Largest Number",
                                            "No rearrangement exists that produces a larger number.")
                return

            # Find the rightmost digit that is larger than the digit at i
            j = len(input_num_list) - 1
            while input_num_list[j] <= input_num_list[i]:
                j -= 1

            # Swap the digits at i and j
            input_num_list[i], input_num_list[j] = input_num_list[j], input_num_list[i]

            # Reverse the subarray to the right of i
            input_num_list[i+1:] = reversed(input_num_list[i+1:])

            result = ''.join(str(x) for x in input_num_list)

            result_str = "The Original Number: " + str(input_num) + "\n" + "Next Largest Number: " + result
            return result_str

        self.result_field = ttk.Label(self, width=60, font=REGULAR_FONT)
        self.result_field.place(x=50, y=250)

        generate_button = ttk.Button(self, text="Generate",
                                     command=lambda: self.result_field.config(text=find_next_larger(get_user_input())))
        generate_button.place(x=50, y=400, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=480, width=100, height=50)


# main
def main():
    app = NextLargerApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
