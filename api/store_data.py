"""
Chicken Kitchen — Store master data.
Source: CK_Master_Locations.xlsx (29 active stores).
"""

STORES = {
    "ALT": {
        "name": "Alton",
        "legal_entity": "CK at Alton Road LLC",
        "admin_email": "ckatalton@gmail.com",
        "address": "1509 Alton Rd, Miami, FL 33139",
    },
    "BIR": {
        "name": "Bird & Ludlum",
        "legal_entity": "CK at Bird & Ludum LLC",
        "admin_email": "ckbirdludlum@gmail.com",
        "address": "6786 Bird Rd, Miami, FL 33155",
    },
    "BIS": {
        "name": "Biscayne & 69th",
        "legal_entity": "CK at Buena Vista LLC",
        "admin_email": "buenavista@chickenkitchen.com",
        "address": "6907 Biscayne Blvd, Miami, FL 33138",
    },
    "BLU": {
        "name": "Blue Lagoon",
        "legal_entity": "CK at Blue Lagoon LLC",
        "admin_email": "bluelagoon@chickenkitchen.com",
        "address": "5765 NW 7th St, Miami, FL 33126",
    },
    "COL": {
        "name": "Collins & 71st",
        "legal_entity": "CK at North Beach LLC",
        "admin_email": "northbeach@chickenkitchen.com",
        "address": "7116 Collins Ave, Miami, FL 33141",
    },
    "COU": {
        "name": "Country Walk",
        "legal_entity": "CK at Country Walk LLC",
        "admin_email": "cwalk@chickenkitchen.com",
        "address": "15812 SW 137th Ave, Miami, FL 33175",
    },
    "CRF": {
        "name": "Coral Reef",
        "legal_entity": "CK at So. Dixie LLC",
        "admin_email": "ckcoralreef@hotmail.com",
        "address": "15053 South Dixie Hwy, Miami, FL 33176",
    },
    "CUT": {
        "name": "Cutler Ridge",
        "legal_entity": "CK at Cutler Ridge LLC",
        "admin_email": "cutlerbay@chickenkitchen.com",
        "address": "20527 Old Cutler Rd, Cutler Bay, FL 33189",
    },
    "DAV": {
        "name": "Davie",
        "legal_entity": "CK at Davie LLC",
        "admin_email": "davie@chickenkitchen.com",
        "address": "2319 South University Dr, Davie, FL 33324",
    },
    "DOR": {
        "name": "Doral",
        "legal_entity": "CK at Doral LLC",
        "admin_email": "doral@chickenkitchen.com",
        "address": "9741 NW 41st St, Miami, FL 33178",
    },
    "DWT": {
        "name": "Downtown",
        "legal_entity": "CK at Downtown LLC",
        "admin_email": "downtown@chickenkitchen.com",
        "address": "146 NE 2nd Ave, Miami, FL 33132",
    },
    "FIU": {
        "name": "FIU",
        "legal_entity": "CK at FIU LLC",
        "admin_email": "fiu@chickenkitchen.com",
        "address": "10550 SW 8th St, Miami, FL 33174",
    },
    "FTL": {
        "name": "Ft Lauderdale",
        "legal_entity": "CK at Plaza del Mar LLC",
        "admin_email": "coralridge@chickenkitchen.com",
        "address": "1523 N Federal Hwy, Fort Lauderdale, FL 33304",
    },
    "GAL": {
        "name": "Galloway",
        "legal_entity": "CK at Galloway LLC",
        "admin_email": "galloway@chickenkitchen.com",
        "address": "8732 Sunset Dr, Miami, FL 33173",
    },
    "HAM": {
        "name": "Hammocks",
        "legal_entity": "CK at Hammocks LLC",
        "admin_email": "hammocks@chickenkitchen.com",
        "address": "15738 SW 72nd St, Miami, FL 33193",
    },
    "KBI": {
        "name": "Key Biscayne",
        "legal_entity": "CK at Key Biscayne LLC",
        "admin_email": "keybiscayne@chickenkitchen.com",
        "address": "65 Harbor Dr Space #6, Key Biscayne, FL 33149",
    },
    "KEN": {
        "name": "Kendall",
        "legal_entity": "CK at Kendall Mall LLC",
        "admin_email": "chickenkitchenkendall@gmail.com",
        "address": "9067 SW 107th Ave, Miami, FL 33176",
    },
    "KEY": {
        "name": "Keystone",
        "legal_entity": "CK at Keystone Plaza LLC",
        "admin_email": "keystone@chickenkitchen.com",
        "address": "13521 Biscayne Blvd, North Miami Beach, FL 33183",
    },
    "LEJ": {
        "name": "Lejeune",
        "legal_entity": "CK at Lejeune LLC",
        "admin_email": "lejeune@chickenkitchen.com",
        "address": "400 South Dixie Hwy, Coral Gables, FL 33146",
    },
    "MBE": {
        "name": "Miami Beach",
        "legal_entity": "CK at 41st LLC",
        "admin_email": "41st@chickenkitchen.com",
        "address": "524 Arthur Godfrey Rd, Miami Beach, FL 33140",
    },
    "MGA": {
        "name": "Miami Gardens",
        "legal_entity": "CK at Miami Garders Drive LLC",
        "admin_email": "miagardens@chickenkitchen.com",
        "address": "18515 NE 18th Ave Ste #100, North Miami Beach, FL 33179",
    },
    "MLK": {
        "name": "Miami Lakes",
        "legal_entity": "CK at Miami Lakes LLC",
        "admin_email": "ckmiamilakes@gmail.com",
        "address": "15221 NW 67th Ave, Miami Lakes, FL 33014",
    },
    "NML": {
        "name": "N. Miami Lakes",
        "legal_entity": "CK at North Miami Lakes LLC",
        "admin_email": "NMLakes@chickenkitchen.com",
        "address": "6450 NW 186 St, Hialeah, FL 33015",
    },
    "PCR": {
        "name": "Pinecrest",
        "legal_entity": "CK at Pinecrest LLC",
        "admin_email": "pinecrest@chickenkitchen.com",
        "address": "11403 South Dixie Hwy, Miami, FL 33176",
    },
    "PLA": {
        "name": "Plantation",
        "legal_entity": "CK at Plantation LLC",
        "admin_email": "plantation@chickenkitchen.com",
        "address": "6985 W Broward Blvd, Plantation, FL 33317",
    },
    "PNS": {
        "name": "Pembroke Pines",
        "legal_entity": "CK at Pines LLC",
        "admin_email": "ppines@chickenkitchen.com",
        "address": "2014 N Flamingo Rd, Pembroke Pines, FL 33028",
    },
    "SUN": {
        "name": "Sunset",
        "legal_entity": "CK at Sunset Drive LLC",
        "admin_email": "sunset@chickenkitchen.com",
        "address": "1565 Sunset Dr, Coral Gables, FL 33143",
    },
    "WBR": {
        "name": "West Bird",
        "legal_entity": "CK at Westbird LLC",
        "admin_email": "westbird@chickenkitchen.com",
        "address": "11425 SW 40th St, Miami, FL 33165",
    },
    "WPI": {
        "name": "West Pines",
        "legal_entity": "CK at West Pines LLC",
        "admin_email": "westpines@chickenkitchen.com",
        "address": "17149 Pines Blvd, Pembroke Pines, FL 33027",
    },
}


def get_store(code: str) -> dict | None:
    """Return store dict by code, or None."""
    return STORES.get(code.upper())


def get_store_choices() -> list[dict]:
    """Return list of {code, label} for dropdowns, sorted by name."""
    choices = [
        {"code": code, "label": f"{info['name']} — {info['address']}"}
        for code, info in STORES.items()
    ]
    choices.sort(key=lambda x: x["label"])
    return choices
