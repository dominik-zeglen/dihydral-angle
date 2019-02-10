# Before you start

First of all, run

```
$ python -m pip install -r requirements.txt
```

to install all packages that are required to run this program.

# Usage

After you install packages, you can run program by invoking

```
$ python main.py --name <pdb_name> --out <output>
```

where `<pdb_name>` is the 4-symbol protein code, and `<output>` is either `csv` or `stdin`. `<output>` is set to `stdin` by default, so you do not have to repeat yourself each time you want to test the command.
