# 🎓 Forms Kart: JEE College Predictor Tool

**Forms Kart - Office Work** is a web-based college prediction tool designed for counselors and students participating in JEE Advanced/Main. It uses real admission data to predict possible colleges and branches a student can get based on their rank, category, gender, and preferences.

---

## 🌟 Features

- ✅ Predicts colleges based on JEE Advanced/Main rank
- 📈 Visualizes options with **interactive bar and pie charts**
- 🎯 Highlights top 5 most suitable colleges and branches
- 📥 Allows download of filtered results in CSV
- 🏫 Includes all IITs, NITs, and IIITs with up-to-date category-wise cutoff data
- ⚙️ Supports branch preferences and dual-degree filtering
- 📊 Real-time metrics on available colleges and branches

---

## 🖥️ Demo

> _Coming Soon_

---

## 📁 Project Structure

```bash
.
├── main.py                 # Streamlit app main interface
├── preprocessor.py         # Loads and standardizes cutoff CSV data
├── helper.py               # Filtering logic and graph generation
├── *.csv                   # Category-wise cutoff data (stored externally)
