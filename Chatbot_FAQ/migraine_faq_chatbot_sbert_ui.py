import streamlit as st
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

faqs = [
   {"question": "What are the common symptoms of a migraine?",
     "answer": "Common migraine symptoms include throbbing headache, nausea, sensitivity to light or sound, and visual disturbances."},
    {"question": "How long does a migraine usually last?",
     "answer": "A migraine can last anywhere from 4 hours to 72 hours depending on the individual and severity."},
    {"question": "What triggers migraines?",
     "answer": "Triggers may include stress, lack of sleep, certain foods, strong smells, hormonal changes, or weather changes."},
    {"question": "Can migraines be cured?",
     "answer": "There is no permanent cure for migraines, but they can be managed with lifestyle changes and medication."},
    {"question": "When should I see a doctor for migraines?",
     "answer": "You should consult a doctor if you experience frequent, severe, or sudden-onset headaches."},
    {"question": "Are there any home remedies for migraines?",
     "answer": "Yes, home remedies like resting in a dark room, applying cold compresses, staying hydrated, and using essential oils may help."},
    {"question": "What medications are used to treat migraines?",
     "answer": "Medications include pain relievers (like ibuprofen), triptans, anti-nausea drugs, and preventive treatments like beta-blockers or antidepressants."},
    {"question": "Is migraine a sign of something serious?",
     "answer": "Usually not, but if your headache is sudden and severe or includes symptoms like confusion, vision loss, or paralysis, seek emergency care."},
    {"question": "Can migraines affect vision?",
     "answer": "Yes, some migraines cause visual disturbances known as 'aura', including flashing lights or temporary vision loss."},
    {"question": "What lifestyle changes help with migraine prevention?",
     "answer": "Maintaining a regular sleep schedule, avoiding trigger foods, staying hydrated, and managing stress can help prevent migraines."},
    {"question": "Are migraines hereditary?",
     "answer": "Yes, migraines often run in families. If a parent has migraines, there's a higher chance the child may experience them too."},
    {"question": "Is there a specific diet for people with migraines?",
     "answer": "Yes, it's helpful to avoid trigger foods such as chocolate, aged cheese, alcohol, and processed meats. A migraine diary can help identify personal triggers."},
    {"question": "Do hormonal changes affect migraines?",
     "answer": "Yes, hormonal changes—especially in women during menstruation, pregnancy, or menopause—can trigger migraines."},
    {"question": "Can dehydration cause migraines?",
     "answer": "Yes, dehydration is a common trigger for migraines. Drinking enough water daily can help prevent attacks."},
    {"question": "What is a migraine aura?",
     "answer": "A migraine aura is a group of sensory disturbances like visual flashes, tingling, or speech difficulty that typically occur before the headache phase."},
    {"question": "Can migraines be a sign of stroke?",
     "answer": "Although rare, migraines with aura can mimic stroke symptoms. It is important to seek immediate medical attention if symptoms are unusual or sudden."},
    {"question": "Are there different types of migraines?",
     "answer": "Yes. Common types include migraine with aura, migraine without aura, vestibular migraine, and chronic migraine."},
    {"question": "Can children get migraines?",
     "answer": "Yes, children can get migraines. Symptoms may differ slightly from adults and often include abdominal pain or nausea."},
    {"question": "Can too much screen time cause migraines?",
     "answer": "Yes, excessive screen exposure can lead to eye strain, triggering migraines, especially in sensitive individuals."},
    {"question": "Is it safe to exercise during a migraine?",
     "answer": "Light exercise may help prevent migraines, but during an active attack, rest is usually better. Intense activity can worsen symptoms."}
]


faq_questions = [faq["question"] for faq in faqs]
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def get_best_answer(user_question):
    user_embedding = model.encode(user_question, convert_to_tensor=True)
    scores = util.cos_sim(user_embedding, faq_embeddings)
    best_match = scores.argmax()
    return faqs[best_match]["answer"]

st.set_page_config(page_title="🧠 Migraine FAQ Chatbot", layout="centered")

st.markdown("""
    <style>
        body { background-color: #f7f9fc; }
        .main { background-color: #ffffff; padding: 2rem; border-radius: 12px; max-width: 800px; margin: auto;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1); }
        .chat-bubble-user { background-color: #d1e7dd; padding: 12px 18px; border-radius: 15px; margin-bottom: 10px;
                            max-width: 80%; text-align: right; }
        .chat-bubble-bot { background-color: #f8d7da; padding: 12px 18px; border-radius: 15px; margin-bottom: 20px;
                           max-width: 80%; text-align: left; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main'>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>💬 Migraine FAQ Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ask any question related to migraines below:</p>", unsafe_allow_html=True)

user_input = st.text_input("You:", placeholder="e.g., What are the causes of migraines?")
submit = st.button("Send")

if submit and user_input:
    response = get_best_answer(user_input)
    st.markdown(f"""
        <div style='display: flex; justify-content: flex-end;'>
            <div class='chat-bubble-user'>{user_input}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div style='display: flex; justify-content: flex-start;'>
            <div class='chat-bubble-bot'><strong>Bot:</strong> {response}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
