import streamlit as st
import pandas as pd
import spacy
from spacy import displacy
import uuid
import subprocess

# -------------------------------
# Load SpaCy model (auto-download if missing)
# -------------------------------
@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

nlp = load_model()

# -------------------------------
# Initialize session state
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="Extracting Key Information (Named Entity Recognition)", layout="wide")

st.title("🔍 Extracting Key Information (Named Entity Recognition)")
st.caption("Extract and visualize entities from customer queries using SpaCy")

# -------------------------------
# Input Section
# -------------------------------
st.subheader("Enter Text")
input_text = st.text_area("Type your query here:", st.session_state.input_text, height=120)

col1, col2 = st.columns([1,1])

if col1.button("Analyze"):
    if input_text.strip():
        doc = nlp(input_text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        df = pd.DataFrame(entities, columns=["entity", "label"]) if entities else pd.DataFrame(columns=["entity","label"])
        html = displacy.render(doc, style="ent", jupyter=False)

        item_id = str(uuid.uuid4())
        st.session_state.history.insert(0, {
            "id": item_id,
            "text": input_text,
            "entities_df": df,
            "entities_html": html
        })
        st.session_state.input_text = input_text
        st.rerun()
    else:
        st.warning("Please enter some text first.")

if col2.button("Clear All"):
    st.session_state.history = []
    st.session_state.input_text = ""
    st.rerun()

st.markdown("---")

# -------------------------------
# Display latest results
# -------------------------------
if st.session_state.history:
    recent = st.session_state.history[0]

    st.subheader("Visualized Entities (displaCy)")
    st.components.v1.html(recent["entities_html"], height=180, scrolling=True)

    st.subheader("Entities Table")
    df_display = recent["entities_df"]

    # Filter by label
    labels = ["ALL"] + sorted(df_display["label"].unique().tolist()) if not df_display.empty else ["ALL"]
    chosen = st.selectbox("Filter by entity label", labels, index=0)

    if chosen == "ALL":
        filtered_df = df_display
    else:
        filtered_df = df_display[df_display["label"] == chosen]

    st.dataframe(filtered_df if not filtered_df.empty else pd.DataFrame(columns=["entity","label"]))

    # Download CSV
    if not df_display.empty:
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button("Download Entities CSV", csv, file_name="entities.csv", mime='text/csv')

    st.markdown("**Entity counts:**")
    counts = df_display["label"].value_counts() if not df_display.empty else pd.Series(dtype=int)
    st.write(counts)

else:
    st.info("No queries analyzed yet. Type a query and press Analyze 🔍")

# -------------------------------
# History Panel
# -------------------------------
with st.sidebar:
    st.subheader("History")

    if st.button("📝 New Chat"):
        st.session_state.input_text = ""
        st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.session_state.input_text = ""
        st.rerun()

    st.markdown("---")

    if not st.session_state.history:
        st.write("— No history yet —")
    else:
        for item in st.session_state.history:
            with st.expander(item["text"][:120]):
                st.write("**Text:**", item["text"])
                st.write("**Entities:**")
                st.write(item["entities_df"] if not item["entities_df"].empty else "No entities found.")
                cols = st.columns([1,1,1])
                if cols[0].button("Load", key=f"load-{item['id']}"):
                    st.session_state.input_text = item["text"]
                    st.rerun()
                if cols[1].button("Delete", key=f"del-{item['id']}"):
                    st.session_state.history = [h for h in st.session_state.history if h["id"] != item["id"]]
                    st.rerun()
                if cols[2].button("View displaCy", key=f"view-{item['id']}"):
                    st.components.v1.html(item["entities_html"], height=220, scrolling=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption(
    "💡 Tip: If displaCy visualization doesn't show colors, try resizing the window. "
    "SpaCy model will auto-download if not found."
)
