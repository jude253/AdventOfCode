# advent-of-code

This repository makes it easy to do the daily challenges for
[advent of code](https://adventofcode.com/) using python.  Additonally,
it uses [hatch](https://hatch.pypa.io/) as the python build system back
end to manage python and dependency versions.

-----

## How to run code for a daily challenge

Substitute the file path of the daily challenge you want to run in the
below command:

```
hatch run python src/advent_of_code/solutions/year_2024/day_00.py
```

## How to run linting/type checking

The below command runs formatting, linting, and type checking:

```
hatch run build-tool:check
```

They can be run individually with these commands:

```
hatch run build-tool:format
hatch run build-tool:lint
hatch run build-tool:types
```

## License

`advent-of-code` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
