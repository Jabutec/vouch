using System.Globalization;

namespace Vouch.Core.Checks;

internal static class MoneyText
{
    // Always "27,500.00" regardless of the computer's regional settings.
    public static string Of(decimal value) => value.ToString("N2", CultureInfo.InvariantCulture);
}
