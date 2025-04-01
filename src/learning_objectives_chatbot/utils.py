"""Utility functions for the Learning Objectives Chatbot."""

from typing import Dict, List, Any, Optional
import re
import pandas as pd


def generate_response(user_input: str, message_history: List[Dict[str, str]]) -> str:
    """Generate chatbot response based on user input and conversation history.
    
    This function simulates a conversational flow to guide users through
    creating effective learning objectives.
    
    Args:
        user_input: The latest user message
        message_history: List of previous messages in the conversation
        
    Returns:
        String response from the assistant
    """
    # Extract just the content from message history for easier processing
    history_content = [msg["content"] for msg in message_history]
    
    # Check what stage of the conversation we're in
    if len(message_history) <= 2:
        # Initial subject/topic identification
        return (
            f"Thanks for sharing about {user_input}! Learning objectives should focus on what "
            f"students will be able to do after the learning experience. "
            f"What level of learning are you targeting? For example:\n"
            f"- Remember/recall information\n"
            f"- Understand/explain concepts\n"
            f"- Apply knowledge to new situations\n"
            f"- Analyze information\n"
            f"- Evaluate ideas\n"
            f"- Create new content or perspectives"
        )
    
    elif len(message_history) <= 4:
        # Learning level identification
        return (
            f"Great! Now let's think about how you'll measure success. "
            f"What specific, observable actions will show that students have achieved this objective? "
            f"For example, will they be able to define, explain, solve, compare, design, etc.?"
        )
    
    elif len(message_history) <= 6:
        # Measurement/verb identification
        subject = message_history[1]["content"]  # The subject from first user reply
        level = message_history[3]["content"]    # The learning level from second user reply
        measurement = user_input                # The measurement from third user reply
        
        # Extract a good action verb based on their input
        verb = extract_action_verb(measurement, get_blooms_level(level))
        
        return (
            f"Excellent! Based on our conversation, let me suggest a learning objective framework:\n\n"
            f"'After completing this [learning experience], students will be able to {verb} [specific content] "
            f"[optional: condition] [optional: criteria].'\n\n"
            f"Would you like to fill in this template for your {subject} objective? Or I can suggest one for you."
        )
    
    elif "suggest" in user_input.lower():
        # User wants a suggestion
        subject = message_history[1]["content"]  # Subject from first user reply
        level = message_history[3]["content"]    # Learning level from second reply
        measurement = message_history[5]["content"]  # Measurement from third reply
        
        # Generate a suggested learning objective
        suggested_objective = generate_sample_objective(subject, level, measurement)
        
        return (
            f"Here's a possible learning objective:\n\n{suggested_objective}\n\n"
            f"What do you think? Would you like to refine this further, or would you prefer "
            f"to create another objective for a different aspect of {subject}?"
        )
    
    elif any(word in user_input.lower() for word in ["refine", "improve", "better", "change"]):
        # User wants to refine the objective
        return (
            f"Let's refine this objective. Is there anything specific you'd like to change? For example:\n"
            f"- Make it more specific\n"
            f"- Change the level of thinking\n"
            f"- Adjust how it will be measured\n"
            f"- Add conditions or criteria for success"
        )
    
    elif "another" in user_input.lower() or "different" in user_input.lower():
        # User wants a new objective
        subject = message_history[1]["content"]  # Subject from first user reply
        
        return (
            f"Let's create another learning objective for {subject}. "
            f"What specific skill or knowledge component would you like to address with this new objective?"
        )
    
    else:
        # Default response for continuing the conversation
        return (
            f"Thanks for sharing that. To create the most effective learning objective, "
            f"we should make sure it's SMART (Specific, Measurable, Achievable, Relevant, Time-bound). "
            f"Would you like to refine the current objective, or should we create another one?"
        )


