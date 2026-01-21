import streamlit as st
import google.generativeai as genai
from story_data import STORY_NODES

# 1. Setup AI (Using Secrets for Security)
# We will set the 'GEMINI_API_KEY' in the Streamlit Cloud dashboard later
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

def evaluate_move(player_input, goal_intent):
    """Asks Gemini to score the player's intent."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a logic gate for a story game. 
    Goal: {goal_intent}
    Player Input: "{player_input}"
    Does the player's input match the goal? 
    Answer ONLY with a decimal number between 0.0 and 1.0.
    """
    try:
        response = model.generate_content(prompt)
        return float(response.text.strip())
    except:
        return 0.0

# 2. Page Configuration
st.set_page_config(page_title="Strategic Storyteller", page_icon="🛡️")

# 3. Initialize Game State
if "current_node" not in st.session_state:
    st.session_state.current_node = "start"

node = STORY_NODES[st.session_state.current_node]

# 4. UI Display
st.title("🛡️ Strategic Storyteller")
st.markdown("---")
st.write(node["text"])

# 5. Game Logic
if not node.get("is_end"):
    player_input = st.text_input("Enter your plan:", placeholder="Type what you would do...")
    
    if st.button("Submit Plan"):
        if player_input:
            with st.spinner("AI is evaluating your strategy..."):
                score = evaluate_move(player_input, node["target_intent"])
                
                # Decision Threshold
                if score >= 0.7:
                    st.success(f"Strategic Match: {int(score*100)}% - Success!")
                    st.session_state.current_node = node["success_node"]
                else:
                    st.error(f"Strategic Match: {int(score*100)}% - Failure.")
                    st.session_state.current_node = node["failure_node"]
                
                st.rerun()
        else:
            st.warning("Please type something before submitting.")
else:
    st.info("The story has ended.")
    if st.button("Restart Journey"):
        st.session_state.current_node = "start"
        st.rerun()
