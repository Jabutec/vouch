namespace Vouch.Core;

/// <summary>One supplier invoice, in the shape every check works with.</summary>
public record Invoice(
    string InvoiceNumber,
    DateOnly InvoiceDate,
    DateOnly? DueDate,
    string DocumentTitle,                 // "TAX INVOICE" or "INVOICE"
    Supplier Supplier,
    Buyer Buyer,
    IReadOnlyList<LineItem> Lines,
    decimal Subtotal,                     // as written on the invoice
    decimal? VatAmount,                   // null when no VAT is shown
    decimal Total,                        // as written on the invoice
    BankDetails Bank,
    IReadOnlyList<string> Notes);         // free text, e.g. "banking details have changed"

public record Supplier(
    string Name,
    string? RegistrationNumber,           // CIPC number; null for sole proprietors
    string? VatNumber,                    // null if not VAT registered
    string Address,
    string Email,
    string Phone);

public record Buyer(
    string Name,
    string Address,
    string? VatNumber);

public record LineItem(
    string Description,
    decimal Quantity,
    decimal UnitPrice,
    decimal Amount);

public record BankDetails(
    string AccountHolder,
    string BankName,
    string BranchCode,
    string AccountNumber);
