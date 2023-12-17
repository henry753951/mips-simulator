from Instructions import Instruction
from pprint import pprint
from colorama import Fore, Back, Style

from MemAndReg import MemAndReg
from stages import ControlUnit, EXStage, IDStage, IFStage, MEMStage, WBStage


def log(string, color=Fore.WHITE):
    print(color + string + Style.RESET_ALL)


def main(args):
    file = open(args.command, "r")
    commands = file.read().splitlines()
    file.close()
    Instructions = [perLine.split(" ", 1) for perLine in commands]
    Instructions = [
        Instruction(opcode, args.replace(" ", "").split(",")) for opcode, args in Instructions
    ]
    log("Load commands from %s" % args.command, Fore.GREEN)
    print("\n".join([str(x) for x in Instructions]))

    log("Initialize registers and data memory", Fore.GREEN)
    _MemAndReg = MemAndReg()
    _MemAndReg.print()

    log("Start executing commands...", Fore.GREEN)
    pipeline = "Y" == input("Use pipeline? (Y/N) ").upper()
    log("")
    controlUnit = ControlUnit(_MemAndReg, Instructions, pipeline)
    controlUnit.stages = [
        IFStage(controlUnit),
        IDStage(controlUnit),
        EXStage(controlUnit),
        MEMStage(controlUnit),
        WBStage(controlUnit),
    ]
    controlUnit.start()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command file", default="command.txt", nargs='?')
    parser.add_argument("result", help="result file", default="result.txt", nargs='?')
    args = parser.parse_args()
    main(args)
