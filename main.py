import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", action="store")
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