def get_sample_objectives() -> Dict[str, List[str]]:
    """Return sample learning objectives by category.
    
    Returns:
        Dictionary of sample objectives organized by category
    """
    return {
        "Knowledge/Remember": [
            "Define the key terms related to photosynthesis.",
            "List the main components of a computer system.",
            "Identify the major periods of art history."
        ],
        "Comprehension/Understand": [
            "Explain the process of cellular respiration.",
            "Summarize the plot of Shakespeare's Hamlet.",
            "Describe the functions of the three branches of government."
        ],
        "Application/Apply": [
            "Calculate the area of irregular shapes using calculus.",
            "Implement a sorting algorithm in Python.",
            "Apply the principles of color theory in a digital composition."
        ],
        "Analysis/Analyze": [
            "Compare and contrast classical and operant conditioning.",
            "Analyze the causes and effects of climate change.",
            "Differentiate between leadership and management strategies."
        ],
        "Evaluation/Evaluate": [
            "Critique a peer's research paper using established criteria.",
            "Evaluate the effectiveness of public health campaigns.",
            "Assess the validity of historical sources."
        ],
        "Creation/Create": [
            "Design an experiment to test the effect of light on plant growth.",
            "Develop a marketing strategy for a new product.",
            "Compose a musical piece that incorporates at least three different scales."
        ]
    }


