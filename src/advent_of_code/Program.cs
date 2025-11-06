// Main entry point for running Advent of Code solutions
// Usage: dotnet run -- <day_number>
// Example: dotnet run -- 3

if (args.Length == 0)
{
    Console.WriteLine("Usage: dotnet run -- <day_number>");
    Console.WriteLine("Example: dotnet run -- 3");
    Environment.Exit(1);
}

string dayNumber = args[0].PadLeft(2, '0');
string dayScript = $"src/advent_of_code/day_{dayNumber}/main.cs";

if (!File.Exists(dayScript))
{
    Console.WriteLine($"Error: Could not find {dayScript}");
    Environment.Exit(1);
}

Console.WriteLine($"Running Day {dayNumber} solution:");
Console.WriteLine(new string('=', 40));

// Execute the day's solution
// Since we can't dynamically compile and run, we'll need to refactor
// this to call into compiled code. For now, let's use a switch statement.

switch (int.Parse(args[0]))
{
    case 3:
        Day03.Run();
        break;
    case 4:
        Day04.Run();
        break;
    default:
        Console.WriteLine($"Day {args[0]} not yet implemented");
        break;
}
