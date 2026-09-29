import streamlit as st
import json
import os
from src.agent import IncidentAgent
from src.memory import HindsightMemoryClient

st.set_page_config(page_title="MindFix - Autonomous Incident Response Agent", page_icon="🛡️", layout="wide")

@st.cache_resource
def load_agent():
    return IncidentAgent()

@st.cache_resource
def load_memory_client():
    return HindsightMemoryClient()

agent = load_agent()
memory_client = load_memory_client()

st.sidebar.title("⚙️ Control Panel")
st.sidebar.info("Powered by **Hindsight** Memory & **Groq** LLM.")

if st.sidebar.button("📥 Seed Demo Incidents"):
    data_path = os.path.join("data", "sample_incidents.json")
    if os.path.exists(data_path):
        with open(data_path, "r") as f:
            incidents = json.load(f)
            count = 0
            for inc in incidents:
                content = f"Incident {inc['incident_id']} on service '{inc['service']}': Error: {inc['error_log']} | Root Cause: {inc['root_cause']} | Resolution: {inc['resolution']}"
                memory_client.add_memory(text_content=content, metadata={"service": inc['service']})
                count += 1
            st.sidebar.success(f"Successfully seeded {count} incidents into Hindsight!")
    else:
        st.sidebar.error("sample_incidents.json not found.")

st.title("🛡️ MindFix: Autonomous Incident Response Agent")
st.markdown("Diagnose production errors instantly using institutional memory powered by **Hindsight**[cite: 1].")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚨 Live Incident Input")
    error_input = st.text_area("Paste error log or stack trace here:", height=180)
    analyze_btn = st.button("Analyze & Resolve", type="primary", use_container_width=True)

with col2:
    st.subheader("🧠 Hindsight Memory Inspector")
    memory_placeholder = st.empty()
    memory_placeholder.info("Recalled context will appear here upon analysis.")

if analyze_btn:
    if not error_input.strip():
        st.warning("Please enter an error log.")
    else:
        with st.spinner("Analyzing and querying Hindsight memory..."):
            past_memories = memory_client.recall_memory(query=error_input, limit=2)
            with col2:
                if past_memories:
                    memory_placeholder.success(f"Recalled {len(past_memories)} past context(s) from Hindsight!")
                    for idx, mem in enumerate(past_memories, 1):
                        st.markdown(f"**Match #{idx}:**")
                        st.code(mem.get("content", "No content"), language="text")
                else:
                    memory_placeholder.warning("No historical matches found in Hindsight memory.")

            response = agent.analyze_incident(error_input)
            st.markdown("---")
            st.subheader("💡 Agent Diagnosis & Remediation Plan")
            st.markdown(response)