#!/usr/bin/env python3
"""Generate synthetic Vouch sample invoices (PDF with text layer) plus expected results.

All entities, numbers and bank details are FICTIONAL. Run from the repo root:

    pip install reportlab
    python tools/generate_samples.py

Outputs go to samples/ (PDFs, *.expected.json, manifest.json).
"""
import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent.parent / "samples"
OUT.mkdir(exist_ok=True)

# ---------- money formatting helpers (South African invoices vary) ----------
def std(x):   return f"R {x:,.2f}"                                   # R 27,500.00
def sa(x):    return "R " + f"{x:,.2f}".replace(",", " ").replace(".", ",")  # R 27 500,00
def raw(x):   return f"R{x:.0f}"                                     # R27500

BUYER = {"name": "Demo Buyer (Pty) Ltd", "address": "45 Example Avenue, Sandton, 2196", "vat": "4990011223"}

SUPPLIER_A = {"name": "Northgate Demo Freight (Pty) Ltd", "reg": "2016/204871/07", "vat": "4120987654",
              "address": "12 Sample Street, Midrand, 1685", "email": "accounts@northgatedemo.example",
              "phone": "+27 11 555 0100"}
BANK_A = {"holder": "Northgate Demo Freight (Pty) Ltd", "bank": "Sample Bank", "branch": "123456", "account": "1234567890"}

KEYS = ["document.requiredFields", "document.arithmetic", "document.vatRate", "format.cipc", "format.vat",
        "format.bank", "consistency.accountHolder", "consistency.emailDomain", "redflags.language",
        "registry.cipcStatus", "vat.vendorMatch", "payment.bankChange", "history.duplicate", "history.firstSeen"]

def base_expected(**over):
    e = {"document.requiredFields": "pass", "document.arithmetic": "pass", "document.vatRate": "pass",
         "format.cipc": "pass", "format.vat": "pass", "format.bank": "pass",
         "consistency.accountHolder": "pass", "consistency.emailDomain": "pass", "redflags.language": "pass",
         "registry.cipcStatus": "unverified", "vat.vendorMatch": "unverified",
         "payment.bankChange": "notApplicable", "history.duplicate": "pass", "history.firstSeen": "warn"}
    e.update(over)
    assert set(e) == set(KEYS)
    return e

def lines(rows, f=std):
    """rows: (description, qty, unit_price) -> display dicts and numeric sum"""
    out, total = [], 0.0
    for d, q, u in rows:
        amt = q * u
        total += amt
        out.append({"desc": d, "qty": str(q), "unit": f(u), "amount": f(amt)})
    return out, total

def vat_totals(sub, f=std, rate=0.15, vat_override=None, sub_override=None):
    s = sub_override if sub_override is not None else sub
    v = vat_override if vat_override is not None else round(s * rate, 2)
    return {"subtotal": f(s), "vat": f(v), "total": f(s + v)}, {"subtotal": s, "vat": v, "total": round(s + v, 2)}

CASES = []

def add(cid, title, supplier, inv_no, date, due, rows, totals_str, totals_num, bank, notes, expected,
        context="isolated", seed=None, formatter=std, vat_note=None, line_items=None, desc=""):
    CASES.append(dict(id=cid, title=title, supplier=supplier, inv_no=inv_no, date=date, due=due, rows=rows,
                      totals_str=totals_str, totals_num=totals_num, bank=bank, notes=notes, expected=expected,
                      context=context, seed=seed or [], vat_note=vat_note, line_items=line_items, desc=desc))

# 01 clean company, VAT vendor
li, s = lines([("Line-haul Johannesburg to Durban (trip)", 2, 12500.0), ("Fuel surcharge", 1, 2500.0)])
ts, tn = vat_totals(s)
add("01-clean-company-vat", "TAX INVOICE", SUPPLIER_A, "INV-2026-0412", "2026-10-15", "2026-11-14", None, ts, tn, BANK_A,
    ["Payment terms: 30 days from invoice date.", "Please use the invoice number as payment reference."],
    base_expected(), line_items=li, desc="Clean company invoice from a VAT vendor. Everything consistent.")

