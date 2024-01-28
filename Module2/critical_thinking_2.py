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

        label = ttk.Label(self, text="String Edit Distance", font=LARGE_FONT)
        label.place(x=250, y=10)

        self.first_word_label = ttk.Label(self, text="First Word", font=REGULAR_FONT)
        self.first_word_label.place(x=50, y=150)
        self.first_word_entry = ttk.Entry(self, width=20)
        self.first_word_entry.insert(-1, "algorithm")
        self.first_word_entry.place(x=50, y=180)

        self.second_word_label = ttk.Label(self, text="Second Word", font=REGULAR_FONT)
        self.second_word_label.place(x=50, y=230)
        self.second_word_entry = ttk.Entry(self, width=20)
        self.second_word_entry.insert(-1, "alligator")
        self.second_word_entry.place(x=50, y=260)

        self.result_field = ttk.Label(self, width=60, font=REGULAR_FONT)
        self.result_field.place(x=300, y=180)

        def edit_distance(word1, word2):
            m, n = len(word1), len(word2)
            i = 0
            word1_list = list(word1)
            word2_list = list(word2)

            # Initialize an array with all 20s. The size is the max of m and n.
            size_max = max(m, n)
            size_min = min(m, n)
            result = [20] * size_max

            # Compute transform cost by comparing words
            while i < size_min:
                if word1_list[i] == word2_list[i]:
                    result[i] = 0
                else:
                    result[i] = 5

                i += 1

            # Display results
            result_string = "Result \n"
            index = 0
            for element in result:
                if index == len(word1_list):
                    break
                if element == 0:
                    result_string += str(word1_list[index] + " ").ljust(4)
                else:
                    result_string += str(word1_list[index] + "* ").ljust(4)
                index += 1
            result_string += "\n"
            index = 0
            for element in result:
                if index == len(word2_list):
                    break
                if element == 0:
                    result_string += str(word2_list[index] + " ").ljust(4)
                else:
                    result_string += str(word2_list[index] + "* ").ljust(4)
                index += 1
            result_string += "\n\n"
            result_string += "Sum: " + str(sum(result))

            self.result_field.config(text=result_string)

            return sum(result)

        generate_button = ttk.Button(self, text="Generate", command=lambda: edit_distance(self.first_word_entry.get(),
                                                                                          self.second_word_entry.get()))
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
