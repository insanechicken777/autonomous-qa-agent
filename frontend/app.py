import streamlit as st
import requests
import json
import pandas as pd
from PIL import Image
import os

# ---------------------------------------------------------
# 1. PATH SETUP & CONFIGURATION
# ---------------------------------------------------------
BACKEND_URL = "http://127.0.0.1:8000"

# Calculate the absolute path to the assets folder
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../qa_agent/frontend
root_dir = os.path.dirname(current_dir)                  # .../qa_agent
icon_path = os.path.join(root_dir, "assets", "favicon.jpg")

# Try to load custom icon for Browser Tab
icon_image = "🕷️" # Fallback
if os.path.exists(icon_path):
    try:
        icon_image = Image.open(icon_path)
    except Exception:
        pass

st.set_page_config(
    page_title="QA Agent | Red Ops", 
    layout="wide", 
    page_icon=icon_image,
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS (RED & BLACK THEME)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* MAIN BACKGROUND */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* SIDEBAR BACKGROUND */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* HEADERS (RED) */
    h1, h2, h3, .main-header {
        color: #FF4B4B !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0px;
    }
    
    /* BUTTONS (RED GRADIENT) */
    .stButton>button {
        background: linear-gradient(45deg, #8B0000, #FF0000);
        color: white;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        text-transform: uppercase;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #FF0000, #FF4B4B);
        box-shadow: 0 0 15px #FF0000;
    }

    /* INPUT FIELDS (DARK GRAY) */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363D;
    }
    
    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363D;
    }
    
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161B22;
        border-radius: 4px;
        color: #888;
        font-weight: bold;
        text-transform: uppercase;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
        color: white !important;
    }

    /* SUCCESS BOX */
    .success-box {
        padding: 15px;
        background-color: #1f2937;
        border-left: 5px solid #00C851;
        color: #00C851;
        font-family: monospace;
        border-radius: 0px;
        margin-bottom: 10px;
    }
    
    /* ALERT BOX */
    .stAlert {
        background-color: #1f2937;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. MAIN HEADER WITH LOGO
# ---------------------------------------------------------
col_logo, col_title = st.columns([1, 15])

with col_logo:
    # === DEBUG LOGIC ===
    if os.path.exists(icon_path):
        # If file exists, show it
        st.image(icon_path, width=80)
    else:
        # If file missing, show explicit error so you can fix the path
        st.error("IMG 404")
        st.caption(f"Looking at: {icon_path}")
    # ===================

with col_title:
    st.title("AUTONOMOUS QA AGENT")
    st.markdown("**SYSTEM STATUS:** `ONLINE` | **MODE:** `RED OPS`")

# ---------------------------------------------------------
# 4. TABS LAYOUT
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["INGESTION (SETUP)", "AGENT (EXECUTION)"])

