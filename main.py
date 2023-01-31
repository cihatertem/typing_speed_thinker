import json
from app.utils import fill_word_list
from app.app import App


def main() -> None:
    while True:
        try:
            with open("data/word_list.json", "r") as file:
                word_list = json.load(file)
                break
        except FileNotFoundError:
            fill_word_list()

    app = App(word_list)
    app.mainloop()


if __name__ == "__main__":
    main()
