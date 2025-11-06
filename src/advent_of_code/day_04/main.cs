using System;

public static class Day04
{
    public static string GetInputFileContents(string filePath = "input/day_04/input.txt")
    {
        string inputFileContents = File.ReadAllText(filePath);
        return inputFileContents;
    }

    public static bool IsFullyContained(int start1, int end1, int start2, int end2)
    {
        if (start1 <= start2 && end1 >= end2)
        {
            return true;
        }
        if (start2 <= start1 && end2 >= end1)
        {
            return true;
        }
        return false;
    }

    // Returns true if the two inclusive ranges [a1,b1] and [a2,b2] overlap at all
    public static bool IsOverlap(int a1, int b1, int a2, int b2)
    {
        return !(b1 < a2 || b2 < a1);
    }

    public static void PartOne(string inputFileContents)
    {
        int containtedCount = 0;

        foreach (var inputFileLine in inputFileContents.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var tmp = inputFileLine.Split(',');
            var elf1 = tmp[0];
            var elf2 = tmp[1];

            var e1 = elf1.Split('-');
            var e2 = elf2.Split('-');

            int elf1StartInt = int.Parse(e1[0]);
            int elf1EndInt = int.Parse(e1[1]);
            int elf2StartInt = int.Parse(e2[0]);
            int elf2EndInt = int.Parse(e2[1]);

            if (IsFullyContained(elf1StartInt, elf1EndInt, elf2StartInt, elf2EndInt))
            {
                containtedCount += 1;
            }
        }
        Console.WriteLine("Total fully contained: " + containtedCount);
    }

    public static void PartTwo(string inputFileContents)
    {
        int overlapCount = 0;

        foreach (var inputFileLine in inputFileContents.Split('\n', StringSplitOptions.RemoveEmptyEntries))
        {
            var tmp = inputFileLine.Split(',');
            var elf1 = tmp[0];
            var elf2 = tmp[1];

            var e1 = elf1.Split('-');
            var e2 = elf2.Split('-');

            int elf1StartInt = int.Parse(e1[0]);
            int elf1EndInt = int.Parse(e1[1]);
            int elf2StartInt = int.Parse(e2[0]);
            int elf2EndInt = int.Parse(e2[1]);

            if (IsOverlap(elf1StartInt, elf1EndInt, elf2StartInt, elf2EndInt))
            {
                overlapCount += 1;
            }
        }

        Console.WriteLine("Total overlapping: " + overlapCount);
    }

    public static void Run()
    {
        string inputFileContents;
        // inputFileContents = GetInputFileContents("input/day_04/test.txt");
        inputFileContents = GetInputFileContents("input/day_04/input.txt");

        Console.WriteLine("Part One:");
        PartOne(inputFileContents);

        Console.WriteLine("Part Two:");
        PartTwo(inputFileContents);
    }
}