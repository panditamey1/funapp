import streamlit as st
import json
import os
from datetime import datetime, time

CHECKLIST_FILE = "trading_checklist.json"

DEFAULT_ITEMS = [
    # Original items
    "Are market conditions (volatility, trend) right for this trade?",
    "Are there major news events that may occur during the trade?",
    "Correct entry point based on strategy?",
    "Is the stop loss reasonable for the potential reward?",
    "How am I getting out of this trade? (Describe)",
    "Is my position size correct?",
    "Am I violating any of my Trading Plan rules?",
    "Am I allowed to trade? (Not on a forced break due to recent losses)",
    "Am I placing this order in the correct hours/my established trading time?",
    "Is it within my max number of positions I can hold at one time?",
    "Is it within my leverage tolerance?",
    "Did I find this trade through the proper means? (Not a 'tip' but from my own research)",
    "What should I remember during the trade? (Key point you've struggled with recently)",
    "Am I in the right mind frame for this trade?",
    # Your additional items
    "My expectations are realistic",
    "I have a probability-tested edge",
    "Trading aligns with my 'ideal self'",
    "No one is influencing me",
    "My entry criteria is clear, now I wait",
    "I am self-aware of my impulses",
    "Sleep was great, exercise was great",
    "My brain and belly have been fed",
    "Trades must meet my criteria",
    "I completely accept my defined risk",
    "Position size is in-line with my process",
    "Good habits are forming in my trading",
    "I am calm, relaxed, and focused"
]

def load_checklist():
    if os.path.exists(CHECKLIST_FILE):
        with open(CHECKLIST_FILE, "r") as f:
            return json.load(f)
    else:
        return {"items": DEFAULT_ITEMS, "checked": []}

def save_checklist(data):
    with open(CHECKLIST_FILE, "w") as f:
        json.dump(data, f)

st.title("📝 Daily Trading Checklist")

data = load_checklist()
items = data.get("items", [])
checked = set(data.get("checked", []))

# Add new checklist item
with st.form(key="add_item_form"):
    new_item = st.text_input("Add a new checklist item", "")
    submitted = st.form_submit_button("Add")
    if submitted and new_item.strip():
        items.append(new_item.strip())
        st.success(f"Added: {new_item.strip()}")

# Show checklist with checkboxes
checked_today = []
for idx, item in enumerate(items):
    checked_state = st.checkbox(item, key=f"item_{idx}", value=(item in checked))
    if checked_state:
        checked_today.append(item)

# Remove checklist item
st.write("### Remove Items")
to_delete = st.multiselect("Select checklist items to remove", options=items)
if st.button("Delete selected"):
    items = [item for item in items if item not in to_delete]
    checked = [item for item in checked if item not in to_delete]
    st.success(f"Deleted: {', '.join(to_delete)}")

# Save checklist status
data = {"items": items, "checked": checked_today}
save_checklist(data)

# Reminder: Must complete before 9 am
now = datetime.now()
cutoff = time(9, 0)
if now.time() < cutoff:
    st.info(f"⏰ Please complete this checklist before **9:00 am**! ({now.strftime('%H:%M')})")
else:
    if len(checked_today) == len(items) and items:
        st.success("✅ All checklist items completed for today!")
    else:
        st.warning("⚠️ You haven't completed all checklist items today.")

st.write("---")
st.caption("Tip: Keep this checklist open every morning. Add/remove items as you refine your trading process.")
