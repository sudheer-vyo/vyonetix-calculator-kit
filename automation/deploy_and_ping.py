"""Vyonetix local release compiler and explicit, verified IndexNow submission.

No production upload, WordPress injection, social posting or push broadcast occurs.
Commands: build, audit, indexnow. IndexNow is never called by build.
Only the fixed, independently tested formula keys below are executable.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import http.client
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://deals.vyonetixsolutions.com.au"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
MARKETS = {
    "AU": ["https://www.amazon.com.au", "vyonetixsave-22"],
    "US": ["https://www.amazon.com", "vyonetix20-20"],
    "UK": ["https://www.amazon.co.uk", "vyonetix20-21"],
    "CA": ["https://www.amazon.ca", "vyonetix2003-20"],
}
BROTHER_SOURCE = "https://www.brother.com.au/-/media/ap2/Australia/Products/Common/Brochures/HL-L2400DW---Brochure.pdf?rev=c36e4868ddd942438fc2a4ec67257c7a"


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_public(url: str) -> tuple[int, bytes, str]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != urllib.parse.urlsplit(BASE).netloc:
        raise ValueError("Only the canonical Vyonetix HTTPS host can be requested")
    req = urllib.request.Request(url, headers={"User-Agent": "VyonetixReleaseValidator/1.0", "Accept-Encoding": "identity", "Connection": "close"})
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            if urllib.parse.urlsplit(response.url).netloc != parsed.netloc:
                raise ValueError("Unexpected cross-host redirect")
            body = response.read()
            if len(body) > 2_000_000:
                raise ValueError("Response exceeds audit size limit")
            return response.status, body, response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        return exc.code, b"", exc.headers.get("Content-Type", "")


def audit_feeds() -> dict:
    receipt = {"checked_at": datetime.now(timezone.utc).isoformat(), "checks": []}
    for path in ["/tools/feed.xml", "/tools/feed.json", "/tools/tools-rss.xml", "/tools/vyonetix-feeds.opml", "/tools/sitemap.xml"]:
        try:
            status, body, mime = get_public(BASE + path)
        except (OSError, ValueError, http.client.HTTPException) as exc:
            receipt["checks"].append({"url": BASE + path, "status": None, "error": type(exc).__name__ + ": " + str(exc)})
            continue
        check = {"url": BASE + path, "status": status, "content_type": mime, "bytes": len(body)}
        if status == 200:
            try:
                if path.endswith(".json"):
                    data = json.loads(body)
                    check["items"] = len(data.get("items", []))
                else:
                    doc = ET.fromstring(body)
                    check["root"] = doc.tag
                    check["items"] = len(doc.findall("./channel/item"))
                    if path.endswith(".opml"):
                        check["advertised_feeds"] = [n.attrib.get("xmlUrl") for n in doc.findall("./body/outline")]
                check["parse"] = "pass"
            except (ValueError, ET.ParseError) as exc:
                check["parse"] = "fail: " + str(exc)
        receipt["checks"].append(check)
    return receipt


def registry() -> dict:
    """Original factual reference transcription; only the freshly checked AU record."""
    return {
        "schema_version": "1.0", "reviewed_at": "2026-10-29", "licence_scope": "Original schema and code are MIT; manufacturer trademarks and source documents are not relicensed.",
        "records": [{"id": "brother-hl-l2400dw-au", "brand": "Brother", "model": "HL-L2400DW", "market": "AU",
                     "aliases": ["HL L2400DW", "HLL2400DW", "Brother HL-L2400DW"],
                     "source_url": BROTHER_SOURCE, "source_name": "Brother Australia brochure, consumables and footnotes",
                     "parts": [{"part": "TN2530", "kind": "standard toner", "rated_pages": 1200},
                               {"part": "TN2530XL", "kind": "high-yield toner", "rated_pages": 3000},
                               {"part": "DR2530", "kind": "drum", "rated_pages": 15000}],
                     "limits": "Rated toner yield uses the manufacturer's test conditions. Drum rating assumes one page per job. No remaining-supply measurement or replacement diagnosis."}],
    }


def normalise(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def batch_report(input_path: Path, records: dict) -> dict:
    with input_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"model", "market", "pages_per_month"}.issubset(reader.fieldnames):
            raise ValueError("CSV requires model, market, pages_per_month columns")
        rows = list(reader)
    results = []
    for number, row in enumerate(rows, 2):
        model, market = row["model"].strip(), row["market"].strip().upper()
        matches = [r for r in records["records"] if r["market"] == market and normalise(model) in {normalise(x) for x in [r["model"], *r["aliases"]]}]
        result = {"row": number, "model": model, "market": market, "status": "unresolved", "reason": "Exact supported model and market required"}
        try:
            pages = float(row["pages_per_month"])
            if not 0 < pages <= 10_000_000 or pages != pages:
                raise ValueError("Workload must be finite and positive")
        except (TypeError, ValueError, OverflowError):
            result.update(status="invalid", reason="pages_per_month must be finite and positive")
            results.append(result)
            continue
        if len(matches) == 1:
            record = matches[0]
            xl = next(p for p in record["parts"] if p["kind"] == "high-yield toner")
            result.update(status="matched_reference", reason="Exact normalized model and explicit market matched the sourced record", part=xl["part"], pages_per_month=pages,
                          rated_pages=xl["rated_pages"], illustrative_months=xl["rated_pages"] / pages, source_url=record["source_url"],
                          limits=record["limits"], tool_url=BASE + "/tools/printer-supply-toolbox/?" + urllib.parse.urlencode({"market": "AU", "brand": "Brother", "model": "HL-L2400DW", "part": "TN2530XL"}))
        results.append(result)
    return {"privacy": "Processed locally. Do not share reports containing confidential equipment data.", "rows": results,
            "matched": sum(r["status"] == "matched_reference" for r in results), "unresolved": sum(r["status"] == "unresolved" for r in results),
            "invalid": sum(r["status"] == "invalid" for r in results)}


def generate_tool_html(tool: dict, campaign: str = "") -> str:
    if tool.get("formula_key") != "thermal_roll_yield":
        raise ValueError("Only reviewed formula_key thermal_roll_yield is currently supported; raw formula_js is not executed")
    slug = tool["slug"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Invalid slug")
    config = json.dumps({"slug": slug, "markets": MARKETS, "campaign": campaign if re.fullmatch(r"\d{6,20}", campaign) else ""}).replace("<", "\\u003c")
    title = html.escape(tool["title"])
    template = '''<!doctype html><html lang="en-AU"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>__TITLE__</title>
<style>body{font:17px system-ui;background:#f5f0fa;color:#242044;margin:0}main{max-width:1000px;margin:auto;padding:24px}header{background:linear-gradient(120deg,#192c4d,#703d8f);color:white;border-radius:22px;padding:30px;position:relative;overflow:hidden}header svg{float:right;width:130px;opacity:.75}h1{font-size:clamp(30px,5vw,48px);line-height:1.1}section{background:linear-gradient(130deg,#faf6ff,#eee0fb);border:1px solid #bca5d5;border-top:5px solid #7c3aed;border-radius:16px;padding:22px;margin-top:18px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}label{display:block;font-weight:650}input,select{box-sizing:border-box;width:100%;font:inherit;padding:10px;border:1px solid #827995;border-radius:7px;margin:7px 0 15px}button,.button{font:inherit;background:#195f53;color:white;border:0;border-radius:9px;padding:12px 17px;display:inline-block;text-decoration:none;cursor:pointer}output{display:block;background:#e0f2ec;padding:18px;border-radius:10px;margin:14px 0;font-weight:650}nav a{margin-right:20px;color:inherit}.disclosure{font-size:13px;display:block;margin:8px 0 16px}a{color:#174d85}@media(max-width:650px){.grid{grid-template-columns:1fr}main{padding:14px}}@media print{button,.commerce{display:none}body,section{background:white}header{color:black;background:none}}</style>
<main><nav><a href="https://deals.vyonetixsolutions.com.au/">Home</a><a href="https://deals.vyonetixsolutions.com.au/tools/">All tools</a></nav><header><svg aria-hidden="true" viewBox="0 0 160 150"><path fill="#ddd0ff" d="M30 35h90v85H30z"/><ellipse fill="#b4a0e8" cx="75" cy="35" rx="45" ry="24"/><ellipse fill="#65528f" cx="75" cy="35" rx="17" ry="10"/><path fill="#efe8ff" d="M75 55h65v83H75z"/><path fill="none" stroke="#7c3aed" stroke-width="3" d="M83 74h49M83 94h49M83 114h49"/></svg><p>Vyonetix label planning</p><h1>How many labels are on your roll?</h1><p>Use roll length, label height and the gap to plan a small print run. The example is ready to calculate.</p></header>
<section><h2>Enter the roll measurements</h2><form id="calc"><div class="grid"><label>Roll length (metres)<input id="length" type="number" min="0.001" max="100000" step="any" value="30" required></label><label>Label height (mm)<input id="height" type="number" min="0.01" max="10000" step="any" value="50" required></label><label>Gap between labels (mm)<input id="gap" type="number" min="0" max="1000" step="any" value="3" required></label><label>Leader and end waste (metres)<input id="waste" type="number" min="0" max="100000" step="any" value="0.3" required></label></div><button type="submit">Calculate label count</button><output id="result" aria-live="polite"></output></form><p>Count = floor((roll length minus waste) × 1,000 ÷ (label height plus gap)). Defaults are illustrative measurements. Actual counts can vary with winding and printer setup.</p><button id="copy" type="button">Copy planning brief</button> <button id="print" type="button">Print or save PDF</button><p id="copyStatus" aria-live="polite"></p></section>
<section class="commerce"><h2>Optional retailer searches</h2><p>Confirm roll width, core, winding direction, thermal media type and your printer's specifications. A search is not compatibility or stock verification.</p><label>Retailer country<select id="market"><option>AU</option><option>US</option><option>UK</option><option>CA</option></select></label><a id="amazon" class="button" target="_blank" rel="sponsored nofollow noopener">Search Amazon</a><span class="disclosure">As an Amazon Associate I earn from qualifying purchases.</span><a id="ebay" class="button" target="_blank" rel="sponsored nofollow noopener" hidden>Search eBay AU</a><span id="epn" class="disclosure" hidden>eBay Partner Network links may earn Vyonetix a commission.</span></section><section><h2>Planning notes</h2><p>This estimates physical roll yield. It does not read a printer, use manufacturer compatibility data, check prices or inspect stock. Measure a complete label pitch and check your media supplier's specification.</p></section></main>
<script>
const CONFIG=__CONFIG__;
function labelCount(length,height,gap,waste){if(![length,height,gap,waste].every(Number.isFinite)||length<=0||height<=0||gap<0||waste<0||waste>length)throw new RangeError('Enter positive roll length and label height. Gap and waste cannot be negative; waste cannot exceed the roll.');return Math.floor((length-waste)*1000/(height+gap));}
const $=id=>document.getElementById(id);let brief='';
function calculate(event){if(event)event.preventDefault();try{const v=['length','height','gap','waste'].map(id=>Number($(id).value));if(['length','height','gap','waste'].some(id=>$(id).value.trim()===''))throw new RangeError('Fill all four measurements.');const count=labelCount(...v);$('result').textContent=count.toLocaleString()+' complete labels (planning estimate)';brief=`Vyonetix label-roll plan: ${count} labels; roll ${v[0]} m, label height ${v[1]} mm, gap ${v[2]} mm, waste ${v[3]} m. Formula: floor(usable mm / label pitch mm). Check media fit with your supplier. https://deals.vyonetixsolutions.com.au/tools/`;return count;}catch(e){$('result').textContent=e.message;brief='';return null;}}
function routes(){const market=$('market').value;const [host,tag]=CONFIG.markets[market];$('amazon').href=host+'/s?'+new URLSearchParams({k:'thermal printer label rolls',tag});$('amazon').textContent='Search Amazon '+market;const enabled=market==='AU'&&Boolean(CONFIG.campaign);$('ebay').hidden=!enabled;$('epn').hidden=!enabled;if(enabled)$('ebay').href='https://www.ebay.com.au/sch/i.html?'+new URLSearchParams({_nkw:'thermal printer label rolls',LH_BIN:'1',mkcid:'1',mkevt:'1',mkrid:'705-53470-19255-0',campid:CONFIG.campaign,toolid:'10001',customid:'vx-'+CONFIG.slug});}
$('calc').addEventListener('submit',calculate);for(const id of ['length','height','gap','waste'])$(id).addEventListener('input',calculate);$('market').addEventListener('change',routes);$('print').addEventListener('click',()=>window.print());$('copy').addEventListener('click',async()=>{if(!brief){$('copyStatus').textContent='Enter valid measurements first.';return;}try{await navigator.clipboard.writeText(brief);$('copyStatus').textContent='Planning brief copied.';}catch(e){$('copyStatus').textContent=brief;}});calculate();routes();
</script></html>'''
    return template.replace("__TITLE__", title).replace("__CONFIG__", config).replace("<style>", "<style>[hidden]{display:none!important}", 1)


def report_html(report: dict) -> str:
    cards = []
    for row in report["rows"]:
        content = f'<h2>{html.escape(row["model"])} ({html.escape(row["market"])})</h2><p>Status: {html.escape(row["status"])}. {html.escape(row["reason"])}</p>'
        if row["status"] == "matched_reference":
            content += f'<p>High-yield reference: <strong>{html.escape(row["part"])}</strong>. Illustrative rated-yield interval: {row["illustrative_months"]:.2f} months at the entered {row["pages_per_month"]:g} pages/month.</p><p>{html.escape(row["limits"])}</p><p><a href="{html.escape(row["source_url"], quote=True)}">Manufacturer reference</a> &nbsp; <a href="{html.escape(row["tool_url"], quote=True)}">Open this model in the Vyonetix finder</a></p>'
        cards.append('<section>' + content + '</section>')
    return '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Example printer purchasing brief</title><style>body{font:17px system-ui;color:#18304b;background:#eef3f8;max-width:950px;margin:30px auto;padding:16px}section{background:#f4f2ff;border-left:5px solid #6554a4;padding:18px;margin:18px 0;border-radius:12px}a{color:#174e92}button{padding:12px;font:inherit}@media print{button{display:none}body{background:white}}</style><h1>Example printer purchasing brief</h1><p>This is a fictitious sample inventory, not a record of your office equipment. Share a real report only after checking it for confidential data.</p><button onclick="window.print()">Print or save PDF</button>' + ''.join(cards) + '<p>This report uses one supported AU manufacturer record. Other models/markets remain unresolved. It is not a replacement diagnosis or stock check.</p>'


def build(out: Path, campaign: str = "") -> dict:
    out.mkdir(parents=True, exist_ok=True)
    data = registry()
    write_json(out / "printer-models-v1.json", data)
    sample = "model,market,pages_per_month\nBrother HL-L2400DW,AU,300\nHLL2400DW,AU,600\nUnknown Printer,AU,300\nHL-L2400DW,UK,300\nHL-L2400DW,AU,0\n"
    (out / "example-inventory.csv").write_text(sample, encoding="utf-8")
    report = batch_report(out / "example-inventory.csv", data)
    write_json(out / "example-report.json", report)
    (out / "fleet-report.html").write_text(report_html(report), encoding="utf-8")
    definition = {"slug": "thermal-label-roll-yield", "title": "Thermal label roll yield planner", "formula_key": "thermal_roll_yield"}
    (out / "index.html").write_text(generate_tool_html(definition, campaign), encoding="utf-8")
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    for k, v in [("title", "Vyonetix reviewed release candidate"), ("link", BASE + "/tools/"), ("description", "Local candidate, not an assertion of publication")]:
        ET.SubElement(channel, k).text = v
    # Candidate feed uses only an existing canonical route, never the new unpublished slug.
    entry = ET.SubElement(channel, "item")
    for k, v in [("title", "Printer supplies finder and model evidence"), ("link", BASE + "/tools/printer-supply-toolbox/"), ("guid", BASE + "/tools/printer-supply-toolbox/"), ("description", "Choose an explicit market and supported model. Confirm the manufacturer part reference before opening an optional retailer search. Unsupported models remain unresolved.")]:
        ET.SubElement(entry, k).text = v
    (out / "candidate-feed.xml").write_bytes(ET.tostring(rss, encoding="utf-8", xml_declaration=True))
    receipt = {"state": "local_candidate_not_deployed", "built_at": datetime.now(timezone.utc).isoformat(), "files": []}
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "release-manifest.json":
            receipt["files"].append({"name": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    write_json(out / "release-manifest.json", receipt)
    return receipt


def indexnow(urls: list[str]) -> dict:
    key = os.environ.get("INDEXNOW_API_KEY", "")
    if not re.fullmatch(r"[A-Za-z0-9-]{8,128}", key):
        raise ValueError("Set an actual account-controlled INDEXNOW_API_KEY; no placeholder is used")
    status, content, _ = get_public(BASE + "/" + key + ".txt")
    if status != 200 or content.decode().strip() != key:
        raise ValueError("Public key ownership could not be verified")
    for url in urls:
        status, content, _ = get_public(url)
        if status != 200 or b"noindex" in content.lower():
            raise ValueError("Submit only existing, indexable HTTP 200 pages")
    payload = json.dumps({"host": urllib.parse.urlsplit(BASE).netloc, "key": key, "keyLocation": BASE + "/" + key + ".txt", "urlList": sorted(set(urls))}).encode()
    request = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=15) as response:
        return {"status": response.status, "submitted": len(set(urls)), "meaning": "Submission receipt only; crawling, indexing and traffic are not guaranteed"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", type=Path, default=ROOT / "01_WEBSITE/staging/2026-10-29-reviewed-pipeline")
    b.add_argument("--epn-campaign", default="", help="Optional account-approved public AU EPN campaign ID")
    a = sub.add_parser("audit")
    a.add_argument("--out", type=Path, required=True)
    report = sub.add_parser("batch")
    report.add_argument("input", type=Path)
    report.add_argument("--out", type=Path, required=True)
    idx = sub.add_parser("indexnow")
    idx.add_argument("urls", nargs="+")
    args = parser.parse_args()
    if args.command == "build":
        result = build(args.out, args.epn_campaign)
    elif args.command == "audit":
        result = audit_feeds()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.out, result)
    elif args.command == "batch":
        result = batch_report(args.input, registry())
        args.out.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.out, result)
    else:
        result = indexnow(args.urls)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
