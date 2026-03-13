from scholarly import scholarly
import json
import signal
import sys

scholar_id = "boCYnOcAAAAJ"

# ---- Hard timeout ----
def handler(signum, frame):
    print("Timeout reached")
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(120)  # 2 min timeout

try:
    author = scholarly.search_author_id(scholar_id)
    # Only basic info + counts + publication metadata
    author = scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])

    # Scholar stats
    stats = {
        "citations": author.get("citedby",0),
        "hindex": author.get("hindex",0),
        "i10index": author.get("i10index",0)
    }

    with open("scholar-stats.json","w") as f:
        json.dump(stats,f,indent=2)

    # Publications
    pubs = []
    for pub in author["publications"]:
        bib = scholarly.fill(pub)["bib"]
        pubs.append({
            "title": bib.get("title",""),
            "authors": bib.get("author",""),
            "venue": bib.get("venue",""),
            "year": bib.get("pub_year",""),
            "abstract": bib.get("abstract",""),
	    "pub_url": pub.get("pub_url", "")
        })

    # Sort publications by year descending
    pubs_sorted = sorted(pubs, key=lambda x: x["year"] if x["year"] else 0, reverse=True)

    with open("publications.json","w") as f:
        json.dump(pubs_sorted,f,indent=2)

    # Citation history
    years = []
    counts = []

    for y,c in author.get("cites_per_year",{}).items():
        years.append(y)
        counts.append(c)

    with open("citations.json","w") as f:
        json.dump({"years":years,"citations":counts},f,indent=2)

    print("Scholar data updated successfully")

except Exception as e:
    print("Scholar fetch failed:", e)