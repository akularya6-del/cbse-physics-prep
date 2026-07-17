import os
import re
import json
import glob
from datetime import datetime

import fitz  # PyMuPDF

TOPIC_MAP = {
    "01": {
        "code": "01",
        "topic": "Electric Charges and Fields",
        "chapter": "Electrostatics",
        "unit": "Electrostatics & Current Electricity",
        "keywords": [
            "charge", "coulomb", "coulomb's law", "electric field", "electric field line",
            "electric flux", "gauss", "gauss's law", "dipole", "dipole moment",
            "point charge", "continuous charge", "uniformly charged", "conducting sphere",
            "insulating", "torque on dipole", "electric field intensity", "field at axis",
            "field at equator", "equatorial point", "axial point", "superposition principle",
            "quantisation of charge", "additivity of charge", "conservation of charge",
            "infinite line charge", "infinite plane sheet", "uniformly charged sphere",
            "hollow sphere", "solid sphere", "cylindrical gaussian surface",
            "spherical gaussian surface", "electric field due to", "flux through",
            "net charge enclosed", "linear charge density", "surface charge density",
            "volume charge density"
        ]
    },
    "02": {
        "code": "02",
        "topic": "Electrostatic Potential and Capacitance",
        "chapter": "Electrostatics",
        "unit": "Electrostatics & Current Electricity",
        "keywords": [
            "potential", "potential difference", "electric potential", "potential energy",
            "capacitor", "capacitance", "parallel plate", "dielectric", "dielectric constant",
            "dielectric strength", "energy stored", "electrostatic energy", "van de graaff",
            "equipotential", "equipotential surface", "work done", "potential at point",
            "combination of capacitors", "series", "parallel", "charge on capacitor",
            "energy density", "polarisation", "polarization", "relative permittivity",
            "spherical capacitor", "cylindrical capacitor", "isolated sphere",
            "common potential", "loss of energy"
        ]
    },
    "03": {
        "code": "03",
        "topic": "Current Electricity",
        "chapter": "Current Electricity",
        "unit": "Electrostatics & Current Electricity",
        "keywords": [
            "current", "drift velocity", "mobility", "ohm's law", "resistance",
            "resistivity", "conductivity", "resistor", "series combination", "parallel combination",
            "kirchhoff", "wheatstone bridge", "metre bridge", "meter bridge", "potentiometer",
            "emf", "internal resistance", "terminal voltage", "cell", "primary cell",
            "secondary cell", "current density", "electrical energy", "electrical power",
            "heating effect", "joule's law", "fuse", "temperature dependence",
            "carbon resistor", "color code", "galvanometer", "ammeter", "voltmeter",
            "shunt", "conversion of galvanometer"
        ]
    },
    "04": {
        "code": "04",
        "topic": "Moving Charges and Magnetism",
        "chapter": "Magnetic Effects of Current and Magnetism",
        "unit": "Magnetic Effects of Current and Magnetism",
        "keywords": [
            "magnetic field", "biot-savart", "biot savart", "ampere's circuital", "ampere circuital",
            "solenoid", "toroid", "force on charge", "lorentz force", "cyclotron",
            "cyclotron frequency", "force on wire", "torque on loop", "magnetic moment",
            "current loop", "moving coil galvanometer", "sensitivity", "figure of merit",
            "shunt", "parallel wires", "force between wires", "ampere", "definition of ampere",
            "straight wire", "circular loop", "magnetic field at centre",
            "magnetic field on axis", "helical path", "radius of circular path"
        ]
    },
    "05": {
        "code": "05",
        "topic": "Magnetism and Matter",
        "chapter": "Magnetic Effects of Current and Magnetism",
        "unit": "Magnetic Effects of Current and Magnetism",
        "keywords": [
            "bar magnet", "magnetic dipole", "magnetic field lines", "dipole moment",
            "torque on magnet", "magnetic field on axis", "magnetic field on equator",
            "earth's magnetism", "geomagnetic", "magnetic declination", "magnetic inclination",
            "horizontal component", "magnetic intensity", "magnetisation", "susceptibility",
            "permeability", "retentivity", "coercivity", "hysteresis", "hysteresis loop",
            "paramagnetic", "diamagnetic", "ferromagnetic", "curie's law", "curie temperature",
            "magnetic field of earth", "magnetic meridian", "geographic meridian"
        ]
    },
    "06": {
        "code": "06",
        "topic": "Electromagnetic Induction",
        "chapter": "Electromagnetic Induction and Alternating Currents",
        "unit": "Electromagnetic Induction and Alternating Currents",
        "keywords": [
            "electromagnetic induction", "faraday", "faraday's law", "lenz", "lenz's law",
            "induced emf", "induced current", "motional emf", "eddy current",
            "self inductance", "self induction", "mutual inductance", "mutual induction",
            "inductor", "energy in inductor", "lc oscillation", "flux", "change in flux",
            "rate of change", "magnetic flux", "coil", "number of turns",
            "rotating coil", "falling magnet", "magnet dropped", "copper ring",
            "metallic pipe", "conducting loop", "area of loop", "time varying field"
        ]
    },
    "07": {
        "code": "07",
        "topic": "Alternating Current",
        "chapter": "Electromagnetic Induction and Alternating Currents",
        "unit": "Electromagnetic Induction and Alternating Currents",
        "keywords": [
            "alternating current", "ac", "rms", "peak value", "peak current", "peak voltage",
            "average value", "phasor", "phasor diagram", "reactance", "impedance",
            "capacitive reactance", "inductive reactance", "resonance", "resonant frequency",
            "lc circuit", "lcr circuit", "series lcr", "parallel lcr", "power factor",
            "wattless current", "choke coil", "transformer", "step up", "step down",
            "efficiency of transformer", "losses in transformer", "eddy current loss",
            "hysteresis loss", "copper loss", "quality factor", "q factor",
            "bandwidth", "half power", "ac voltage", "ac source", "oscillating voltage"
        ]
    },
    "08": {
        "code": "08",
        "topic": "Electromagnetic Waves",
        "chapter": "Electromagnetic Waves",
        "unit": "Electromagnetic Waves",
        "keywords": [
            "electromagnetic wave", "em wave", "maxwell", "displacement current",
            "electromagnetic spectrum", "infrared", "ultraviolet", "x-ray", "gamma ray",
            "microwave", "radio wave", "wavelength", "frequency", "speed of light",
            "hertz experiment", "em wave properties", "transverse nature",
            "energy of em wave", "intensity", "poynting vector"
        ]
    },
    "09": {
        "code": "09",
        "topic": "Ray Optics and Optical Instruments",
        "chapter": "Optics",
        "unit": "Optics",
        "keywords": [
            "reflection", "refraction", "snell's law", "total internal reflection",
            "critical angle", "lens", "convex lens", "concave lens", "focal length",
            "image formation", "magnification", "power of lens", "lens formula",
            "lens maker", "mirror", "convex mirror", "concave mirror", "mirror formula",
            "prism", "dispersion", "angle of prism", "angle of deviation", "minimum deviation",
            "rainbow", "scattering", "rayleigh", "optical instrument", "microscope",
            "telescope", "compound microscope", "astronomical telescope", "reflecting telescope",
            "resolving power", "angular resolution", "chromatic aberration", "spherical aberration",
            "refractive index", "absolute refractive index", "relative refractive index",
            "apparent depth", "real depth", "glass slab", "slab", "lateral shift",
            "optical fibre", "optical fiber", "endoscope"
        ]
    },
    "10": {
        "code": "10",
        "topic": "Wave Optics",
        "chapter": "Optics",
        "unit": "Optics",
        "keywords": [
            "wave optics", "interference", "young's double slit", "young double slit",
            "fringe", "fringe width", "coherent source", "diffraction", "single slit",
            "diffraction pattern", "resolution", "resolving power", "polarisation",
            "polarization", "polaroid", "malus law", "brewster", "brewster's angle",
            "plane polarised", "plane polarized", "wavefront", "huygens", "huygen's",
            "refraction of wave", "reflection of wave", "path difference", "phase difference",
            "constructive interference", "destructive interference", "intensity distribution",
            "fringe visibility", "coherence", "temporal coherence", "spatial coherence"
        ]
    },
    "11": {
        "code": "11",
        "topic": "Dual Nature of Radiation and Matter",
        "chapter": "Dual Nature of Radiation and Matter",
        "unit": "Dual Nature of Radiation and Matter",
        "keywords": [
            "photoelectric effect", "photoelectric", "photoelectron", "threshold frequency",
            "threshold wavelength", "stopping potential", "work function", "einstein's",
            "einstein photoelectric", "photon", "photon energy", "de broglie",
            "de broglie wavelength", "matter wave", "wave particle duality",
            "davisson germer", "electron diffraction", "photoelectric current",
            "saturation current", "intensity of light", "frequency of light",
            "kinetic energy of photoelectron", "maximum kinetic energy",
            "energy of photon", "momentum of photon", "wavelength of electron",
            "wave nature", "particle nature"
        ]
    },
    "12": {
        "code": "12",
        "topic": "Atoms",
        "chapter": "Atoms and Nuclei",
        "unit": "Atoms and Nuclei",
        "keywords": [
            "bohr model", "bohr's model", "bohr radius", "hydrogen atom", "hydrogen spectrum",
            "spectral series", "lyman", "balmer", "paschen", "brackett", "pfund",
            "energy level", "orbit", "orbital", "excited state", "ground state",
            "ionization energy", "ionization potential", "binding energy of electron",
            "rydberg constant", "rydberg formula", "transition", "emission spectrum",
            "absorption spectrum", "angular momentum", "quantized", "quantisation"
        ]
    },
    "13": {
        "code": "13",
        "topic": "Nuclei",
        "chapter": "Atoms and Nuclei",
        "unit": "Atoms and Nuclei",
        "keywords": [
            "nucleus", "nuclear", "atomic mass", "mass number", "atomic number",
            "isotope", "isobar", "isoton", "nuclear size", "nuclear radius",
            "nuclear density", "binding energy", "mass defect", "packing fraction",
            "nuclear fission", "fission", "nuclear fusion", "fusion", "chain reaction",
            "critical mass", "nuclear reactor", "moderator", "control rod", "coolant",
            "radioactivity", "radioactive", "alpha decay", "beta decay", "gamma decay",
            "half life", "half-life", "mean life", "decay constant", "activity",
            "nuclear force", "strong force", "mass energy relation", "e=mc2", "amu",
            "energy equivalent", "nuclear waste", "breeder reactor", "thermal neutron"
        ]
    },
    "14": {
        "code": "14",
        "topic": "Semiconductor Electronics",
        "chapter": "Electronic Devices",
        "unit": "Electronic Devices",
        "keywords": [
            "semiconductor", "intrinsic", "extrinsic", "p-type", "n-type",
            "doping", "donor", "acceptor", "majority carrier", "minority carrier",
            "p-n junction", "pn junction", "depletion region", "forward bias",
            "reverse bias", "diode", "rectifier", "half wave", "full wave",
            "bridge rectifier", "filter", "zener diode", "voltage regulator",
            "zener breakdown", "avalanche breakdown", "led", "light emitting",
            "photodiode", "solar cell", "transistor", "bjt", "common emitter",
            "common base", "common collector", "amplifier", "gain", "current gain",
            "voltage gain", "feedback", "oscillator", "logic gate", "and gate",
            "or gate", "not gate", "nand gate", "nor gate", "truth table",
            "integrated circuit", "ic"
        ]
    },
    "15": {
        "code": "15",
        "topic": "Communication Systems",
        "chapter": "Communication Systems",
        "unit": "Communication Systems",
        "keywords": [
            "communication", "transducer", "transmitter", "receiver", "channel",
            "signal", "noise", "modulation", "amplitude modulation", "am",
            "frequency modulation", "fm", "demodulation", "detector",
            "antenna", "bandwidth", "sky wave", "space wave", "ground wave",
            "propagation", "ionosphere", "microwave", "satellite", "earth station",
            "modulation index", "carrier wave", "message signal", "baseband",
            "repeaters", "attenuation", "amplification"
        ]
    }
}

