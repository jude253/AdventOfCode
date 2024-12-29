# advent-of-code

This repository makes it easy to do the daily challenges for
[advent of code](https://adventofcode.com/) using python.  Additonally,
it uses [hatch](https://hatch.pypa.io/) as the python build system back
end to manage python and dependency versions.

-----

# Input Files

Input files should go in the input folder for the appropriate day/year.
They are currently expected to not have a file extension.  Each year
should have a corresponding input and solutions folder.

## How to run python code for a daily challenge (Hatch)

Substitute the file path of the daily challenge you want to run in the
below command:

```bash
hatch run python src/advent_of_code/solutions/year_2024/day_00.py
```

## How to run python linting/type checking (Hatch)

The below command runs formatting, linting, and type checking:

```bash
hatch run build-tool:check
```

They can be run individually with these commands:

```bash
hatch run build-tool:format
hatch run build-tool:lint
hatch run build-tool:types
```

## How to run python code using CLI (Hatch or Bazel)


### Bazel

```bash
bazel run main 2024 01
```


### Hatch

```bash
hatch run python src/advent_of_code/main.py 2024 01
```

### Bazel notes

- Command reminders:
    - Bazel build all command: `bazel build //...`
    - Bazel build main command: `bazel build //:main`
    - Bazel test command: `bazel test //:test`
    - Bazel clean command: `bazel clean`
- Be sure to run `bazel run //:requirements.update` before adding new packages to `py_binary` or other `rules_python` function.  Also this may need to be run again to update the dependencies for a different platform than the one this command was orignally run on (MacOS)
- Didn't try using bazel to install/run hatch, but that might be better to reduce dependency duplication
- There is a lot of duplication of python version logic and dependency specification, but it works
- It could be good to separate out the code better to have different libraries for the cli, input and daily code, but I didn't do this b/c not sure how to do this easily with hatch
- Didn't see if it was possible to specify python dependencies in a `pyproject.toml` file rather than a requirements.txt style file, but that could reduce complexity, though not sure `rules_python` could parse it in the same format as hatch, which is why it might best to just install hatch with bazel and run it that way.


## License

`advent-of-code` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
