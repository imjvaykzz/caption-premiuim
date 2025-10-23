import openai
import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
# Securely use API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="AI Premium Caption Generator", page_icon="🚀", layout="centered")
st.title("🚀 AI Premium Caption Generator")
st.write("Generate multi-platform social media captions + hashtags instantly!")

# Sidebar options
st.sidebar.header("Settings")
platform = st.sidebar.selectbox("Select platform:", ["Instagram", "TikTok", "YouTube", "Twitter"])
tone = st.sidebar.selectbox("Tone/Style:", ["Funny", "Motivational", "Professional", "Casual", "Sarcastic"])
bulk_input = st.sidebar.text_area("Enter multiple topics (one per line):")
num_captions = st.sidebar.slider("Number of captions per topic:", 1, 10, 5)
temperature = st.sidebar.slider("Creativity (temperature):", 0.5, 1.0, 0.8, 0.05)
export_format = st.sidebar.selectbox("Export format:", ["CSV", "TXT"])

# Function to generate captions using OpenAI
def generate_captions(topic):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a creative social media caption generator for {platform} in {tone} tone."},
                {"role": "user", "content": f"Generate {num_captions} captions with hashtags for this topic: {topic}"}
            ],
            temperature=temperature
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# ---------------- MAIN ----------------
if st.button("Generate Captions"):
    topics = [t.strip() for t in bulk_input.split('\n') if t.strip()] if bulk_input else []
    if not topics:
        st.warning("Please enter at least one topic.")
    else:
        all_captions = []
        for topic in topics:
            st.subheader(f"Topic: {topic}")
            captions = generate_captions(topic)
            st.text_area(f"Captions for '{topic}':", captions, height=200)
            all_captions.append({"Topic": topic, "Captions": captions})

        # Export options
        if export_format == "CSV":
            df = pd.DataFrame(all_captions)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, file_name="captions.csv", mime="text/csv")
        else:
            txt = "\n\n".join([f"{a['Topic']}:\n{a['Captions']}" for a in all_captions])
            st.download_button("Download TXT", txt, file_name="captions.txt", mime="text/plain")