FILENAME_PATTERNS = [
    r'Physics_(\d{4})_(Main|Compartment)_Set(\d)',
    r'(\d{4})_(Compartment|Main)_Set(\d)_Physics',
    r'CBSE_12th_Physics_(\d{4})_(Compt|Main)_Set(\d)',
    r'12_Physics_(\d{4})_(Main|Compt)_(\d+)_(\d+)_(\d+)',
    r'(\d{4})_Physics_Class12_(Compartment|Main)_S(\d)'
]

SECTION_MARKS = {
    'A': 1,
    'B': 2,
    'C': 3,
    'D': 5,
    'E': 4  # Typical for case study
}

def parse_metadata(filename):
    for pattern in FILENAME_PATTERNS:
        match = re.search(pattern, filename, re.IGNORECASE)
        if match:
            groups = match.groups()
            year = int(groups[0])
            ptype_raw = groups[1].lower()
            ptype = 'Compartment' if 'compt' in ptype_raw or 'compartment' in ptype_raw else 'Main'
            
            if len(groups) >= 3:
                # Some formats might have sets at different groups
                if 'set' in pattern.lower() or 's' in pattern.lower() or len(groups) == 3:
                    set_num = int(groups[2])
                elif len(groups) >= 5: # e.g. 12_Physics_2024_Main_55_1_1
                    set_num = int(groups[4]) 
                else:
                    set_num = 1
            else:
                set_num = 1
            
            return year, ptype, set_num
    
    # Fallback inference
    year = 2024
    if '20' in filename:
        y_match = re.search(r'(20\d\d)', filename)
        if y_match:
            year = int(y_match.group(1))
    
    ptype = 'Compartment' if 'compt' in filename.lower() or 'compartment' in filename.lower() else 'Main'
    
    set_match = re.search(r'set[_-]?(\d)', filename.lower())
    set_num = int(set_match.group(1)) if set_match else 1
    
    return year, ptype, set_num

