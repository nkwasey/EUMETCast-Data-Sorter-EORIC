
from packages.ui import *


def main():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