# 02 clean sole proprietor (no VAT, no CIPC)
li, s = lines([("Lawn maintenance (visit)", 4, 450.0), ("Hedge trimming", 1, 900.0), ("Refuse removal", 1, 500.0)])
add("02-clean-sole-proprietor", "INVOICE",
    {"name": "Sample Garden Services (owner: J Example)", "reg": None, "vat": None,
     "address": "8 Demo Road, Meyerton, 1960", "email": "jexample.gardens@gmail.com", "phone": "+27 82 555 0123"},
    "SG-0031", "2026-10-12", "2026-10-26", None, {"subtotal": std(s), "vat": None, "total": std(s)},
    {"subtotal": s, "vat": None, "total": s},
    {"holder": "J Example", "bank": "Sample Bank", "branch": "123456", "account": "4440002222"},
    ["Not registered for VAT."],
    base_expected(**{"document.vatRate": "notApplicable", "format.cipc": "notApplicable", "format.vat": "notApplicable",
                     "consistency.emailDomain": "notApplicable", "registry.cipcStatus": "notApplicable",
                     "vat.vendorMatch": "notApplicable"}),
    line_items=li, desc="Legitimate sole proprietor: no CIPC number, no VAT, plain invoice. Must NOT be flagged for missing VAT.")

# 03 arithmetic wrong (subtotal does not equal sum of lines)
li, s = lines([("Line-haul Johannesburg to Durban (trip)", 2, 12500.0), ("Fuel surcharge", 1, 2500.0)])
ts, tn = vat_totals(s, sub_override=28500.0)
add("03-arithmetic-wrong-subtotal", "TAX INVOICE", SUPPLIER_A, "INV-2026-0420", "2026-10-16", "2026-11-15", None, ts, tn, BANK_A,
    ["Payment terms: 30 days from invoice date."], base_expected(**{"document.arithmetic": "fail"}),
    line_items=li, desc="Lines sum to R27,500.00 but the subtotal states R28,500.00. VAT is consistent with the stated subtotal.")

# 04 VAT rate wrong
li, s = lines([("Line-haul Johannesburg to Durban (trip)", 2, 12500.0), ("Fuel surcharge", 1, 2500.0)])
ts, tn = vat_totals(s, vat_override=4400.0)
add("04-vat-rate-wrong", "TAX INVOICE", SUPPLIER_A, "INV-2026-0421", "2026-10-16", "2026-11-15", None, ts, tn, BANK_A,
    ["Payment terms: 30 days from invoice date."], base_expected(**{"document.vatRate": "fail"}),
    line_items=li, desc="VAT charged is 16% of the subtotal instead of the standard rate. Totals are otherwise consistent.")

# 05 charges VAT but no VAT number
SUP_B = {"name": "Ridgeback Demo Print (Pty) Ltd", "reg": "2019/456123/07", "vat": None,
         "address": "3 Test Lane, Edenvale, 1609", "email": "billing@ridgebackdemo.example", "phone": "+27 11 555 0200"}
li, s = lines([("Flyers A5 (each)", 500, 4.0), ("Pull-up banner", 2, 750.0)])
ts, tn = vat_totals(s)
add("05-vat-charged-no-vat-number", "TAX INVOICE", SUP_B, "RB-2207", "2026-10-14", "2026-11-13", None, ts, tn,
    {"holder": "Ridgeback Demo Print (Pty) Ltd", "bank": "Sample Bank", "branch": "123456", "account": "5550001111"},
    ["Payment terms: 30 days."],
    base_expected(**{"document.requiredFields": "fail", "format.vat": "fail"}),
    line_items=li, desc="Labelled a tax invoice and charges VAT, but shows no supplier VAT number.")

# 06 malformed CIPC number
SUP_C = {"name": "Coastline Demo Supplies (Pty) Ltd", "reg": "2018/12345/07", "vat": "4301122334",
         "address": "77 Harbour Road, Durban, 4001", "email": "accounts@coastlinedemo.example", "phone": "+27 31 555 0300"}
li, s = lines([("Packaging materials (box)", 40, 125.0), ("Delivery", 1, 450.0)])
ts, tn = vat_totals(s)
add("06-malformed-cipc", "TAX INVOICE", SUP_C, "CS-90114", "2026-10-13", "2026-11-12", None, ts, tn,
    {"holder": "Coastline Demo Supplies (Pty) Ltd", "bank": "Sample Bank", "branch": "123456", "account": "6660003333"},
    ["Payment terms: 30 days."], base_expected(**{"format.cipc": "fail"}),
    line_items=li, desc="CIPC number has 5 digits in the middle block instead of 6 (format YYYY/NNNNNN/TT).")

