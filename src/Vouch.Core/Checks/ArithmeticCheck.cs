namespace Vouch.Core.Checks;

/// <summary>Checks that line items, subtotal, VAT and total agree with each other.</summary>
public class ArithmeticCheck : IBusinessCheck
{
    private const decimal Tolerance = 0.01m; // allow one cent of rounding

    public string Id => "document.arithmetic";

    public CheckResult Run(Invoice invoice)
    {
        var problems = new List<string>();

        foreach (var line in invoice.Lines)
        {
            var expected = line.Quantity * line.UnitPrice;
            if (Math.Abs(expected - line.Amount) > Tolerance)
                problems.Add($"Line '{line.Description}': {line.Quantity} x {MoneyText.Of(line.UnitPrice)} is {MoneyText.Of(expected)}, but the invoice shows {MoneyText.Of(line.Amount)}.");
        }

        var linesTotal = invoice.Lines.Sum(l => l.Amount);
        if (Math.Abs(linesTotal - invoice.Subtotal) > Tolerance)
            problems.Add($"Lines add up to {MoneyText.Of(linesTotal)}, but the subtotal is {MoneyText.Of(invoice.Subtotal)}.");

        var expectedTotal = invoice.Subtotal + (invoice.VatAmount ?? 0m);
        if (Math.Abs(expectedTotal - invoice.Total) > Tolerance)
            problems.Add($"Subtotal plus VAT is {MoneyText.Of(expectedTotal)}, but the total is {MoneyText.Of(invoice.Total)}.");

        return problems.Count == 0
            ? CheckResult.Pass(Id, "Line items, subtotal, VAT and total are consistent.")
            : CheckResult.Fail(Id, string.Join(" ", problems));
    }
}
