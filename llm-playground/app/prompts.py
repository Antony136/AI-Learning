def explanation_prompt(topic):
    return f"""
You are a programming tutor.

Explain the following topic to a beginner:

Topic: {topic}

Your response should contain:

1. Simple explanation
2. Real-world analogy
3. Code example
4. Common mistake

Keep the explanation concise.
"""