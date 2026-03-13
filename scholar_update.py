from scholarly import scholarly
import json

scholar_id = "boCYnOcAAAAJ"

author = scholarly.search_author_id(scholar_id)
author = scholarly.fill(author)

stats = {
    "citations": author["citedby"],
    "hindex": author["hindex"],
    "papers": len(author["publications"])
}

with open("scholar-stats.json","w") as f:
    json.dump(stats,f,indent=2)

pubs=[]

for pub in author["publications"][:30]:
    p = scholarly.fill(pub)
    pubs.append({
        "title": p["bib"].get("title",""),
        "authors": p["bib"].get("author",""),
        "venue": p["bib"].get("venue",""),
        "year": p["bib"].get("pub_year","")
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