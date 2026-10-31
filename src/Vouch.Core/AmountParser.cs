using System.Globalization;
using System.Text;

namespace Vouch.Core;

/// <summary>
/// Turns invoice amount text such as "R52300", "R 52,300.00" or "R 40 000,00" into a decimal.
/// </summary>
public static class AmountParser
{
    public static bool TryParse(string? text, out decimal value)
    {
        value = 0m;
        if (string.IsNullOrWhiteSpace(text)) return false;

        // Drop the currency marker.
        var s = text.Replace("ZAR", "", StringComparison.OrdinalIgnoreCase)
                    .Replace("R", "", StringComparison.OrdinalIgnoreCase);

        // Keep digits, "," and "." and an optional leading minus. Spaces (including
        // non-breaking ones) are thousands separators on many SA invoices, so they are skipped.
        var negative = false;
        var cleaned = new StringBuilder();
        foreach (var c in s)
        {
            if (c is >= '0' and <= '9' || c == ',' || c == '.') cleaned.Append(c);
            else if (char.IsWhiteSpace(c)) continue;
            else if (c == '-' && cleaned.Length == 0 && !negative) negative = true;
            else return false; // any other character means this is not a plain amount
        }

        var raw = cleaned.ToString();
        if (!raw.Any(c => c is >= '0' and <= '9')) return false;

        var decimalSeparator = FindDecimalSeparator(raw);
        if (decimalSeparator is char d && raw.Count(c => c == d) != 1) return false;

        // Rebuild the number with "." as the decimal point and no thousands separators.
        var normalised = new StringBuilder();
        foreach (var c in raw)
        {
            if (c is >= '0' and <= '9') normalised.Append(c);
            else if (c == decimalSeparator) normalised.Append('.');
            // any other "," or "." is a thousands separator: skip it
        }

        if (!decimal.TryParse(normalised.ToString(), NumberStyles.AllowDecimalPoint,
                CultureInfo.InvariantCulture, out var parsed))
            return false;

        value = negative ? -parsed : parsed;
        return true;
    }

    // Works out which of "," or "." is the decimal separator, or null if there is none.
    private static char? FindDecimalSeparator(string raw)
    {
        var lastComma = raw.LastIndexOf(',');
        var lastDot = raw.LastIndexOf('.');

        // Both present: the one that comes last is the decimal separator ("6,000.00" or "6.000,00").
        if (lastComma >= 0 && lastDot >= 0) return lastComma > lastDot ? ',' : '.';

        // Only one kind present.
        var separator = lastComma >= 0 ? ',' : lastDot >= 0 ? '.' : (char?)null;
        if (separator is null) return null;

        var occurrences = raw.Count(c => c == separator);
        var digitsAfter = raw.Length - raw.LastIndexOf(separator.Value) - 1;

        // "1,500" is a thousands separator; "1,50" and "12.5" are decimals. Repeated ones are thousands.
        return occurrences == 1 && digitsAfter != 3 ? separator : null;
    }
}