# 07 name mismatch: account holder and email domain differ from supplier name
SUP_D = {"name": "Summit Demo Tools (Pty) Ltd", "reg": "2014/998877/07", "vat": "4777788899",
         "address": "19 Workshop Street, Boksburg, 1459", "email": "billing@quickpay-invoices.example", "phone": "+27 11 555 0400"}
li, s = lines([("Power tool set", 3, 2800.0)])
ts, tn = vat_totals(s)
add("07-name-mismatch", "TAX INVOICE", SUP_D, "SDT-5521", "2026-10-17", "2026-11-16", None, ts, tn,
    {"holder": "Karabo Example Trading", "bank": "Sample Bank", "branch": "123456", "account": "7770004444"},
    ["Payment terms: 30 days."],
    base_expected(**{"consistency.accountHolder": "fail", "consistency.emailDomain": "warn"}),
    line_items=li, desc="Bank account holder is a different name from the supplier, and the email domain does not match the company.")

# 08 bank changed + urgent language (history from file 01)
li, s = lines([("Line-haul Johannesburg to Durban (trip)", 2, 12500.0)])
ts, tn = vat_totals(s)
add("08-bank-changed-urgent", "TAX INVOICE", SUPPLIER_A, "INV-2026-0455", "2026-10-27", "2026-10-28", None, ts, tn,
    {"holder": "Northgate Demo Freight (Pty) Ltd", "bank": "Other Demo Bank", "branch": "654321", "account": "9876543210"},
    ["IMPORTANT: Our banking details have changed. Please pay into the new account below.",
     "URGENT: payment required within 24 hours to avoid suspension of services."],
    base_expected(**{"redflags.language": "warn", "payment.bankChange": "fail", "history.firstSeen": "pass"}),
    context="after", seed=["01-clean-company-vat.pdf"], line_items=li,
    desc="Same supplier as file 01 but a different bank account, with change-of-details and urgency wording.")

# 09 duplicate of file 01
li, s = lines([("Line-haul Johannesburg to Durban (trip)", 2, 12500.0), ("Fuel surcharge", 1, 2500.0)])
ts, tn = vat_totals(s)
add("09-duplicate-invoice", "TAX INVOICE", SUPPLIER_A, "INV-2026-0412", "2026-10-20", "2026-11-19", None, ts, tn, BANK_A,
    ["Payment terms: 30 days from invoice date.", "Reminder: this invoice is still outstanding."],
    base_expected(**{"history.duplicate": "fail", "history.firstSeen": "pass", "payment.bankChange": "pass"}),
    context="after", seed=["01-clean-company-vat.pdf"], line_items=li,
    desc="Same supplier, invoice number and amounts as file 01, resent on a later date.")

# 10 messy amount formats (all correct, tests parsing)
SUP_E = {"name": "Highveld Demo Catering (Pty) Ltd", "reg": "2012/334455/07", "vat": "4556677889",
         "address": "5 Banquet Close, Pretoria, 0001", "email": "accounts@highveldcatering-demo.example",
         "phone": "+27 12 555 0500"}
li = [{"desc": "Catering (day)", "qty": "2", "unit": raw(20000), "amount": sa(40000)},
      {"desc": "Equipment hire", "qty": "1", "unit": std(6000), "amount": std(6000)}]
ts = {"subtotal": sa(46000), "vat": sa(6900), "total": sa(52900)}
tn = {"subtotal": 46000.0, "vat": 6900.0, "total": 52900.0}
add("10-messy-amount-formats", "TAX INVOICE", SUP_E, "HC-1188", "2026-10-18", "2026-11-17", None, ts, tn,
    {"holder": "Highveld Demo Catering (Pty) Ltd", "bank": "Sample Bank", "branch": "123456", "account": "8880005555"},
    ["Amount due: R52900 by EFT."], base_expected(), line_items=li,
    desc="Correct invoice using mixed formats (R20000, R 40 000,00, R 6,000.00, R52900). Tests amount parsing.")

# ---------- rendering ----------
W, H = A4
M = 50

