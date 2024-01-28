import tkinter as tk
import tkinter.messagebox
from tkinter import ttk

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class TemplateApp(tk.Tk):

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
        for F in (StartPage, LoginPage):
            frame = F(container, self)

            # initializing frame of that object from
            # StartPage, LoginPage, respectively with
            # for loop
            self.frames[F] = frame

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

        label = ttk.Label(self, text="Template", font=LARGE_FONT)
        label.place(x=350, y=10)

        login_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame(LoginPage))
        login_button.place(x=50, y=240, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=400, width=100, height=50)


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login", font=LARGE_FONT)
        label.place(x=400, y=10)

        username_title = ttk.Label(self, text="Username")
        username_title.place(x=50, y=150)
        username_field = ttk.Entry(self, width=20)
        username_field.place(x=50, y=170)

        password_title = ttk.Label(self, text="Password")
        password_title.place(x=50, y=220)
        password_field = ttk.Entry(self, show="*", width=20)
        password_field.place(x=50, y=240)

        back_button = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        back_button.place(x=50, y=400, width=100, height=50)


# main
def main():
    # print_welcome_menu()
    app = TemplateApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
