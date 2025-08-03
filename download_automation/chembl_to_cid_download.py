import requests
import time
import os

from rdkit import Chem
from rdkit.Chem import AllChem

chembl_ids = ["CHEMBL483017",
"CHEMBL491307",
"CHEMBL1079367",
"CHEMBL2376097",
"CHEMBL2333536",
"CHEMBL507166",
"CHEMBL494659",
"CHEMBL1081338",
"CHEMBL464376",
"CHEMBL4544522",
"CHEMBL491879",
"CHEMBL1514916",
"CHEMBL519970"
]
cid_list = []

def get_smiles_from_chembl(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{chembl_id}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data["molecule_structures"]["canonical_smiles"]
        else:
            print(f"⚠️ ChEMBL ID {chembl_id} not found.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {chembl_id}: {e}")
        return None

def get_cid_from_smiles(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()["IdentifierList"]["CID"][0]
        else:
            print(f"⚠️ No CID found for SMILES: {smiles}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching CID for SMILES: {e}")
        return None

def download_sdf(cid, filename):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/record/SDF/?record_type=3d"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200 and response.content.strip():
            with open(f"{filename}.sdf", "wb") as f:
                f.write(response.content)
            print(f"✅ Saved 3D SDF for {filename}")
        else:
            print(f"⚠️ 3D structure not available for CID {cid}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading SDF for CID {cid}: {e}")

# Main loop
for chembl_id in chembl_ids:
    smiles = get_smiles_from_chembl(chembl_id)
    if smiles:
        cid = get_cid_from_smiles(smiles)
        if cid:
            cid_list.append(cid)
            download_sdf(cid, chembl_id)
    time.sleep(1)  # ⏳ Wait to avoid rate limits

print("\n🧾 Final CID list:", cid_list)