def analyze_objective(objective: str) -> Dict[str, Any]:
    """Analyze a learning objective for quality and effectiveness.
    
    Args:
        objective: The learning objective to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    # Default analysis structure
    analysis = {
        "blooms_level": "Unknown",
        "measurable": False,
        "clarity_score": 0,
        "suggestions": []
    }
    
    # Check for action verbs to determine Bloom's level
    for level, verbs in BLOOMS_TAXONOMY_VERBS.items():
        for verb in verbs:
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, objective.lower()):
                analysis["blooms_level"] = level
                break
    
    # Check if it's measurable (contains a specific action verb)
    all_verbs = [verb for verbs in BLOOMS_TAXONOMY_VERBS.values() for verb in verbs]
    if any(re.search(r'\b' + re.escape(verb) + r'\b', objective.lower()) for verb in all_verbs):
        analysis["measurable"] = True
    
    # Calculate clarity score (simplified version)
    clarity = 5  # Start with a middle score
    
    # Add points for positive attributes
    if analysis["measurable"]:
        clarity += 2
    if len(objective.split()) >= 10:  # Reasonable length
        clarity += 1
    if "will be able to" in objective.lower():
        clarity += 1
    if any(condition in objective.lower() for condition in ["using", "through", "by", "with"]):
        clarity += 1
    
    # Subtract points for negative attributes
    if len(objective.split()) > 30:  # Too wordy
        clarity -= 1
    if objective.count(",") > 2:  # Too complex
        clarity -= 1
    
    # Cap the clarity score between 1-10
    analysis["clarity_score"] = max(1, min(10, clarity))
    
    return analysis


def suggest_improvements(analysis: Dict[str, Any]) -> List[str]:
    """Generate suggestions for improving a learning objective based on analysis.
    
    Args:
        analysis: Dictionary containing analysis results
        
    Returns:
        List of improvement suggestions
    """
    suggestions = []
    
    if not analysis["measurable"]:
        suggestions.append(
            "Use a specific, measurable action verb from Bloom's Taxonomy that matches your desired learning level."
        )
    
    if analysis["clarity_score"] < 6:
        suggestions.append(
            "Improve clarity by being more specific about what students will be able to do."
        )
        
    if analysis["blooms_level"] == "Unknown":
        suggestions.append(
            "Include a clear action verb that aligns with the intended learning level."
        )
    
    if analysis["clarity_score"] < 8 and "Remember" in analysis["blooms_level"]:
        suggestions.append(
            "Consider using higher-order thinking skills beyond recall if appropriate for your learning context."
        )
    
    return suggestions


def generate_sample_objective(subject: str, level: str, measurement: str) -> str:
    """Generate a sample learning objective based on user inputs.
    
    Args:
        subject: The subject area
        level: The learning level
        measurement: How learning will be measured
        
    Returns:
        A sample learning objective
    """
    # Clean and extract key information
    subject = subject.strip().lower()
    level = level.strip().lower()
    
    # Determine Bloom's level and appropriate verb
    blooms_level = get_blooms_level(level)
    verb = extract_action_verb(measurement, blooms_level)
    
    # Generate contextual content based on subject
    if "math" in subject or "statistic" in subject:
        content = f"{verb} complex problems using appropriate formulas and techniques"
    elif "literature" in subject or "english" in subject:
        content = f"{verb} texts to identify themes and literary devices"
    elif "science" in subject:
        content = f"{verb} scientific principles to explain natural phenomena"
    elif "history" in subject:
        content = f"{verb} historical events and their impact on modern society"
    elif "art" in subject:
        content = f"{verb} artistic techniques and principles in original compositions"
    elif "programming" in subject or "coding" in subject or "computer" in subject:
        content = f"{verb} algorithms to solve computational problems efficiently"
    else:
        content = f"{verb} key concepts and principles related to {subject}"
    
    # Construct the full objective
    objective = f"After completing this course, students will be able to {content}."
    
    return objective


def extract_action_verb(text: str, blooms_level: str) -> str:
    """Extract an appropriate action verb from text or suggest one based on Bloom's level.
    
    Args:
        text: Text to extract verb from
        blooms_level: Bloom's taxonomy level
        
    Returns:
        An appropriate action verb
    """
    # Try to extract a verb from the user's text
    for verb in BLOOMS_TAXONOMY_VERBS.get(blooms_level, []):
        if verb in text.lower():
            return verb
    
    # If no matching verb found, return a default one for the appropriate level
    default_verbs = {
        "Remember": "identify",
        "Understand": "explain",
        "Apply": "apply",
        "Analyze": "analyze",
        "Evaluate": "evaluate",
        "Create": "create"
    }
    
    return default_verbs.get(blooms_level, "demonstrate")


def get_blooms_level(text: str) -> str:
    """Determine the Bloom's taxonomy level from text description.
    
    Args:
        text: Text describing a learning level
        
    Returns:
        Corresponding Bloom's taxonomy level
    """
    text = text.lower()
    
    if any(word in text for word in ["remember", "recall", "memorize", "identify", "list"]):
        return "Remember"
    elif any(word in text for word in ["understand", "explain", "describe", "summarize"]):
        return "Understand"
    elif any(word in text for word in ["apply", "use", "implement", "solve"]):
        return "Apply"
    elif any(word in text for word in ["analyze", "compare", "contrast", "examine"]):
        return "Analyze"
    elif any(word in text for word in ["evaluate", "assess", "judge", "critique"]):
        return "Evaluate"
    elif any(word in text for word in ["create", "design", "develop", "compose"]):
        return "Create"
    else:
        # Default to middle level if unclear
        return "Apply"


# Bloom's Taxonomy Verbs
BLOOMS_TAXONOMY_VERBS = {
    "Remember": [
        "define", "describe", "identify", "label", "list", "match", "name", "outline",
        "recall", "recognize", "reproduce", "select", "state"
    ],
    "Understand": [
        "classify", "compare", "contrast", "demonstrate", "discuss", "explain",
        "extend", "illustrate", "infer", "interpret", "paraphrase", "predict",
        "summarize", "translate"
    ],
    "Apply": [
        "apply", "change", "compute", "construct", "demonstrate", "discover",
        "manipulate", "modify", "operate", "predict", "prepare", "produce",
        "relate", "show", "solve", "use"
    ],
    "Analyze": [
        "analyze", "break down", "categorize", "compare", "contrast", "differentiate",
        "discriminate", "distinguish", "examine", "experiment", "identify", "illustrate",
        "infer", "outline", "relate", "select", "separate"
    ],
    "Evaluate": [
        "appraise", "argue", "assess", "choose", "compare", "conclude", "contrast",
        "criticize", "critique", "defend", "evaluate", "judge", "justify",
        "prioritize", "rate", "select", "support", "value"
    ],
    "Create": [
        "assemble", "compose", "construct", "create", "design", "develop", "devise",
        "formulate", "generate", "hypothesize", "invent", "make", "organize",
        "plan", "produce", "write"
    ]
}