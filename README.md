# 🔍 RedLens – Reddit User Persona Analyzer

**RedLens** is a Python tool that analyzes Reddit users by scraping their public posts and comments to generate a comprehensive **user persona** — with **citations** from the source content.


---

## 🚀 Features

✅ **Reddit Profile Scraping**  
✅ **Persona Inference (Demographics, Interests, Style)**  
✅ **LLM/NLP-enhanced Pattern Extraction**  
✅ **Citation System** (links to supporting posts/comments)  
✅ **Command Line Interface**  
✅ **Rate-Limiting & Error Handling**  
✅ **Configurable Limits and Delay** via `config.ini`

---

## 🛠️ Installation & Setup

### ✅ Prerequisites

* Python 3.7+
* Internet connection (to access Reddit’s public API)

---

### 🔧 Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/PraTham-Patill/RedLens.git
cd RedLens

# 2. Install required packages
pip install -r requirements.txt
```

---

## 📖 Usage

Run the persona analyzer with a Reddit profile URL:

```bash
python reddit_persona_analyzer.py <reddit_profile_url>
```

---

### ⚙️ Command Line Options

| Option     | Description                                  |
| ---------- | -------------------------------------------- |
| `<url>`    | Reddit user profile URL (required)           |
| `--output` | Custom output filename (optional)            |
| `--limit`  | Max posts/comments to analyze (default: 100) |
| `--delay`  | Delay between requests (default: 1.0 sec)    |

---

### 📌 Example Usage

```bash
# Basic usage
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/

# Custom output name
python reddit_persona_analyzer.py https://www.reddit.com/user/Hungry-Move-6603/ --output hungry_output.txt

# Increased limit & delay
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/ --limit 150 --delay 2.0
```

---

## 📂 Output Format

Each output `.txt` file includes:

1. **User Summary** – username, activity stats
2. **Demographics** – age estimate, gender, location, education, occupation
3. **Interests & Subreddits**
4. **Communication Style** – tone, formality, humor
5. **Community Behavior** – post/comment patterns
6. **🔗 Citations** – links to posts/comments for each trait

---

## 🧪 Sample Output Files

These files are included in the repo for evaluation:

* `kojied_persona.txt`
* `Hungry-Move-6603_persona.txt`

---

## 📁 Project Structure

```
RedLens/
├── reddit_persona_analyzer.py     # Main script
├── test_analyzer.py               # Optional test script
├── config.ini                     # Delay/limit settings
├── requirements.txt               # Python dependencies
├── kojied_persona.txt             # Output sample 1
├── Hungry-Move-6603_persona.txt   # Output sample 2
├── README.md                      # Documentation
└── .gitignore                     # Ignored files
```

---

## 🔧 Technical Summary

* **Public Reddit API:** No authentication required
* **Scraping Format:** JSON endpoints for posts and comments
* **Analysis:** Pattern recognition + simple NLP + rule-based inference
* **Output:** Structured persona report with post/comment citations