def clean_garbage_text(text):
    import re
    # Remove words with common Kruti Dev symbols mapped to English ASCII
    # Kruti Dev uses characters like H$, {, }, ~, ^, |, etc., extensively
    words = text.split()
    cleaned_words = []
    
    # Exclude words that have specific garbage markers or are non-ascii
    garbage_patterns = [
        r'H\$', r'\{', r'\}', r'~', r'\^', r'\u00a1', r'\u00a9', r'\u00a2', 
        r'\u00e1', r'\u00e2', r'§', r'¢', r'£', r'¤', r'¥', r'¦', r'¨', r'ª', r'«', r'¬', r'\u00bb', r'\u00ab',
        r'moB', r'm¡a', r'm\|', r'eH\$', r'Zamo', r'hmo', r'm`'
    ]
    
    for w in words:
        is_garbage = False
        for pattern in garbage_patterns:
            if re.search(pattern, w):
                is_garbage = True
                break
        if not is_garbage:
            # Drop any non-ascii characters from the word
            w_clean = re.sub(r'[^\x00-\x7F]+', '', w)
            if w_clean:
                cleaned_words.append(w_clean)
                
    result = ' '.join(cleaned_words)
    # Basic cleanup
    result = re.sub(r'\s+', ' ', result).strip()
    return result

