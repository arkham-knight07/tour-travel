from utils.jsonstore import load_json_any

# Load tours from backend/data/tours.json OR frontend/data/tours.json
TOURS = load_json_any("data/tours.json")

def search_tours(q="", type_="", featured=None):
    q = (q or "").lower().strip()
    type_ = (type_ or "").lower().strip()

    results = []
    for t in TOURS:
        ok = True
        if q:
            hay = f'{t.get("title","")} {t.get("short","")}'.lower()
            ok &= q in hay
        if type_:
            ok &= t.get("type", "").lower() == type_
        if featured is not None:
            ok &= bool(t.get("featured", False)) == bool(featured)
        if ok:
            results.append(t)
    return results
def get_tour_by_id(tour_id):
    for t in TOURS:
        if t.get("id") == tour_id:
            return t
    return None