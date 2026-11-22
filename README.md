# Product Complaint Form: white-label and multilingual

A user-friendly product complaint form for construction-chemical manufacturers and their dealers.
It is **one HTML file**: no server, no installation, works on phone and desktop.

**▶ Live demo:** https://corpsebride999.github.io/complaint-form/

## Features
- **EN / TR / RU** interface, switchable at any time
- **Auto-translation** of free text: the customer writes in their own language, and you read it in yours. The original is always kept
- **Remembers the customer's company details** on their device. A new complaint keeps them, and they can be edited at any time
- **Label photo → auto-fill**: batch / order no, product code, product, production and expiry dates, and pack size are read from the photo (Tesseract.js OCR). Read fields are highlighted for checking
- **Smart classification**: the customer describes the problem in their own words, and the form picks the product group and complaint types automatically. If several groups fit (for example interior or exterior paint), it asks
- **Problem packages**: pack sizes × units, with a base / colour column for paints and a "whole batch affected" option
- 10 product groups and 90 complaint types built in (paints, decorative plasters, tile adhesives, grouts, waterproofing, repair mortars, floor coatings, ETICS, sealants, additives)
- Up to **10 photos**, compressed automatically
- **Save PDF**, **Save HTML** (a complete copy that can be reopened and continued) or **Send by e-mail** to a chosen recipient
- **⚙ Customize**: your company name, logo, colour, e-mail recipients, complaint number prefix
- **Your own product groups & complaint types**: download the Excel template, edit it, upload it

## Brand it for your company
**Without coding:** open the form → ⚙ Customize → set your name, logo and recipients, and upload your Excel list.

**As a ready file to send customers (Python 3):**
```bash
cp config/example.config.json config/mycompany.config.json   # edit brand, recipients, "allowCustomize": false, "output"
python build.py config/mycompany.config.json                  # → one self-contained HTML file
```
Optional:
- **Your own groups and products:** copy `taxonomy/default.groups.json`, add `"products": [{"code":"1234","name":"My Product"}]` to the groups, and point `"groups"` in your config at the copy.
- **Label reading rules:** in your config, `"ocr": {"batch": ["regex…"], "code": ["regex…"]}` tells the form where your labels print the batch no and product code.

Complaint types live in `taxonomy/type-library.tsv`: `id | English | Türkçe | Русский | keywords`.

Private configs, `private/` and `dist/` are git-ignored, so your company and customer data stay off GitHub.

## Privacy
Everything stays in the user's browser. Nothing is sent anywhere until the user saves a PDF or chooses to e-mail it.
Online services are only used for label reading (Tesseract.js from jsDelivr), PDF creation (html2pdf.js) and auto-translation.

## License
MIT
