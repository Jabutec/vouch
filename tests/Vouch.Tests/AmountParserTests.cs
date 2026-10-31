using System.Globalization;
using Vouch.Core;
using Xunit;

namespace Vouch.Tests;

public class AmountParserTests
{
    [Theory]
    [InlineData("R52300", "52300")]
    [InlineData("R 52,300.00", "52300.00")]
    [InlineData("R 40 000,00", "40000.00")]
    [InlineData("R20000", "20000")]
    [InlineData("R 6,000.00", "6000.00")]
    [InlineData("R 52 900,00", "52900.00")]
    [InlineData("27500", "27500")]
    [InlineData("R 1,500", "1500")]
    [InlineData("R 1,50", "1.50")]
    [InlineData("R 12.5", "12.5")]
    [InlineData("R1 234 567,89", "1234567.89")]
    [InlineData("R 1,234,567.89", "1234567.89")]
    [InlineData("-R 100.00", "-100.00")]
    [InlineData("R 40\u00A0000,00", "40000.00")] // non-breaking space
    public void Parses_valid_amounts(string input, string expected)
    {
        Assert.True(AmountParser.TryParse(input, out var actual));
        Assert.Equal(decimal.Parse(expected, CultureInfo.InvariantCulture), actual);
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    [InlineData("abc")]
    [InlineData("R")]
    [InlineData("R 12 abc")]
    [InlineData("R 1,2,3.4.5")]
    [InlineData("12-5")]
    public void Rejects_invalid_amounts(string? input)
    {
        Assert.False(AmountParser.TryParse(input, out _));
    }
}
