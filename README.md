<div align="center">

# ☕ NomadSpots
### *A Global Workspace & Coffee Scout for Digital Nomads*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Folium](https://img.shields.io/badge/GIS-Folium%2FLeaflet-green?style=for-the-badge&logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Discover, rate, and map the best remote work cafes and workspaces worldwide with zero API key dependencies and a gorgeous dark-roast glassmorphism UI.*

[✨ View Live Demo](#-local-installation) • [🚀 Quick Start](#-local-installation-and-setup)

</div>

---

## ☕ About The Project

**NomadSpots** is a lightweight, high-performance web application designed for remote workers, freelancers, and digital nomads scouting out reliable Wi-Fi, great coffee, and inspiring workspaces across cities globally. 

Built with **Streamlit** and interactive GIS mapping, it combines a sleek espresso dark-mode aesthetic with practical tools like one-click Google Maps directions and a built-in AI recommendation engine.

---

## ✨ Key Features

* **🗺️ Multi-Layer Global Atlas:** Powered by `Folium`, featuring seamless layer switching between **CartoDB Dark Matter**, **OpenStreetMap**, and **Google Satellite** imagery.
* **📍 One-Click Google Maps Integration:** Every mapped pin and directory card includes direct navigation links to open exact coordinates instantly in Google Maps.
* **⭐ Detailed Workspace Ratings:** Filter and evaluate spots based on Wi-Fi reliability, coffee quality, and atmospheric vibes (e.g., *Quiet & Productive*, *Social & Creative*).
* **🤖 AI Nomad Advisor:** An intelligent suggestion engine that matches user prompts with the best-suited workspace in the directory.
* **✨ Community Submissions:** An interactive form allowing users worldwide to pin and publish new cafes to the global atlas.

---

## 🛠️ Tech Stack

* **Frontend & Framework:** Streamlit (Python)
* **GIS & Mapping:** Folium, Leaflet.js, Streamlit-Folium
* **Data Management:** Pandas
* **UI Design:** Custom CSS, Glassmorphism, Dark-Roast Coffee Palette

---

## 📁 Repository Structure

```text
nomad-spots/
├── .streamlit/
│   └── config.toml      # Theme & configuration settings
├── app.py               # Main application logic & UI
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation