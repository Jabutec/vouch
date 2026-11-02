namespace Vouch.Core.Checks;

/// <summary>Checks that the VAT charged is the standard rate applied to the subtotal.</summary>
public class VatRateCheck : IBusinessCheck
{
    // Standard South African VAT rate. Confirm against SARS before relying on it.
    public const decimal StandardRate = 0.15m;
    private const decimal Tolerance = 0.01m;

    public string Id => "document.vatRate";

    public CheckResult Run(Invoice invoice)
    {
        if (invoice.VatAmount is not decimal vat)
            return CheckResult.NotApplicable(Id, "No VAT is charged on this invoice.");

        var expected = Math.Round(invoice.Subtotal * StandardRate, 2, MidpointRounding.AwayFromZero);

        return Math.Abs(vat - expected) <= Tolerance
            ? CheckResult.Pass(Id, $"VAT of {MoneyText.Of(vat)} matches {StandardRate:P0} of the subtotal.")
            : CheckResult.Fail(Id, $"VAT shown is {MoneyText.Of(vat)}, but {StandardRate:P0} of the subtotal ({MoneyText.Of(invoice.Subtotal)}) is {MoneyText.Of(expected)}.");
    }
}
