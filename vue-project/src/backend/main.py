# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re
import ast
import json
from pathlib import Path
from typing import List, Dict

# --- Load CONFIG from the PoC notebook (embedded here) ---
# I parsed your notebook and obtained the following relevant CONFIG.
# If you later want to tune this, either edit this dict or load the notebook dynamically.
CONFIG = {
    "expected_folders": {
        "1.0 Unit Panel Documentation": ["Assessment Moderation", "Unit Moderation", "QEA Report"],
        "2.0 Unit Outline": ["Unit Outline"],
        "3.0 Learning Materials": ["Lecture"],
        "4.0 Tutorial Materials": ["Tutorial"],
        "5.0 Assessments and Marking Schemes": ["Assignment", "Rubric", "Test"],
        "6.0 Samples of Students' Work": [],
        "7.0 Outcome Based Education Report": ["OBE"],
        "8.0 Safety Acknowledgement": [],
        "9.0 Final Exam Script": []
    },
    # Naming pattern (from your PoC) for student files
    "student_work_pattern": r"^(COS\d{5})_(Assignment|Test|Tutorial)\d+_(\d{8})\.(pdf|docx)$"
}

EXPECTED = CONFIG["expected_folders"]
STUDENT_RE = re.compile(CONFIG.get("student_work_pattern", ""), flags=re.IGNORECASE)

# Map folder titles (1.0 ...) to stable keys unit1..unit9
folder_titles = list(EXPECTED.keys())  # expected order preserved from notebook
unit_keys = {title: f"unit{idx+1}" for idx, title in enumerate(folder_titles)}

# Create reverse index: keyword -> unit key for quick mapping
keyword_index = []
for title, keywords in EXPECTED.items():
    for kw in keywords:
        keyword_index.append((kw.lower(), unit_keys[title]))
# Note: Some folders have empty keyword lists (e.g., 6,8,9) — student regex covers 6

app = FastAPI(title="Filename Classifier (PoC)")

# CORS - allow your frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:3000","http://127.0.0.1:5173","*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FilenamesPayload(BaseModel):
    filenames: List[str]

def classify_filename(name: str) -> str:
    """
    Returns unit key (unit1..unit9) or 'unsorted' if none matched.
    Strategy:
      1) substring match against keywords (case-insensitive) mapped to units
      2) if student regex matches --> classify into unit for "6.0 Samples of Students' Work"
      3) fallback: unsorted
    """
    if not name:
        return "unsorted"
    lname = name.lower()
    # 1) keyword matching (first match wins)
    for kw, unit in keyword_index:
        if kw and kw.lower() in lname:
            return unit

    # 2) student file regex (goes to the 6.0 folder unitN where that title is)
    if STUDENT_RE.search(name):
        # find unit id for 6.0
        for title, key in unit_keys.items():
            if "samples of students' work" in title.lower():
                return key
        # fallback
        return "unsorted"

    # 3) fallback unsorted
    return "unsorted"

@app.post("/classify")
def classify(payload: FilenamesPayload) -> Dict[str, List[str]]:
    # Prepare initial result dictionary with all unit keys + unsorted
    result = {f"unit{i+1}": [] for i in range(len(folder_titles))}
    result["unsorted"] = []

    for fname in payload.filenames:
        unit = classify_filename(fname)
        if unit in result:
            result[unit].append(fname)
        else:
            # If somehow a folder title mapped to something else, put in unsorted
            result["unsorted"].append(fname)

    return result