def render(c, case):
    s, inv = case["supplier"], case
    y = H - 60
    c.setFont("Helvetica-Bold", 14); c.drawString(M, y, s["name"]); y -= 16
    c.setFont("Helvetica", 9)
    for t in [s["address"], f"Tel: {s['phone']}   Email: {s['email']}"]:
        c.drawString(M, y, t); y -= 12
    if s["reg"]: c.drawString(M, y, f"Registration No: {s['reg']}"); y -= 12
    if s["vat"]: c.drawString(M, y, f"VAT No: {s['vat']}"); y -= 12
    c.setFont("Helvetica-Bold", 18); c.drawRightString(W - M, H - 60, case["title"])
    c.setFont("Helvetica", 10)
    c.drawRightString(W - M, H - 80, f"Invoice No: {case['inv_no']}")
    c.drawRightString(W - M, H - 94, f"Date: {case['date']}")
    c.drawRightString(W - M, H - 108, f"Due date: {case['due']}")
    y -= 14
    c.setFont("Helvetica-Bold", 10); c.drawString(M, y, "Bill to:"); y -= 13
    c.setFont("Helvetica", 10)
    for t in [BUYER["name"], BUYER["address"], f"VAT No: {BUYER['vat']}"]:
        c.drawString(M, y, t); y -= 12
    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(M, y, "Description"); c.drawString(330, y, "Qty"); c.drawRightString(440, y, "Unit price"); c.drawRightString(W - M, y, "Amount")
    y -= 4; c.line(M, y, W - M, y); y -= 14
    c.setFont("Helvetica", 10)
    for li in case["line_items"]:
        c.drawString(M, y, li["desc"]); c.drawString(330, y, li["qty"])
        c.drawRightString(440, y, li["unit"]); c.drawRightString(W - M, y, li["amount"]); y -= 14
    y -= 4; c.line(M, y, W - M, y); y -= 16
    t = case["totals_str"]
    c.drawRightString(440, y, "Subtotal:"); c.drawRightString(W - M, y, t["subtotal"]); y -= 14
    if t["vat"] is not None:
        c.drawRightString(440, y, "VAT:"); c.drawRightString(W - M, y, t["vat"]); y -= 14
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(440, y, "Total due:"); c.drawRightString(W - M, y, t["total"]); y -= 28
    c.setFont("Helvetica-Bold", 10); c.drawString(M, y, "Banking details"); y -= 13
    c.setFont("Helvetica", 10)
    b = case["bank"]
    for line in [f"Account holder: {b['holder']}", f"Bank: {b['bank']}", f"Branch code: {b['branch']}", f"Account number: {b['account']}"]:
        c.drawString(M, y, line); y -= 12
    y -= 10
    for n in case["notes"]:
        c.drawString(M, y, n); y -= 12
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(M, 40, "SYNTHETIC TEST DATA - fictional entities and numbers - not a real invoice.")

def level0(expected):
    for k, v in expected.items():
        if k.split(".")[0] in ("document", "format", "consistency", "redflags") and v == "fail":
            return "none"
    return 0

def main():
    manifest = []
    for case in CASES:
        fname = case["id"] + ".pdf"
        c = canvas.Canvas(str(OUT / fname), pagesize=A4)
        c.setTitle(f"{case['title']} {case['inv_no']}")
        c.setAuthor(case["supplier"]["name"])
        c.setCreator("Vouch sample generator")
        render(c, case); c.save()
        exp = {
            "file": fname,
            "description": case["desc"],
            "context": {"mode": case["context"], "seedHistoryFrom": case["seed"]},
            "supplierType": "company" if case["supplier"]["reg"] else "soleProprietor",
            "expectedParsed": {
                "supplierName": case["supplier"]["name"], "cipc": case["supplier"]["reg"], "vatNumber": case["supplier"]["vat"],
                "invoiceNumber": case["inv_no"], "invoiceDate": case["date"],
                "subtotal": case["totals_num"]["subtotal"], "vatAmount": case["totals_num"]["vat"],
                "total": case["totals_num"]["total"], "bankAccount": case["bank"]["account"],
            },
            "expected": case["expected"],
            "highestLevelReached": level0(case["expected"]),
        }
        (OUT / (case["id"] + ".expected.json")).write_text(json.dumps(exp, indent=2) + "\n", encoding="utf-8")
        manifest.append({"file": fname, "expected": case["id"] + ".expected.json", "heldBack": False})
    (OUT / "manifest.json").write_text(json.dumps({"runOrder": manifest}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(CASES)} samples to {OUT}")

if __name__ == "__main__":
    main()
