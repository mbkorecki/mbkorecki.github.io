from scholarly import scholarly
import json

scholar_id = "boCYnOcAAAAJ"

author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author, sections=["basics","indices","counts","publications"])

# stats
stats = {
    "citations": author["citedby"],
    "hindex": author["hindex"],
    "papers": len(author["publications"])
}

with open("scholar-stats.json","w") as f:
    json.dump(stats,f,indent=2)


# publications (NO fill() calls)
pubs = []

for pub in author["publications"][:20]:

    bib = pub["bib"]

    pubs.append({
        "title": bib.get("title",""),
        "authors": bib.get("author",""),
        "venue": bib.get("venue",""),
        "year": bib.get("pub_year","")
    })


with open("publications.json","w") as f:
    json.dump(pubs,f,indent=2)


# citation history
years = []
counts = []

for y,c in author["cites_per_year"].items():
    years.append(y)
    counts.append(c)

with open("citations.json","w") as f:
    json.dump({"years":years,"citations":counts},f,indent=2)