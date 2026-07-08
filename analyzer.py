from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import re

STOP_WORDS = {
    # French
    'les', 'des', 'est', 'une', 'que', 'qui', 'dans', 'pour', 'sur',
    'avec', 'par', 'pas', 'plus', 'tout', 'mais', 'ont', 'son', 'ses',
    'cette', 'ces', 'aux', 'leur', 'leurs', 'comme', 'aussi', 'bien',
    'peut', 'dont', 'ainsi', 'selon', 'entre', 'tres', 'fait', 'etre',
    'avoir', 'faire', 'dit', 'lors', 'alors', 'donc', 'car', 'soit',
    'nous', 'vous', 'ils', 'elles', 'celui', 'celle', 'ceux', 'celles',
    'quoi', 'quel', 'quelle', 'quels', 'quelles', 'tout', 'tous',
    # English
    'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
    'was', 'one', 'our', 'out', 'has', 'him', 'his', 'how', 'its',
    'may', 'new', 'now', 'see', 'two', 'way', 'who', 'use', 'your',
    'from', 'they', 'will', 'with', 'this', 'that', 'have', 'been',
    'were', 'said', 'each', 'which', 'their', 'what', 'about', 'would',
    'there', 'when', 'make', 'like', 'into', 'than', 'time', 'could',
    'other', 'some', 'these', 'those', 'given', 'using', 'used',
    # Common short words
    'un', 'le', 'la', 'et', 'en', 'du', 'de', 'au', 'se', 'si',
    'on', 'an', 'or', 'to', 'in', 'is', 'it', 'be', 'as', 'at',
    'so', 'we', 'he', 'by', 'do', 'if', 'me', 'my', 'up', 'an',
    # Numbers as words
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    # Additional noise words
    'votre', 'deux', 'comment', 'somme', 'cases', 'taille', 'nombre',
    'valeur', 'suivant', 'suivante', 'chaque', 'autre', 'autres',
    'même', 'meme', 'type', 'types', 'code', 'codes', 'ligne',
    'lignes', 'point', 'points', 'fois', 'après', 'avant', 'sans',
    'sous', 'tres', 'plus', 'moins', 'only', 'each', 'must', 'should',
    'write', 'give', 'show', 'ecrire', 'donner', 'montrer',
}

def is_meaningful(word):
    """Check if a word is meaningful (not a stop word, not too short, not a number)."""
    word = word.lower().strip()
    if len(word) <= 3:
        return False
    if word in STOP_WORDS:
        return False
    if word.isdigit():
        return False
    if re.match(r'^\d+[\.\,]?\d*$', word):
        return False
    return True

def extract_topics(questions, n_topics=8):
    """Extract main topics from questions using TF-IDF."""
    if len(questions) < 2:
        return ["Not enough questions to analyze"]
    
    vectorizer = TfidfVectorizer(
        max_features=200,
        stop_words=list(STOP_WORDS),
        ngram_range=(1, 2),
        min_df=1
    )
    
    try:
        tfidf_matrix = vectorizer.fit_transform(questions)
        feature_names = vectorizer.get_feature_names_out()
        
        topics = []
        for i in range(tfidf_matrix.shape[0]):
            row = tfidf_matrix.getrow(i).toarray()[0]
            top_indices = row.argsort()[-5:][::-1]
            top_words = [feature_names[idx] for idx in top_indices if row[idx] > 0]
            topics.extend(top_words)
        
        # Filter and count
        meaningful_topics = [t for t in topics if all(is_meaningful(w) for w in t.split())]
        topic_counts = Counter(meaningful_topics)
        top_topics = [topic for topic, count in topic_counts.most_common(n_topics)]
        
        return top_topics if top_topics else ["General concepts"]
    
    except Exception:
        return ["Could not extract topics"]

def classify_difficulty(question):
    """Classify question difficulty."""
    question_lower = question.lower()
    
    hard_keywords = [
        'prove', 'derive', 'demonstrate', 'analyze', 'evaluate',
        'compare', 'design', 'implement', 'optimize', 'complex',
        'justify', 'critique', 'synthesize', 'montrer', 'démontrer',
        'prouver', 'analyser', 'comparer', 'concevoir', 'implémenter',
        'expliquer pourquoi', 'justifier', 'déduire', 'établir'
    ]
    
    medium_keywords = [
        'calculate', 'compute', 'solve', 'find', 'determine',
        'describe', 'explain', 'apply', 'show', 'calculer',
        'résoudre', 'trouver', 'déterminer', 'décrire', 'expliquer',
        'appliquer', 'représenter', 'construire', 'écrire'
    ]
    
    easy_keywords = [
        'define', 'list', 'name', 'state', 'identify', 'what is',
        'give an example', 'true or false', 'définir', 'lister',
        'nommer', 'citer', 'donner', 'qu\'est', 'vrai ou faux'
    ]
    
    hard_score = sum(1 for kw in hard_keywords if kw in question_lower)
    medium_score = sum(1 for kw in medium_keywords if kw in question_lower)
    easy_score = sum(1 for kw in easy_keywords if kw in question_lower)
    
    word_count = len(question.split())
    if word_count > 50:
        hard_score += 1
    elif word_count > 25:
        medium_score += 1

    if hard_score > 0:
        return "Hard"
    elif medium_score > 0:
        return "Medium"
    else:
        return "Easy"

def analyze_exam(questions):
    """Full analysis of extracted questions."""
    if not questions:
        return {
            "total_questions": 0,
            "topics": [],
            "difficulty_distribution": {},
            "difficulty_per_question": []
        }
    
    difficulties = [classify_difficulty(q) for q in questions]
    difficulty_counts = Counter(difficulties)
    topics = extract_topics(questions)
    
    return {
        "total_questions": len(questions),
        "topics": topics,
        "difficulty_distribution": dict(difficulty_counts),
        "difficulty_per_question": difficulties
    }

def clean_topics_with_ai(raw_topics, subject):
    """Use Mistral to filter and clean extracted topics."""
    import os
    from mistralai import Mistral
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        import streamlit as st
        api_key = st.secrets["MISTRAL_API_KEY"]
    except:
        api_key = os.getenv("MISTRAL_API_KEY")
    client = Mistral(api_key=api_key)
    
    
    topics_str = ", ".join(raw_topics)
    
    prompt = f"""You are an academic expert. I extracted these words/phrases from {subject} exam papers:

{topics_str}

Your job: return ONLY the real academic topics from this list. Remove:
- Verbs and instructions (vérifier, representer, executer, montrer, donner)
- Generic words (pages, argument, cases, taille, nombre)
- Stop words or noise

Return ONLY a comma-separated list of real academic topics. Nothing else. No explanation.
Example output: systeme exploitation, memoire physique, allocation memoire, processus, table multipli"""

    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    
    cleaned = response.choices[0].message.content.strip()
    topics = [t.strip() for t in cleaned.split(',') if t.strip()]
    return topics