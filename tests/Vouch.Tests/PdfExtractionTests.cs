using UglyToad.PdfPig;
using Xunit;

namespace Vouch.Tests;

public class PdfExtractionTests
{
    // Walks up from the build folder until it finds the repo's samples folder
    private static string SamplePath(string name)
    {
        var dir = new DirectoryInfo(AppContext.BaseDirectory);
        while (dir is not null && !Directory.Exists(Path.Combine(dir.FullName, "samples")))
            dir = dir.Parent;
        return Path.Combine(dir!.FullName, "samples", name);
    }

    [Fact]
    public void Sample01_text_contains_invoice_number_and_supplier()
    {
        using var doc = PdfDocument.Open(SamplePath("01-clean-company-vat.pdf"));
        var text = string.Join("\n", doc.GetPages().Select(p => p.Text));

        Assert.Contains("INV-2026-0412", text);
        Assert.Contains("Northgate Demo Freight", text);
    }
}