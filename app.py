import streamlit as st
import google.generativeai as genai
from story_data import STORY_NODES

# 1. Setup AI
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key missing in Secrets!")

def evaluate_move(player_input, goal_intent):
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Improved prompt for more consistent scoring
    prompt = f"""
    The story goal is: {goal_intent}.
    The player says: "{player_input}".
    Rate how well this plan achieves the goal. 
    Return ONLY a number between 0.0 and 1.0. 
    (Example: 0.9 for great, 0.2 for bad).
    """
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it's just a number
        score_text = response.text.strip().split()[0] 
        return float(score_text)
    except:
        return 0.0

# 2. Initialize Game State (Locking the node)
if "current_node" not in st.session_state:
    st.session_state.current_node = "start"

node = STORY_NODES[st.session_state.current_node]

# 3. UI Display
st.title("🛡️ Strategic Storyteller")
st.write(node["text"])

# 4. Game Logic
if not node.get("is_end"):
    # Use a form to prevent the app from refreshing too early
    with st.form(key='player_form'):
        player_input = st.text_input("Enter your plan:")
        submit_button = st.form_submit_button(label='Submit Plan')

        if submit_button and player_input:
            with st.spinner("Evaluating..."):
                score = evaluate_move(player_input, node["target_intent"])
                
                # Logic to switch nodes
                if score >= 0.5: # Lowered threshold slightly for testing
                    st.session_state.current_node = node["success_node"]
                else:
                    st.session_state.current_node = node["failure_node"]
                
                # Force a refresh to the NEW node
                st.rerun()
elif node.get("is_end"):
    st.markdown("---")
    st.success("The End.")
    if st.button("Restart Journey"):
        st.session_state.current_node = "start"
        st.rerun()
