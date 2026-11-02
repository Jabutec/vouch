using Vouch.Core;

namespace Vouch.Tests;

internal static class TestInvoices
{
    public static Invoice Create(IReadOnlyList<LineItem> lines, decimal subtotal, decimal? vat, decimal total) =>
        new(
            InvoiceNumber: "TEST-1",
            InvoiceDate: new DateOnly(2026, 10, 15),
            DueDate: null,
            DocumentTitle: vat is null ? "INVOICE" : "TAX INVOICE",
            Supplier: new Supplier("Test Supplier (Pty) Ltd", "2016/204871/07", "4120987654",
                "1 Test Street", "accounts@test.example", "000 000 0000"),
            Buyer: new Buyer("Test Buyer (Pty) Ltd", "2 Test Road", null),
            Lines: lines,
            Subtotal: subtotal,
            VatAmount: vat,
            Total: total,
            Bank: new BankDetails("Test Supplier (Pty) Ltd", "Sample Bank", "123456", "1234567890"),
            Notes: []);
}
