from scholarly import scholarly
import json
import signal
import sys

scholar_id = "boCYnOcAAAAJ"

# ---- Hard timeout (90 seconds) ----
def handler(signum, frame):
    print("Timeout reached")
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(90)

try:

    author = scholarly.search_author_id(scholar_id)
    author = scholarly.fill(author, sections=["basics","indices","counts","publications"])

    stats = {
        "citations": author["citedby"],
        "hindex": author["hindex"],
        "papers": len(author["publications"])
    }

    with open("scholar-stats.json","w") as f:
        json.dump(stats,f,indent=2)

    pubs = []

    for pub in author["publications"][:15]:
        bib = pub["bib"]

        pubs.append({
            "title": bib.get("title",""),
            "authors": bib.get("author",""),
            "venue": bib.get("venue",""),
            "year": bib.get("pub_year","")
        })

    with open("publications.json","w") as f:
        json.dump(pubs,f,indent=2)

    years=[]
    counts=[]

    for y,c in author["cites_per_year"].items():
        years.append(y)
        counts.append(c)

    with open("citations.json","w") as f:
        json.dump({"years":years,"citations":counts},f,indent=2)

    print("Scholar data updated")

except Exception as e:
    print("Scholar fetch failed:",e)