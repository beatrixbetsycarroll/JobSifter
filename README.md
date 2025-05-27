# JobSifter

This project is a modular pipeline for ingesting job postings, applying approval rules, and storing/logging the results. Built for a technical interview prompt by The Ladders.

---

## 📦 Features

- Parses job feeds from multiple formats (dicts, flat strings)
- Normalizes fields like salary, location, and language
- Evaluates job postings based on configurable rules:
  - Must be remote or based in US/Canada
  - Must be full-time
  - Must meet salary threshold ($100K yearly or $45/hour)
  - Must not be from staffing firms
  - Must be in English (or French if in Canada)
- Stores approved jobs in:
  - In-memory list (for publication)
  - `approved_jobs.json` (as a mocked persistence layer)
- Logs rejected jobs with reasons

---

## 🚀 How to Run

```bash
python -m jobsifter.main path_to_feed_data_file
# for example:
python -m jobsifter.main data/feed2.json
```
If you don't specify a file, it will default to running it on data/feed1.json.

---

## 📁 Project Structure

```bash
jobsifter/
├── main.py               # Entry point
├── models/               # Typed data models (JobPosting, Salary, etc.)
├── ingestion/parser.py   # Feed parsing and normalization
├── approval/evaluator.py # Rule-based job approval
├── storage/writer.py     # File output for approved + rejected jobs
├── constants.py          # Shared constants (e.g., salary thresholds)
```
---

## 🧠 Assumptions / Design Notes

- **Salary inference**:
  - If a salary period is missing, we infer `"hourly"` if the amount is under $200
- **Language fallback**:
  - If the language is empty or missing, we default to `"English"`
  - We assume the `language` field refers to metadata, not the text content of the description
- **Location + Employment filtering**:
  - Jobs must be remote or in the US/Canada
  - Only "Full-Time" jobs are allowed (e.g., internships and contracts are rejected)
- **Date handling**:
  - Posting date is treated as a string, but could easily be parsed as a `datetime`
- **Input validation**:
  - Feed JSON files may have trailing garbage — we handle that gracefully
- **Testability**:
  - Code is fully modular and typed for easy unit testing and extension

---

## 🧪 Future Ideas

- Add real language detection on job descriptions
- Add LLM API integration for further customization (for many possible uses)
- Plug in a real DB or job publishing API
- Add CLI flags for verbosity or output file control
