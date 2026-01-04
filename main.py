import argparse


def main():
    parser = argparse.ArgumentParser(usage="python main.py [-g], where -g runs the GUI, otherwise runs the CLI.")
    parser.add_argument("-g", "--gui", action="store_true", help="run the GUI")
    args = parser.parse_args()
    if args.gui:
        from gui import guiMain
        from sys import argv
        guiMain(argv)
    else:
        from cli import cliMain
        cliMain()


if __name__ == "__main__":
    main()
