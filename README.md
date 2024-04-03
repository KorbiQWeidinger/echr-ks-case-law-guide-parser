# echr-ks-case-law-guide-parser

Parser for ECHR case law guides.

These guides are property of the ECHR.
They were scraped for educational/research purposes.

Source: [all-case-law-guides](https://ks.echr.coe.int/web/echr-ks/all-case-law-guides)
Dump: `echr_case_law_guides.csv`

### Parsing format / goal

Goal: extract all paragraphs from each case law guide
Format: paragraph, paragraph_nr, guide_id

### Development Instructions

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=value
deactivate
```
