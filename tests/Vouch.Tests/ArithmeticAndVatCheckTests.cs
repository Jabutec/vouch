using Vouch.Core;
using Vouch.Core.Checks;
using Xunit;

namespace Vouch.Tests;

public class ArithmeticCheckTests
{
    private static readonly LineItem[] Sample01Lines =
    {
        new("Line-haul Johannesburg to Durban (trip)", 2, 12500m, 25000m),
        new("Fuel surcharge", 1, 2500m, 2500m),
    };

    private readonly ArithmeticCheck _check = new();

    [Fact]
    public void Clean_invoice_passes() // sample 01
    {
        var invoice = TestInvoices.Create(Sample01Lines, 27500m, 4125m, 31625m);
        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }

    [Fact]
    public void Subtotal_that_does_not_match_the_lines_fails() // sample 03
    {
        var invoice = TestInvoices.Create(Sample01Lines, 28500m, 4275m, 32775m);
        var result = _check.Run(invoice);

        Assert.Equal(CheckStatus.Fail, result.Status);
        Assert.Contains("27,500.00", result.Message);
    }

    [Fact]
    public void Wrong_vat_rate_is_not_an_arithmetic_problem() // sample 04
    {
        var invoice = TestInvoices.Create(Sample01Lines, 27500m, 4400m, 31900m);
        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }

    [Fact]
    public void Invoice_without_vat_passes() // sample 02
    {
        var lines = new LineItem[]
        {
            new("Lawn maintenance (visit)", 4, 450m, 1800m),
            new("Hedge trimming", 1, 900m, 900m),
            new("Refuse removal", 1, 500m, 500m),
        };
        var invoice = TestInvoices.Create(lines, 3200m, null, 3200m);

        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }

    [Fact]
    public void Total_that_does_not_match_fails()
    {
        var invoice = TestInvoices.Create(Sample01Lines, 27500m, 4125m, 31000m);
        Assert.Equal(CheckStatus.Fail, _check.Run(invoice).Status);
    }

    [Fact]
    public void One_cent_rounding_difference_is_tolerated()
    {
        var lines = new LineItem[] { new("Item", 3, 33.33m, 100.00m) }; // 3 x 33.33 = 99.99
        var invoice = TestInvoices.Create(lines, 100.00m, 15.00m, 115.00m);

        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }
}

public class VatRateCheckTests
{
    private static readonly LineItem[] Lines =
    {
        new("Line-haul Johannesburg to Durban (trip)", 2, 12500m, 25000m),
        new("Fuel surcharge", 1, 2500m, 2500m),
    };

    private readonly VatRateCheck _check = new();

    [Fact]
    public void Standard_rate_passes() // sample 01
    {
        var invoice = TestInvoices.Create(Lines, 27500m, 4125m, 31625m);
        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }

    [Fact]
    public void Wrong_rate_fails_and_says_what_it_should_be() // sample 04
    {
        var invoice = TestInvoices.Create(Lines, 27500m, 4400m, 31900m);
        var result = _check.Run(invoice);

        Assert.Equal(CheckStatus.Fail, result.Status);
        Assert.Contains("4,125.00", result.Message);
    }

    [Fact]
    public void No_vat_is_not_applicable() // sample 02
    {
        var invoice = TestInvoices.Create(Lines, 3200m, null, 3200m);
        Assert.Equal(CheckStatus.NotApplicable, _check.Run(invoice).Status);
    }

    [Fact]
    public void Half_cent_amounts_round_the_way_invoices_do()
    {
        // 15% of 5,450.00 is 817.50 exactly
        var invoice = TestInvoices.Create(Lines, 5450m, 817.50m, 6267.50m);
        Assert.Equal(CheckStatus.Pass, _check.Run(invoice).Status);
    }
}
