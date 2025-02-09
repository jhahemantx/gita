from flask import Flask, request, jsonify, render_template
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


groq_api_key = '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'  # Replace with your actual API key
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# Define the prompt to enforce Bhagavad Gita-based responses
prompt = ChatPromptTemplate.from_template(
    """
    You are a divine assistant providing wisdom **strictly based on the Bhagavad Gita**.
    Answer the user's question as **Lord Krishna would, according to the Bhagavad Gita**.

    If the question is unrelated to the Bhagavad Gita, politely refuse to answer.

    **User's Question:** {input}
    """
)

app = Flask(__name__)

# Keywords to determine Bhagavad Gita-related queries
gita_keywords = [
    "gita", "bhagavad gita", "krishna", "arjuna", "karma", "dharma", "yoga", "shloka", "vedas", "mahabharata",
    "stress", "anxiety", "depression", "worry", "fear", "anger", "happiness", "peace", "purpose", "life", "death", 
   
]

def is_gita_related(query):
    return any(keyword in query.lower() for keyword in gita_keywords)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_prompt = data.get('question', '').strip().lower()
    
    if is_gita_related(user_prompt):
        formatted_query = f"Find the answer **strictly according to the Bhagavad Gita**, as Lord Krishna would have said it:\n\n{user_prompt}"
        response = llm.invoke(formatted_query)
        return jsonify({"response": response.content if hasattr(response, "content") else response})
    else:
        return jsonify({"response": "❌ I can only answer questions based on the Bhagavad Gita. Please ask something related to life, struggles, or wisdom from the Gita."})

if __name__ == '__main__':
    app.run(debug=True)