def extract_questions_from_text(text, filename, year, ptype, set_num):
    questions = []
    
    # Standardize newlines
    text = text.replace('\r\n', '\n')
    
    # Find sections
    sections = {}
    current_section = None
    
    lines = text.split('\n')
    
    # We will just iterate and try to find question patterns.
    # A simple state machine
    current_q_num = None
    current_q_text = []
    current_marks = None
    
    # Try to detect explicit marks like [1 Mark], (2 marks)
    def extract_marks(t):
        m = re.search(r'\[(\d+)\s*marks?\]|\((\d+)\s*marks?\)', t, re.IGNORECASE)
        if m:
            for g in m.groups():
                if g: 
                    mark_val = int(g)
                    if mark_val <= 5: # CBSE questions are max 5 marks
                        return mark_val
        return None
        
    for line in lines:
        # Detect section header
        sec_match = re.match(r'^SECTION\s*-\s*([A-E])', line.strip(), re.IGNORECASE) or re.match(r'^SECTION\s+([A-E])', line.strip(), re.IGNORECASE)
        if sec_match:
            current_section = sec_match.group(1).upper()
            continue
            
        # Detect question start
        q_match = re.match(r'^Q\.?\s*(\d+)|^Question\s*(\d+)|^(\d+)\.\s*', line.strip(), re.IGNORECASE)
        if q_match:
            if current_q_num is not None:
                qtext_full = ' '.join(current_q_text).strip()
                qtext_full = clean_garbage_text(qtext_full)
                if len(qtext_full) > 10: # Only add if there's meaningful text left
                    marks = extract_marks(qtext_full)
                    if marks is None and current_section in SECTION_MARKS:
                        marks = SECTION_MARKS[current_section]
                        
                    questions.append({
                        "q_num": current_q_num,
                        "text": qtext_full,
                        "section": current_section or "UNKNOWN",
                        "marks": marks
                    })
            
            # Start new question
            for g in q_match.groups():
                if g: 
                    current_q_num = g
                    break
            
            # Remove the question prefix from line
            line_cleaned = re.sub(r'^Q\.?\s*(\d+)\.?\s*|^Question\s*(\d+)\.?\s*|^(\d+)\.\s*', '', line.strip(), flags=re.IGNORECASE)
            current_q_text = [line_cleaned]
        else:
            if current_q_num is not None:
                current_q_text.append(line.strip())
                
    if current_q_num is not None:
        qtext_full = ' '.join(current_q_text).strip()
        qtext_full = clean_garbage_text(qtext_full)
        if len(qtext_full) > 10:  # Only add if there's meaningful text left
            marks = extract_marks(qtext_full)
            if marks is None and current_section in SECTION_MARKS:
                marks = SECTION_MARKS.get(current_section)
                
            questions.append({
                "q_num": current_q_num,
                "text": qtext_full,
                "section": current_section or "UNKNOWN",
                "marks": marks
            })

    return questions

