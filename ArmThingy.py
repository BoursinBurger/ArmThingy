from ArmThingyUI import ArmThingyUI
from tkinter import Tk


def main():
    """
    Entry point for the application.
    :return:
    """
    root = Tk()
    ui = ArmThingyUI(root)
    ui.run()


if __name__ == "__main__":
    main()
