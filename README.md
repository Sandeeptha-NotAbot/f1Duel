# 🏁 f1Duel: A Head-to-Head Driver Battle Analyzer

**f1Duel** is an interactive Streamlit app that lets you compare Formula 1 drivers head-to-head across any race session using [FastF1](https://theoehrly.github.io/Fast-F1/). Dive into lap times, performance gaps, tyre strategies, and even animated visualizations!

---

## 🚀 Features

- 📅 Select season, race, and session (Race, Qualifying, Practice)
- 🧠 Automatically generates driver list for selected session
- 📊 Lap time comparison plot between two drivers
- 🥇 Podium and race summary with flags, teams, and tyre info
- 📈 Animated lap-by-lap delta graph
- 👻 Ghost lap speed comparison animation
- ⚡ Built using `FastF1`, `Plotly`, `Pandas`, and `Streamlit`

---

## 🧰 Installation

```bash
git clone https://github.com/Sandeeptha-NotAbot/f1Duel.git
cd f1Duel
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
