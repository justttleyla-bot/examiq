import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def generate_practice_questions(topics, subject, difficulty, num_questions, sample_questions):
    """Generate practice questions using Mistral AI."""
    
    samples = "\n".join(sample_questions[:3]) if sample_questions else "No samples available"
    topics_str = ", ".join(topics)
    
    prompt = f"""You are an expert professor creating exam questions.

Subject: {subject}
Main topics identified: {topics_str}
Difficulty level requested: {difficulty}
Number of questions to generate: {num_questions}

Here are sample questions from past exams to match the style:
{samples}

Generate exactly {num_questions} practice questions that:
1. Match the style and format of the sample questions above
2. Cover the identified topics
3. Are at {difficulty} difficulty level
4. Are clear and unambiguous
5. Include a mix of question types (theoretical, practical, problem-solving)


Format as a tight numbered list. No blank lines between questions. After all questions, add **Answers:** with one-line guidelines per question. Be concise.
    
Generate the questions now:"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def predict_likely_topics(all_topics, subject, exam_texts):
    """Predict which topics are most likely to appear on the next exam."""
    
    topics_str = ", ".join(all_topics)
    combined_text = " ".join(exam_texts)[:2000]
    
    prompt = f"""You are an expert academic advisor analyzing past exam patterns.

Subject: {subject}
Topics found across past exams: {topics_str}

Sample content from past exams:
{combined_text}

Based on these past exams, predict:
1. The TOP 5 topics most likely to appear on the next exam (ranked by likelihood)
2. For each topic, explain WHY it is likely to appear (frequency, importance, pattern)
3. Which topics seem underrepresented and might appear soon

Be specific and concise. No empty lines between items. Format as:

**Predicted Topics:**
1. **[Topic]** — [One sentence reason]
2. **[Topic]** — [One sentence reason]
3. **[Topic]** — [One sentence reason]
4. **[Topic]** — [One sentence reason]
5. **[Topic]** — [One sentence reason]

**Underrepresented Topics:**
- **[Topic]** — [One sentence]"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content