# =========================================================
# TAB 1: INGESTION
# =========================================================
with tab1:
    st.markdown("### 1. KNOWLEDGE BASE INGESTION")
    st.markdown("Upload project artifacts to train the Neural Network.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("SUPPORT DOCUMENTS (RULES)")
        uploaded_docs = st.file_uploader("Upload MD/TXT", accept_multiple_files=True, key="docs")
        
    with col2:
        st.warning("TARGET APPLICATION (DOM)")
        uploaded_html = st.file_uploader("Upload checkout.html", type=["html"], key="html")

    st.write("")
    build_btn = st.button("INITIALIZE KNOWLEDGE BASE", type="primary")
    
    if build_btn:
        if not uploaded_docs:
            st.error("NO DOCUMENTS DETECTED.")
        else:
            with st.spinner("VECTORIZING DOCUMENTS..."):
                files = []
                for doc in uploaded_docs:
                    files.append(("files", (doc.name, doc.getvalue(), doc.type)))
                
                try:
                    response = requests.post(f"{BACKEND_URL}/upload-documents/", files=files)
                    if response.status_code == 200:
                        st.markdown('<div class="success-box">CORE SYSTEMS ONLINE. VECTORS INDEXED.</div>', unsafe_allow_html=True)
                        with st.expander("VIEW VECTOR METADATA"):
                            st.json(response.json())
                    else:
                        st.error(f"SYSTEM FAILURE: {response.text}")
                except Exception as e:
                    st.error(f"CONNECTION LOST: {e}")

# =========================================================
# TAB 2: AGENTS
# =========================================================
with tab2:
    st.markdown("### 2. TEST OPERATIONS")
    
    # --- SECTION A: TEST CASES ---
    st.subheader("A. STRATEGY AGENT")
    
    col_q, col_btn = st.columns([4, 1])
    with col_q:
        default_query = "Generate positive and negative test cases for the discount code feature."
        feature_query = st.text_input("ENTER MISSION PARAMETERS:", value=default_query)
    with col_btn:
        st.write("") 
        st.write("") 
        generate_tc_btn = st.button("EXECUTE PLAN")

    if generate_tc_btn:
        if not feature_query:
            st.warning("INPUT REQUIRED.")
        else:
            with st.spinner("NEURAL PROCESSING..."):
                try:
                    payload = {"query": feature_query}
                    response = requests.post(f"{BACKEND_URL}/generate-tests/", data=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        tc_raw = data.get("test_cases", [])
                        
                        # --- ROBUST JSON PARSING ---
                        if isinstance(tc_raw, str):
                            try:
                                clean_json = tc_raw.replace("```json", "").replace("```", "").strip()
                                parsed_data = json.loads(clean_json)
                            except:
                                st.session_state['test_cases'] = []
                                st.error("DATA CORRUPTION DETECTED (Invalid JSON): " + tc_raw)
                                parsed_data = []
                        else:
                            parsed_data = tc_raw

                        # Unwrap dictionary if needed
                        if isinstance(parsed_data, dict):
                            if "test_cases" in parsed_data:
                                final_list = parsed_data["test_cases"]
                            else:
                                final_list = [parsed_data]
                        elif isinstance(parsed_data, list):
                            final_list = parsed_data
                        else:
                            final_list = []

                        st.session_state['test_cases'] = final_list
                        
                    else:
                        st.error(f"SERVER ERROR: {response.text}")
                except Exception as e:
                    st.error(f"NETWORK ERROR: {e}")

    # Display Test Cases
    if 'test_cases' in st.session_state and st.session_state['test_cases']:
        tcs = st.session_state['test_cases']
        st.markdown(f"**STRATEGY GENERATED:** `{len(tcs)} TEST SCENARIOS`")
        
        # Raw Data (Expander)
        with st.expander("VIEW RAW JSON DATA"):
            st.json(tcs)

        # DataFrame
        df = pd.DataFrame(tcs)
        if not df.empty:
            df.columns = [c.lower() for c in df.columns]
            desired_cols = ['test_id', 'description', 'expected_result', 'grounded_in']
            final_cols = [c for c in desired_cols if c in df.columns]
            
            if final_cols:
                st.dataframe(df[final_cols], use_container_width=True)
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.warning("EMPTY DATAFRAME GENERATED.")

        st.divider()

        # --- SECTION B: SCRIPT AGENT ---
        st.subheader("B. AUTOMATION AGENT (SELENIUM)")
        
        if not uploaded_html:
            st.error("TARGET HTML MISSING. RETURN TO INGESTION TAB.")
        else:
            # --- DROPDOWN LOGIC ---
            tc_options = {}
            for i, tc in enumerate(tcs):
                tc_lower = {k.lower(): v for k, v in tc.items()} if isinstance(tc, dict) else {}
                
                if isinstance(tc, dict):
                    t_id = tc_lower.get('test_id') or tc_lower.get('id') or tc_lower.get('test_case_id') or f"TC-{i}"
                    desc = tc_lower.get('description') or tc_lower.get('test_scenario') or tc_lower.get('summary') or "No Description"
                    label = f"{t_id}: {str(desc)[:50]}..."
                    tc_options[label] = tc 
                elif isinstance(tc, str):
                    label = f"TC-{i}: {tc[:50]}..."
                    tc_options[label] = {
                        "test_id": f"TC-{i}", 
                        "description": tc, 
                        "expected_result": "See description"
                    }

            selected_label = st.selectbox("SELECT TARGET SCENARIO:", list(tc_options.keys()))
            
            if st.button("GENERATE PAYLOAD (PYTHON SCRIPT)"):
                selected_case = tc_options[selected_label]
                uploaded_html.seek(0) 
                html_content = uploaded_html.getvalue().decode("utf-8")
                
                with st.spinner("WRITING CODE..."):
                    payload = {
                        "test_case_json": json.dumps(selected_case),
                        "html_content": html_content
                    }
                    try:
                        resp = requests.post(f"{BACKEND_URL}/generate-script/", data=payload)
                        if resp.status_code == 200:
                            raw_script = resp.json().get("script", "")
                            clean_script = raw_script.replace("```python", "").replace("```", "").strip()
                            st.session_state['generated_script'] = clean_script
                        else:
                            st.error(f"Error: {resp.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

            # Show Script
            if 'generated_script' in st.session_state:
                st.markdown("#### GENERATED SCRIPT")
                st.code(st.session_state['generated_script'], language='python')
                
                st.download_button(
                    label="DOWNLOAD .PY FILE",
                    data=st.session_state['generated_script'],
                    file_name="test_script.py",
                    mime="text/x-python"
                )