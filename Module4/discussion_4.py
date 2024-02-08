import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import tkinter.scrolledtext as st

LARGE_FONT = ("Verdana", 35)
REGULAR_FONT = ("Verdana", 14)


class QueueUsingStacksApp(tk.Tk):

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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.stack1 = [] # For enqueue
        self.stack2 = [] # For dequeue

        label = ttk.Label(self, text="Queue Using Stacks", font=LARGE_FONT)
        label.place(x=250, y=10)

        def on_entry_click_enqueue(event):
            if self.enqueue_entry.get() == 'Enter value':
                self.enqueue_entry.delete(0, tk.END)
                self.enqueue_entry.config(foreground='black')

        def on_focus_out_enqueue(event):
            if not self.enqueue_entry.get():
                self.enqueue_entry.insert(0, 'Enter value')
                self.enqueue_entry.config(foreground='grey')

        default_value_text = "Enter value"
        self.enqueue_entry = ttk.Entry(self, width=15, foreground='grey')
        self.enqueue_entry.insert(0, default_value_text)
        self.enqueue_entry.bind('<FocusIn>', on_entry_click_enqueue)
        self.enqueue_entry.bind('<FocusOut>', on_focus_out_enqueue)
        self.enqueue_entry.place(x=50, y=150)
        self.enqueue_button = ttk.Button(self, text='Enqueue', command=lambda: get_enqueue())
        self.enqueue_button.place(x=50, y=180, width=100, height=50)

        self.dequeue_button = ttk.Button(self, text='Dequeue', command=lambda: dequeue())
        self.dequeue_button.place(x=50, y=260, width=100, height=50)

        self.queue_label = ttk.Label(self, text='Queue', font=REGULAR_FONT)
        self.queue_label.place(x=200, y=100)
        self.queue_text_area = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.queue_text_area.place(x=200, y=150)

        self.stack1_label = ttk.Label(self, text='Stack 1', font=REGULAR_FONT)
        self.stack1_label.place(x=425, y=100)
        self.stack1_text_area = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.stack1_text_area.place(x=425, y=150)

        self.stack2_label = ttk.Label(self, text='Stack 2', font=REGULAR_FONT)
        self.stack2_label.place(x=650, y=100)
        self.stack2_text_area = st.ScrolledText(self, width=15, height=10, font=REGULAR_FONT)
        self.stack2_text_area.place(x=650, y=150)

        def get_enqueue():
            value_to_insert = self.enqueue_entry.get()

            if value_to_insert == 'Enter value':
                tkinter.messagebox.showinfo('Invalid Enqueue', 'Please enter value to enqueue.')
                return

            enqueue(value_to_insert)

            self.enqueue_entry.delete(0, tk.END)
            self.enqueue_entry.config(foreground='grey')
            self.enqueue_entry.insert(0, default_value_text)

        def enqueue(item):
            # Push item onto stack 1
            self.stack1.append(item)
            show_queue()
            show_stack1()

        def dequeue():
            if not self.stack2:
                # If stack2 is empty, transfer elements from stack1 to stack2
                # Top of stack2 represents first elements put into stack1
                while self.stack1:
                    self.stack2.append(self.stack1.pop())

            # Pop from stack2 if it's not empty
            if self.stack2:
                self.stack2.pop()
                show_queue()
                show_stack1()
                show_stack2()
                return
            else:
                # Queue is empty
                tkinter.messagebox.showinfo('Empty Queue', 'The queue is empty.')
                return

        def show_queue():
            res = 'First\n'
            res += '-------\n'
            stack1_copy = self.stack1.copy()
            stack2_copy = self.stack2.copy()

            while stack2_copy:
                res += str(stack2_copy.pop()) + '\n'

            while stack1_copy:
                stack2_copy.append(stack1_copy.pop())

            while stack2_copy:
                res += str(stack2_copy.pop()) + '\n'

            res += '-------\n'
            res += 'Last'

            self.queue_text_area.delete(1.0, tk.END)
            self.queue_text_area.insert(tk.INSERT, res)

        def show_stack1():
            res = 'Top\n'
            res += '-------\n'
            stack1_copy = self.stack1.copy()

            while stack1_copy:
                res += str(stack1_copy.pop()) + '\n'

            res += '-------\n'
            res += 'Bottom \n'

            self.stack1_text_area.delete(1.0, tk.END)
            self.stack1_text_area.insert(tk.INSERT, res)

        def show_stack2():
            res = 'Top\n'
            res += '-------\n'
            stack2_copy = self.stack2.copy()

            while stack2_copy:
                res += str(stack2_copy.pop()) + '\n'

            res += '-------\n'
            res += 'Bottom \n'

            self.stack2_text_area.delete(1.0, tk.END)
            self.stack2_text_area.insert(tk.INSERT, res)

        def clear_all():
            self.stack1 = []
            self.stack2 = []
            self.queue_text_area.delete(1.0, tk.END)
            self.stack1_text_area.delete(1.0, tk.END)
            self.stack2_text_area.delete(1.0, tk.END)

        clear_button = ttk.Button(self, text="Clear", command=lambda: clear_all())
        clear_button.place(x=50, y=450, width=100, height=50)

        quit_button = ttk.Button(self, text="Quit", command=lambda: controller.destroy())
        quit_button.place(x=50, y=500, width=100, height=50)


# main
def main():
    app = QueueUsingStacksApp()
    app.mainloop()


# Execute main
if __name__ == "__main__":
    main()
