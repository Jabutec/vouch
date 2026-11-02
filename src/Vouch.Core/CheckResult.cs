namespace Vouch.Core;

public enum CheckStatus { Pass, Warn, Fail, Unverified, NotApplicable }

/// <summary>The outcome of one check: a status plus a plain-English message.</summary>
public record CheckResult(string CheckId, CheckStatus Status, string Message)
{
    public static CheckResult Pass(string id, string message) => new(id, CheckStatus.Pass, message);
    public static CheckResult Warn(string id, string message) => new(id, CheckStatus.Warn, message);
    public static CheckResult Fail(string id, string message) => new(id, CheckStatus.Fail, message);
    public static CheckResult Unverified(string id, string message) => new(id, CheckStatus.Unverified, message);
    public static CheckResult NotApplicable(string id, string message) => new(id, CheckStatus.NotApplicable, message);
}

/// <summary>Every check implements this, so new checks plug in without changing anything else.</summary>
public interface IBusinessCheck
{
    string Id { get; }
    CheckResult Run(Invoice invoice);
}
