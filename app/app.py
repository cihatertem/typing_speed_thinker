import tkinter as tk
from tkinter.messagebox import showinfo
from random import sample


class App(tk.Tk):
    """
    Typing Speed Test Main Class based on Tkinter
    """
    BACKGROUND_PRIMARY = "#f8f8f0"
    BACKGROUND_SECONDARY = "#eeeeee"
    BACKGROUND_WORD = "#b8e069"
    FOREGROUND = "#888888"
    WHITE = "#fff"
    BLACK = "#000"

    def __init__(self, word_repository) -> None:
        super().__init__()
        self.word_repository = word_repository
        self.words_list = [
            self.load_random_words_row() for _ in range(3)
        ]
        self.word_labels_list = []
        self.word_label_index = 0
        self.show_words_on_screen()
        self.fill_color_word_background()
        self.word_counter = 0
        self.failed_counter = 0
        self.schedule = None

        # Tkinter
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 1320
        self.window_height = 760

        self.title("Typing Speed Tester")
        self.geometry(
            f"{self.window_width}x{self.window_height}"
            f"+{round(self.screen_width / 2 - self.window_width / 2)}"
            f"+{round(self.screen_height / 2 - self.window_height / 2)}"
        )
        self.config(bg=self.BACKGROUND_PRIMARY)
        self.resizable(False, False)

        self.header = tk.Label(
            self,
            text="Typing Speed Tester",
            anchor=tk.CENTER,
            justify=tk.CENTER,
            background=self.BACKGROUND_PRIMARY,
            foreground=self.FOREGROUND,
            font=("Ubuntu", 48, "bold", "italic"),
        )
        self.header.grid(
            row=1, column=1, columnspan=5, pady=20, padx=200
        )

        self.description = tk.Label(
            self,
            text="How fast are your fingers? Try the one-minute typing test to"
                 " find out!\n Press the space bar after each word. "
                 "At the end, your typing speed in WPM. \n"
                 "Good luck!",
            justify=tk.CENTER,
            anchor=tk.CENTER,
            background=self.BACKGROUND_PRIMARY,
            foreground=self.FOREGROUND,
            font=("Ubuntu", 10, "normal")
        )
        self.description.grid(row=2, column=1, columnspan=5, pady=70)

        self.wpm_label = tk.Label(
            self,
            text="WPM: ",
            foreground=self.FOREGROUND,
            background=self.BACKGROUND_SECONDARY,
            font=("Ubuntu", 8, "normal")
        )
        self.wpm_label.grid(row=3, column=1, sticky=tk.SE, pady=20)

        self.wpm_text = tk.StringVar(value="?")
        self.wpm_box = tk.Label(
            self,
            textvariable=self.wpm_text,
            foreground=self.FOREGROUND,
            background=self.WHITE,
            width=3,
            anchor=tk.CENTER
        )
        self.wpm_box.grid(row=3, column=2, sticky=tk.SW, pady=20, padx=10)

        self.time_label = tk.Label(
            self,
            text="Time Left: ",
            foreground=self.FOREGROUND,
            background=self.BACKGROUND_SECONDARY,
            font=("Ubuntu", 8, "normal"),
        )
        self.time_label.grid(row=3, column=3, sticky=tk.SE, pady=20)

        self.time_text = tk.StringVar(value="60")
        self.time_box = tk.Label(
            self,
            textvariable=self.time_text,
            foreground=self.FOREGROUND,
            background=self.WHITE,
            anchor=tk.CENTER,
            width=3
        )
        self.time_box.grid(row=3, column=4, sticky=tk.SW, pady=20, padx=10)

        self.restart_btn = tk.Button(
            self,
            text="Restart",
            font=("Ubuntu", 8, "bold"),
            background=self.BACKGROUND_PRIMARY,
            foreground=self.FOREGROUND,
            command=lambda: self.restart()
        )
        self.restart_btn.grid(row=3, column=5, pady=20)

        self.word_var = tk.StringVar()
        self.word = tk.Entry(
            self,
            textvariable=self.word_var,
            foreground=self.BLACK,
            background=self.WHITE,
            font=("Ubuntu Mono", 12, "bold"),
            justify=tk.CENTER
        )
        self.word.grid(
            row=7, column=2, columnspan=3, pady=10, ipady=10,
        )

        self.word.focus()
        self.word.bind("<space>", self.press_space_event_handler)
        self.word.bind("<KeyPress>", self.start_timer)

    def start_timer(self, event) -> int:
        """
        Tkinter event handler callback function that starts time counter
        :param event: Tkinter event parameter
        :return: 0 to break recursive out.
        """
        second = int(self.time_text.get())
        if second == 0:
            self.after_cancel(self.schedule)
            self.word.unbind("<space>")
            self.word["state"] = "disabled"
            showinfo(
                "Your WPM Score!",
                f"WPM: {self.word_counter}\nTyping Fail: {self.failed_counter}"
            )
            return 0

        self.time_text.set(str(second - 1))
        self.schedule = self.after(1000, lambda: self.start_timer(event))
        self.word.unbind("<KeyPress>")

    def press_space_event_handler(self, event) -> None:
        """
        Tkinter event handler callback function that controls press SPACE key
        event.
        :param event: Tkinter event parameter
        :return:
        """
        self.check_final_word()
        self.shift_word_rows()
        self.change_word_bg_color()
        self.clear_word_entry()

    def check_final_word(self) -> None:
        """
        Compares last state of the word in input  with current word and
        increases success/failed counter variables.
        :return:
        """
        text = self.word_labels_list[self.word_label_index]["text"]
        if self.word_var.get().strip() == text:
            self.word_counter += 1
        else:
            self.failed_counter += 1
        self.wpm_text.set(str(self.word_counter))

    def clear_and_fill_word_list(self) -> None:
        """
        Clears and refill instance's word_list list.
        :return:
        """
        self.words_list.clear()

        for _ in range(3):
            self.words_list.append(
                self.load_random_words_row()
            )

    def shift_word_rows(self) -> None:
        """
        Shifts and replace words list
        :return:
        """
        if self.word_label_index == 14:
            self.clear_and_fill_word_list()

            updated_words_list = []
            for row in self.words_list:
                for word in row:
                    updated_words_list.append(word)

            for index, label in enumerate(self.word_labels_list):
                label["text"] = updated_words_list[index]
                if index == 14:
                    self.empty_color_word_background()

    def change_word_bg_color(self) -> None:
        """
        Changes background color of the current word.
        :return:
        """
        if self.word_label_index < 14:
            self.empty_color_word_background()
            self.word_label_index += 1
        else:
            self.word_label_index = 0

        self.fill_color_word_background()

    def empty_color_word_background(self) -> None:
        """
        Clears background color previous "current word".
        :return:
        """
        self.word_labels_list[self.word_label_index] \
            ["background"] = self.BACKGROUND_PRIMARY
        self.word_labels_list[self.word_label_index] \
            ["foreground"] = self.FOREGROUND

    def fill_color_word_background(self) -> None:
        """
        Fills green background color of the current word.
        :return:
        """
        self.word_labels_list[self.word_label_index] \
            ["background"] = self.BACKGROUND_WORD
        self.word_labels_list[self.word_label_index] \
            ["foreground"] = self.BLACK

    def clear_word_entry(self) -> None:
        """
        Clears word input characters.
        :return:
        """
        self.word_var.set("")

    def restart(self) -> None:
        """
        Restarts and re-initializes the typing test.
        :return:
        """
        self.clear_word_entry()
        self.wpm_text.set("0")
        self.time_text.set("60")

        for label in self.word_labels_list:
            label.destroy()

        self.clear_and_fill_word_list()
        self.word_labels_list = []
        self.word_label_index = 0
        self.word_counter = 0
        self.failed_counter = 0
        self.show_words_on_screen()
        self.fill_color_word_background()

        if self.schedule:
            self.after_cancel(self.schedule)

        self.word["state"] = "normal"
        self.word.focus()
        self.word.bind("<space>", self.press_space_event_handler)
        self.word.bind("<KeyPress>", self.start_timer)

    def load_random_words_row(self) -> list:
        """
        Chooses randomly 5 words from word_repository, adds those words in a
        list.
        :return: Returns the word list with 5 randomly chosen words.
        """
        words_on_screen = [
            *sample(self.word_repository, k=5)
        ]
        return words_on_screen

    def show_words_on_screen(self) -> None:
        """
        Shows words list on the screen.
        :return:
        """
        word_row = 4
        word_column = 1
        for row in self.words_list:
            for word in row:
                word_label = tk.Label(
                    self,
                    text=word,
                    fg=self.FOREGROUND,
                    bg=self.BACKGROUND_PRIMARY,
                    font=("Ubuntu", 14, "bold"),
                    justify=tk.CENTER,
                    anchor=tk.CENTER,
                    width=13
                )

                word_label.grid(
                    row=word_row, column=word_column, sticky=tk.NS,
                    pady=5, ipadx=4, ipady=5
                )
                self.word_labels_list.append(word_label)

                word_column += 1

            word_column = 1
            word_row += 1