def classify_question(text):
    scores = {k: 0 for k in TOPIC_MAP}
    text_lower = text.lower()
    
    derivation_keywords = ["derive", "obtain", "prove", "show that"]
    is_derivation = any(dk in text_lower for dk in derivation_keywords)
    
    for code, info in TOPIC_MAP.items():
        for kw in info['keywords']:
            if kw.lower() in text_lower:
                # 1.5x multiplier if it's a derivation question
                weight = 1.5 if is_derivation else 1.0
                scores[code] += weight
                
    max_score = max(scores.values())
    
    if max_score == 0:
        return "00", "Unclassified", False, scores
        
    # Sort topics by score
    sorted_topics = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_code, top_score = sorted_topics[0]
    
    ambiguous = False
    if len(sorted_topics) > 1 and sorted_topics[1][1] > 0:
        second_score = sorted_topics[1][1]
        if (top_score - second_score) / top_score <= 0.2:
            ambiguous = True
            
    return top_code, TOPIC_MAP[top_code]["topic"], ambiguous, scores

def detect_properties(text):
    text_lower = text.lower()
    is_numerical = bool(re.search(r'\d', text)) and any(k in text_lower for k in ["calculate", "find", "determine", "evaluate", "?"])
    has_derivation = any(k in text_lower for k in ["derive", "obtain an expression", "prove that", "show that"])
    has_diagram = any(k in text_lower for k in ["fig.", "figure", "diagram", "given in the figure", "as shown"])
    has_graph = any(k in text_lower for k in ["graph", "plot", "curve", "characteristic curve", "vi characteristic"])
    
    return is_numerical, has_derivation, has_diagram, has_graph

def is_hindi_page(text):
    # Detect garbled Hindi fonts by frequency of specific mapped symbols
    hindi_score = text.count('{') + text.count('}') + text.count('$') + text.count('©') + text.count('~')
    return hindi_score > 50

