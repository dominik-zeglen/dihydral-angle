from argparse import ArgumentParser
from csv import writer
from argparse import ArgumentTypeError

from src.main import get_pdb_info, get_protein_info
from src.colors import bcolors


def str2bool(value):
    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--name", type=str)
    arg_parser.add_argument("--out", default="stdout", type=str)
    arg_parser.add_argument(
        "--info", const=True, default=False, nargs="?", type=str2bool
    )

    args = vars(arg_parser.parse_args())

    if not args["name"]:
        print(bcolors.FAIL + "It seems like you forgot --name argument" + bcolors.ENDC)
    else:
        data = get_pdb_info(args["name"])
        if args["info"]:
            print(get_protein_info(args["name"]))
        elif args["out"] == "csv":
            with open("angles/" + args["name"], "w") as f:
                csv_writer = writer(f, delimiter=" ")
                csv_writer.writerows([(line["fi"], line["psi"]) for line in data])
        else:
            for line in data:
                print(str(line["fi"]) + " " + str(line["psi"]))
