import json
import random
from datetime import datetime
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

st.set_page_config(
    page_title="NomadSpots | Vintage Workspace & Coffee Scout",
    page_icon="☕",
    layout="wide",
)

# ==============================================================================
# 📜 VINTAGE LIGHT PARCHMENT & COFFEEHOUSE THEME (CSS)
# ==============================================================================
custom_css = """
<style>
/* Authentic Aged Parchment Background with Subtle Grid */
.stApp {
    background-color: #F5F1E8;
    background-image: radial-gradient(#E3D6B8 0.75px, transparent 0.75px), 
                      radial-gradient(#E3D6B8 0.75px, #F5F1E8 0.75px);
    background-size: 30px 30px;
    background-position: 0 0, 15px 15px;
}

/* Antique Sepia & Espresso Typography */
html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #2D231B !important;
    font-family: 'Georgia', serif;
}

/* Notebook Header styling with antique underline */
h1 {
    font-family: 'Georgia', serif;
    font-weight: 800;
    color: #4A3525 !important;
    border-bottom: 2px solid #C4B495;
    padding-bottom: 10px;
}
h2, h3 {
    font-family: 'Georgia', serif;
    color: #5C3A21 !important;
    font-weight: 700;
}

/* Paper Journal Container Cards */
div[data-testid="stBlock"] {
    background-color: #FCF9F2 !important;
    border-radius: 6px;
    border: 1px solid #C4B495;
    box-shadow: 3px 5px 15px rgba(45, 35, 27, 0.08);
    padding: 1.4rem;
}

/* Deep Leather Brown Accent Buttons */
div.stButton > button, div.stDownloadButton > button {
    background-color: #5C3A21 !important;
    color: #F5F1E8 !important;
    border-radius: 4px !important;
    border: 1px solid #3B2414 !important;
    font-family: 'Georgia', serif;
    font-weight: 600;
    transition: all 0.2s ease;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    background-color: #432A17 !important;
}

/* Custom Metrics */
[data-testid="stMetricValue"] {
    color: #5C3A21 !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    color: #554235 !important;
    font-weight: 600;
}

/* Custom Styled Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: #E8DECA !important;
    border-radius: 4px 4px 0px 0px;
    border: 1px solid #C4B495;
    color: #4A3525 !important;
    padding: 10px 18px;
    font-weight: 600;
    font-family: 'Georgia', serif;
}
.stTabs [aria-selected="true"] {
    background-color: #5C3A21 !important;
    color: #F5F1E8 !important;
    font-weight: 700 !important;
}

/* Input Fields styling for vintage paper */
input, select, textarea {
    background-color: #FCF9F2 !important;
    color: #2D231B !important;
    border: 1px solid #C4B495 !important;
    border-radius: 4px !important;
    font-family: 'Georgia', serif !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==============================================================================
# 📍 INITIALIZE DEFAULT NOMAD SPOTS
# ==============================================================================
if "spots" not in st.session_state:
  st.session_state.spots = [
      {
          "id": 1,
          "name": "Archive Coffee & Workspace",
          "city": "Canggu, Bali",
          "lat": -8.6574,
          "lon": 115.1325,
          "wifi_rating": 5,
          "coffee_rating": 5,
          "vibe": "Quiet & Productive",
          "notes": (
              "Lightning fast Wi-Fi, excellent pour-overs, air-conditioned"
              " indoor booths."
          ),
          "check_ins": [
              "☕ Checked in Jan 2026: Amazing flat whites and steady AC!"
          ],
      },
      {
          "id": 2,
          "name": "The Globe & Bean Roastery",
          "city": "Lisbon, Portugal",
          "lat": 38.7169,
          "lon": -9.1399,
          "wifi_rating": 4,
          "coffee_rating": 5,
          "vibe": "Social & Creative",
          "notes": (
              "Great sunlight, communal tables, fills up fast by 11 AM. Amazing"
              " flat whites."
          ),
          "check_ins": ["🥐 Checked in Dec 2025: Perfect morning sunlight."],
      },
      {
          "id": 3,
          "name": "Kinfolk Library & Cafe",
          "city": "Tokyo, Japan",
          "lat": 35.6620,
          "lon": 139.7038,
          "wifi_rating": 5,
          "coffee_rating": 4,
          "vibe": "Ultra Quiet",
          "notes": (
              "Stunning minimalist wooden interior. Strict quiet zone on the"
              " second floor."
          ),
          "check_ins": [],
      },
      {
          "id": 4,
          "name": "Café Botanico",
          "city": "Medellín, Colombia",
          "lat": 6.2442,
          "lon": -75.5812,
          "wifi_rating": 4,
          "coffee_rating": 5,
          "vibe": "Lush & Breezy",
          "notes": (
              "Open-air garden workspace surrounded by tropical plants."
              " Reliable power outlets."
          ),
          "check_ins": [],
      },
  ]

# ==============================================================================
# 🤖 AI NOMAD ASSISTANT LOGIC
# ==============================================================================


def ask_ai_advisor(prompt, spots_df):
  if spots_df.empty:
    return "No spots available in the database yet!"

  prompt_lower = prompt.lower()
  matches = []
  for _, row in spots_df.iterrows():
    score = 0
    if (
        "quiet" in prompt_lower
        and "quiet" in str(row["vibe"]).lower()
        or "quiet" in str(row["notes"]).lower()
    ):
      score += 3
    if "fast" in prompt_lower and row["wifi_rating"] == 5:
      score += 3
    if "coffee" in prompt_lower and row["coffee_rating"] == 5:
      score += 3
    if "social" in prompt_lower and "social" in str(row["vibe"]).lower():
      score += 2
    score += row["wifi_rating"] + row["coffee_rating"]
    matches.append((score, row))

  matches.sort(key=lambda x: x[0], reverse=True)
  best_match = matches[0][1]

  return (
      f"🤖 **AI Advisor Recommendation:**\n\nBased on your prompt"
      f' (*"{prompt}"*) — I suggest **{best_match["name"]}** in'
      f" **{best_match['city']}**!\n\n- 📶 **Wi-Fi:**"
      f" {'⭐' * best_match['wifi_rating']}\n- ☕ **Coffee:**"
      f" {'⭐' * best_match['coffee_rating']}\n- 🏷️ **Atmosphere:**"
      f" `{best_match['vibe']}`\n\n> *\"{best_match['notes']}\"*"
  )


# ==============================================================================
# 🖥️ APP HEADER & METRICS
# ==============================================================================
st.title("☕ NomadSpots")
st.markdown(
    "*A spatial field notebook and directory for remote workers worldwide.*"
)

df = pd.DataFrame(st.session_state.spots)
total_spots = len(df)
avg_wifi = round(df["wifi_rating"].mean(), 1) if not df.empty else 0
avg_coffee = round(df["coffee_rating"].mean(), 1) if not df.empty else 0

col1, col2, col3 = st.columns(3)
col1.metric(label="Saved Workspace Havens", value=total_spots)
col2.metric(label="Global Avg Wi-Fi", value=f"{avg_wifi} / 5 ⭐")
col3.metric(label="Global Avg Brew", value=f"{avg_coffee} / 5 ⭐")

st.divider()

# ==============================================================================
# 📑 TABS: MAP vs DIRECTORY vs ADD SPOT vs AI vs GUIDE
# ==============================================================================
tab_map, tab_directory, tab_add, tab_ai, tab_guide = st.tabs([
    "🗺️ Global Map",
    "☕ Directory & Check-ins",
    "✨ Submit Haven",
    "🤖 AI Advisor",
    "🎒 Export Guide",
])

with tab_map:
  st.markdown("### Mapped workspaces")
  st.caption(
      "Switch between OpenStreetMap and Google Satellite layers using the map"
      " control in the top-right corner."
  )

  m = folium.Map(
      location=[20.0, 0.0],
      zoom_start=2,
      tiles="OpenStreetMap",
      name="OpenStreetMap",
  )
  folium.TileLayer(
      tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
      attr="Google Satellite",
      name="Google Satellite",
      max_zoom=20,
  ).add_to(m)

  for spot in st.session_state.spots:
    gmaps_url = (
        f"https://www.google.com/maps/search/?api=1&query={spot['lat']},{spot['lon']}"
    )
    popup_html = f"""
        <div style="font-family: Georgia, serif; width: 220px; color: #2D231B;">
            <h4 style="margin:0; color:#5C3A21;">{spot['name']}</h4>
            <p style="margin:4px 0; font-size:12px;">📍 <b>{spot['city']}</b></p>
            <p style="margin:4px 0; font-size:12px;">📶 Wi-Fi: {'⭐'*spot['wifi_rating']}</p>
            <p style="margin:4px 0; font-size:12px;">☕ Coffee: {'⭐'*spot['coffee_rating']}</p>
            <p style="margin:4px 0; font-size:12px;">🏷️ {spot['vibe']}</p>
            <hr style="margin:4px 0; border-top: 1px solid #C4B495;">
            <p style="font-size:11px; color:#555;">{spot['notes']}</p>
            <a href="{gmaps_url}" target="_blank" style="display:block; margin-top:6px; font-size:12px; color:#5C3A21; font-weight:bold; text-decoration:none;">🗺️ Open in Google Maps</a>
        </div>
        """
    folium.Marker(
        location=[spot["lat"], spot["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=spot["name"],
        icon=folium.Icon(color="orange", icon="coffee", prefix="fa"),
    ).add_to(m)

  folium.LayerControl().add_to(m)
  st_folium(m, width=1200, height=520)

with tab_directory:
  st.markdown("### Curated Cafe & Workspace Journal")

  # Search and Filter Controls
  s1, s2, s3 = st.columns([2, 1, 1])
  with s1:
    search_query = st.text_input(
        "🔍 Instant Search", placeholder="Type a cafe name or city..."
    )
  with s2:
    vibe_filter = st.selectbox(
        "Atmosphere", ["All"] + list(df["vibe"].unique())
    )
  with s3:
    min_wifi = st.slider("Min Wi-Fi ⭐", min_value=1, max_value=5, value=1)

  # Apply Filters & Search
  filtered_df = df.copy()
  if search_query:
    filtered_df = filtered_df[
        filtered_df["name"].str.contains(search_query, case=False, na=False)
        | filtered_df["city"].str.contains(
            search_query, case=False, na=False
        )
    ]
  if vibe_filter != "All":
    filtered_df = filtered_df[filtered_df["vibe"] == vibe_filter]
  filtered_df = filtered_df[filtered_df["wifi_rating"] >= min_wifi]

  if filtered_df.empty:
    st.info("No workspaces match your search criteria.")

  for _, row in filtered_df.iterrows():
    gmaps_url = (
        f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
    )
    spot_checkins = row.get("check_ins", [])
    if isinstance(spot_checkins, float):
      spot_checkins = []

    with st.container():
      col_a, col_b = st.columns([4, 1])
      with col_a:
        st.markdown(f"#### ☕ {row['name']} — *{row['city']}*")
        st.markdown(
            f"**📶 Wi-Fi:** `{'⭐'*row['wifi_rating']}` &nbsp;|&nbsp; **☕"
            f" Brew:** `{'⭐'*row['coffee_rating']}` &nbsp;|&nbsp; **🏷️"
            f" Atmosphere:** `{row['vibe']}`"
        )
        st.info(row["notes"])

        if spot_checkins:
          st.markdown("**💬 Community Check-ins:**")
          for checkin in spot_checkins:
            st.markdown(f"> *{checkin}*")

        with st.expander(f"➕ Add Check-in for {row['name']}"):
          new_checkin = st.text_input(
              "Your tip or update",
              placeholder="e.g., Great seating near the back window today",
              key=f"checkin_input_{row['id']}",
          )
          if st.button("Post Check-in", key=f"post_{row['id']}"):
            if new_checkin:
              timestamp = datetime.now().strftime("%b %Y")
              for s in st.session_state.spots:
                if s["id"] == row["id"]:
                  if "check_ins" not in s:
                    s["check_ins"] = []
                  s["check_ins"].append(
                      f"💬 Checked in {timestamp}: {new_checkin}"
                  )
              st.success("Check-in added successfully!")
              st.rerun()

        st.markdown(f"[🗺️ Open Directions in Google Maps]({gmaps_url})")

      with col_b:
        if st.button("Delete Spot", key=f"del_{row['id']}"):
          st.session_state.spots = [
              x for x in st.session_state.spots if x["id"] != row["id"]
          ]
          st.rerun()
      st.divider()

with tab_add:
  st.markdown("### Record a New Workspace Haven")
  st.markdown(
      "Pin a new work-friendly cafe or remote workspace to your field"
      " notebook."
  )

  with st.form("add_spot_form"):
    spot_name = st.text_input(
        "Spot Name", placeholder="e.g., Stumptown Coffee Roasters"
    )
    spot_city = st.text_input("City & Country", placeholder="e.g., Portland, USA")

    c1, c2 = st.columns(2)
    with c1:
      spot_lat = st.number_input("Latitude", value=45.5152, format="%.4f")
    with c2:
      spot_lon = st.number_input("Longitude", value=-122.6784, format="%.4f")

    c3, c4 = st.columns(2)
    with c3:
      wifi_rate = st.slider("Wi-Fi Reliability ⭐", 1, 5, 5)
    with c4:
      coffee_rate = st.slider("Coffee / Brew Quality ⭐", 1, 5, 5)

    spot_vibe = st.selectbox(
        "Atmosphere / Vibe",
        [
            "Quiet & Productive",
            "Social & Creative",
            "Ultra Quiet",
            "Lush & Breezy",
            "Casual & Cozy",
        ],
    )
    spot_notes = st.text_area(
        "Field Review",
        placeholder=(
            "Plug availability, noise levels, natural lighting, seating..."
        ),
    )

    submitted = st.form_submit_button("Seal Entry in Atlas")
    if submitted:
      if spot_name and spot_city:
        new_id = (
            max([x["id"] for x in st.session_state.spots]) + 1
            if st.session_state.spots
            else 1
        )
        st.session_state.spots.append({
            "id": new_id,
            "name": spot_name,
            "city": spot_city,
            "lat": spot_lat,
            "lon": spot_lon,
            "wifi_rating": wifi_rate,
            "coffee_rating": coffee_rate,
            "vibe": spot_vibe,
            "notes": spot_notes,
            "check_ins": [],
        })
        st.success(f"Successfully recorded '{spot_name}' in your atlas!")
        st.rerun()
      else:
        st.error("Please provide a spot name and city.")

with tab_ai:
  st.markdown("### 🤖 AI Nomad Recommendation Engine")
  st.markdown(
      "Describe what kind of environment you need, and let the AI find your"
      " ideal workspace."
  )

  user_prompt = st.text_input(
      "Describe your dream workspace today:",
      placeholder=(
          "e.g., I need a quiet place with 5-star wifi and amazing pour-over"
          " coffee"
      ),
  )
  if st.button("Get AI Recommendation"):
    if user_prompt:
      ai_response = ask_ai_advisor(user_prompt, df)
      st.markdown(ai_response)
    else:
      st.warning("Please type a request for the AI advisor.")

with tab_guide:
  st.markdown("### 🎒 Export Travel & Workspace Guide")
  st.markdown(
      "Compile all current workspace havens into a clean Markdown travel guide"
      " to take with you."
  )

  guide_markdown = "# ☕ NomadSpots Travel & Workspace Guide\n\n"
  guide_markdown += (
      f"*Generated on {datetime.now().strftime('%B %d, %Y')}*\n\n---\n\n"
  )

  for _, row in df.iterrows():
    gmaps_url = (
        f"https://www.google.com/maps/search/?api=1&query={row['lat']},{row['lon']}"
    )
    guide_markdown += f"### ☕ {row['name']} ({row['city']})\n"
    guide_markdown += (
        f"- **Wi-Fi:** {'⭐'*row['wifi_rating']} | **Coffee:**"
        f" {'⭐'*row['coffee_rating']} | **Vibe:** `{row['vibe']}`\n"
    )
    guide_markdown += f"- **Notes:** {row['notes']}\n"
    spot_checkins = row.get("check_ins", [])
    if isinstance(spot_checkins, list) and spot_checkins:
      guide_markdown += "- **Check-ins:**\n"
      for c in spot_checkins:
        guide_markdown += f"  - {c}\n"
    guide_markdown += f"- [Open in Google Maps]({gmaps_url})\n\n---\n\n"

  st.text_area(
      "Markdown Guide Preview", value=guide_markdown, height=300
  )

  st.download_button(
      label="📥 Download Travel Guide (.md)",
      data=guide_markdown,
      file_name="nomad_spots_guide.md",
      mime="text/markdown",
  )
