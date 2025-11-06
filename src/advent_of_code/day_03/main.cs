using System.Collections.Immutable;
using System.ComponentModel;
using System.Numerics;

public static class Day03
{
    public static string GetInputFileContents(string filePath = "input/day_03/input.txt")
    {
        string inputFileContents = File.ReadAllText(filePath);
        return inputFileContents;
    }

    public static int GetPrioritySum(List<char> overlappingItems)
    {
        int a_value = (int)'a';
        int z_value = (int)'z';
        int A_value = (int)'A';
        int Z_value = (int)'Z';

        int totalPriority = 0;

        foreach (char item in overlappingItems)
        {
            int item_value = (int)item;
            int item_priority = 0;

            if (item_value >= a_value && item_value <= z_value)
            {
                item_priority = item_value - a_value + 1;
            }
            if (item_value >= A_value && item_value <= Z_value)
            {
                item_priority = item_value - A_value + 27;
            }
            totalPriority += item_priority;
        }
        return totalPriority;
    }
    public static void PartOne(string inputFileContents)
    {
        List<List<string>> rucksacks = [];
        string compartment1;
        string compartment2;

        foreach (var rucksack in inputFileContents.Split('\n'))
        {
            List<string> rucksackCompartments = [];
            compartment1 = rucksack.Substring(0, rucksack.Length / 2);
            compartment2 = rucksack.Substring(rucksack.Length / 2, rucksack.Length / 2);
            rucksackCompartments.Add(compartment1);
            rucksackCompartments.Add(compartment2);
            rucksacks.Add(rucksackCompartments);
        }

        List<char> overlappingItems = [];

        foreach (List<string> rucksackCompartments in rucksacks)
        {
            HashSet<char> compartment1Set = [];
            HashSet<char> compartment2Set = [];

            compartment1 = rucksackCompartments[0];
            compartment2 = rucksackCompartments[1];

            foreach (var item in compartment1)
            {
                compartment1Set.Add(item);
            }

            foreach (var item in compartment2)
            {
                compartment2Set.Add(item);
            }

            foreach (var item in compartment2Set)
            {
                if (compartment1Set.Contains(item))
                {
                    overlappingItems.Add(item);
                }
            }
        }
        int totalPriority = GetPrioritySum(overlappingItems);
        Console.WriteLine("totalPriority: " + totalPriority);

    }

    public static void PartTwo(string inputFileContents)
    {
        List<List<HashSet<char>>> elfGroups = [];
        int count = 0;
        List<HashSet<char>> elfGroup = [];

        foreach (string rucksack in inputFileContents.Split('\n'))
        {
            HashSet<char> rucksackSet = [];

            if (count == 0)
            {
                elfGroup = [];
            }

            foreach (char item in rucksack)
            {
                rucksackSet.Add(item);
            }

            elfGroup.Add(rucksackSet);
            if (count == 2)
            {
                elfGroups.Add(elfGroup);
            }
            count = (count + 1) % 3;
        }

        List<char> overlappingItems = [];

        foreach (List<HashSet<char>> tmpElfGroup in elfGroups)
        {
            HashSet<char> elf1Set = tmpElfGroup[0];
            HashSet<char> elf2Set = tmpElfGroup[1];
            HashSet<char> elf3Set = tmpElfGroup[2];

            foreach (char item in elf1Set)
            {
                if (elf2Set.Contains(item) && elf3Set.Contains(item))
                {
                    overlappingItems.Add(item);
                }
            }
        }

        int totalPriority = GetPrioritySum(overlappingItems);
        
        Console.WriteLine("totalPriority: " + totalPriority);
    }

    public static void Run()
    {
        string inputFileContents;
        // inputFileContents = GetInputFileContents("input/day_03/test.txt");
        inputFileContents = GetInputFileContents("input/day_03/input.txt");
        Console.WriteLine("Part One:");
        PartOne(inputFileContents);

        Console.WriteLine("Part Two:");
        PartTwo(inputFileContents);
    }
}