def main(directory):
    pdf_files = glob.glob(os.path.join(directory, "**", "*.pdf"), recursive=True)
    
    db = {
        "metadata": {
            "examBoard": "CBSE",
            "subject": "Physics",
            "class": 12,
            "subjectCode": "042",
            "extractionTimestamp": datetime.utcnow().isoformat() + "Z",
            "totalPapersProcessed": 0,
            "totalQuestionsExtracted": 0,
            "unclassifiedCount": 0,
            "ambiguousCount": 0,
            "papersList": []
        },
        "questions": []
    }
    
    report_lines = ["# Extraction Report", ""]
    
    failed_pdfs = []
    unclassified_qs = []
    ambiguous_qs = []
    
    for pdf_path in pdf_files:
        seen_texts_words = []
        filename = os.path.basename(pdf_path)
        year, ptype, set_num = parse_metadata(filename)
        
        try:
            doc = fitz.open(pdf_path)
            full_text = ""
            for page in doc:
                raw_text = page.get_text()
                if not is_hindi_page(raw_text):
                    full_text += raw_text + "\n"
            doc.close()
            
            q_extracted = extract_questions_from_text(full_text, filename, year, ptype, set_num)
            
            db["metadata"]["totalPapersProcessed"] += 1
            db["metadata"]["papersList"].append(filename)
            
            for q in q_extracted:
                q_id = f"{year}-{'COMP' if ptype == 'Compartment' else 'MAIN'}-S{set_num}-Q{q['q_num']}"
                
                # Deduplication logic (Fuzzy Jaccard)
                new_words = set(re.findall(r'\w+', q['text'].lower()))
                is_dup = False
                if len(new_words) >= 5:
                    for seen_words in seen_texts_words:
                        intersection = new_words.intersection(seen_words)
                        union = new_words.union(seen_words)
                        if len(union) > 0 and len(intersection) / len(union) > 0.85:
                            is_dup = True
                            break
                if is_dup:
                    continue
                if len(new_words) >= 5:
                    seen_texts_words.append(new_words)
                
                topic_code, topic_name, ambiguous, scores = classify_question(q['text'])
                is_num, has_deriv, has_diag, has_graph = detect_properties(q['text'])
                
                q_obj = {
                    "id": q_id,
                    "year": year,
                    "paperType": ptype,
                    "setNumber": set_num,
                    "questionNumber": str(q['q_num']),
                    "section": q['section'],
                    "marks": q['marks'],
                    "questionText": q['text'],
                    "topicCode": topic_code,
                    "topicName": topic_name,
                    "chapterName": TOPIC_MAP[topic_code]["chapter"] if topic_code != "00" else "Unclassified",
                    "unitName": TOPIC_MAP[topic_code]["unit"] if topic_code != "00" else "Unclassified",
                    "isNumerical": is_num,
                    "hasDerivation": has_deriv,
                    "hasDiagram": has_diag,
                    "hasGraph": has_graph,
                    "topicAmbiguous": ambiguous,
                    "topicScoreBreakdown": {k: v for k, v in scores.items() if v > 0},
                    "sourceFilename": filename,
                    "pageNumber": 1 # Simplified, as we process full text at once
                }
                
                db["questions"].append(q_obj)
                db["metadata"]["totalQuestionsExtracted"] += 1
                
                if topic_code == "00":
                    db["metadata"]["unclassifiedCount"] += 1
                    unclassified_qs.append(q_obj)
                
                if ambiguous:
                    db["metadata"]["ambiguousCount"] += 1
                    ambiguous_qs.append(q_obj)
                    
            report_lines.append(f"- Processed `{filename}`: {len(q_extracted)} questions.")
            
        except Exception as e:
            failed_pdfs.append(f"{filename}: {str(e)}")
            report_lines.append(f"- FAILED `{filename}`: {str(e)}")

    with open("physics_questions_database.json", "w") as f:
        json.dump(db, f, indent=2)
        
    report_lines.append("")
    report_lines.append("## Summary")
    report_lines.append(f"Total Papers Processed: {db['metadata']['totalPapersProcessed']}")
    report_lines.append(f"Total Failed PDFs: {len(failed_pdfs)}")
    report_lines.append(f"Total Questions Extracted: {db['metadata']['totalQuestionsExtracted']}")
    report_lines.append(f"Unclassified Count: {db['metadata']['unclassifiedCount']}")
    report_lines.append(f"Ambiguous Count: {db['metadata']['ambiguousCount']}")
    
    report_lines.append("\n## Failed PDFs")
    for fp in failed_pdfs:
        report_lines.append(f"- {fp}")
        
    report_lines.append("\n## Unclassified Questions")
    for uq in unclassified_qs:
        report_lines.append(f"- {uq['id']}: {uq['questionText']}")
        
    report_lines.append("\n## Ambiguous Questions")
    for aq in ambiguous_qs:
        report_lines.append(f"- {aq['id']}: {aq['questionText']}")

    with open("extraction_report.md", "w") as f:
        f.write('\n'.join(report_lines))

if __name__ == "__main__":
    import sys
    directory = sys.argv[1] if len(sys.argv) > 1 else "./papers/"
    main(directory)
