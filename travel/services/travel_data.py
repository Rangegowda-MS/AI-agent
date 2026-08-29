DESTINATIONS = {
    "goa": (["Baga Beach","Fort Aguada","Fontainhas","Chapora Fort","Candolim"], 3500, "Beaches, food, heritage and nightlife."),
    "kerala": (["Alleppey Backwaters","Munnar","Fort Kochi","Varkala","Thekkady"], 4000, "Backwaters, hills, wildlife and slow travel."),
    "manali": (["Solang Valley","Old Manali","Hidimba Temple","Atal Tunnel","Mall Road"], 3800, "Mountains, adventure and scenic escapes."),
    "coorg": (["Abbey Falls","Raja's Seat","Coffee Estate","Dubare","Mandalpatti"], 3200, "Coffee estates, waterfalls and misty hills."),
    "jaipur": (["Amber Fort","City Palace","Hawa Mahal","Jantar Mantar","Bapu Bazaar"], 3000, "Forts, palaces, markets and culture.")
}
def get_destination(name):
    return DESTINATIONS.get(name.lower(), (["Local landmark","Popular market","Cultural attraction","Scenic viewpoint","Local food street"], 3200, "A personalized destination plan."))
