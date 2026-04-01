def build_system_prompt():
    return f"""
Answer the question using only the context.

Instructions:
- Use exact words and phrases from the context
- Copy the answer directly from the context whenever possible
- Select the shortest span that fully answers the question
- If multiple contexts are provided, choose the context that contains the most complete answer

Constraints:
- Use only information from the context
- Keep the answer to one sentence

If there is no relevant answer in the contexts, say:
I don't know
"""

def build_user_prompt(contexts, question):
    context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])

    return f"""
Context:
{context_lines}

Question:
{question}
"""

def build_faithfulness_prompt(contexts, output):
    context_lines = "".join([f"- {doc.page_content}\n" for doc in contexts])
    prompt = f"""
You are a strict evaluator.

Determine whether the answer is fully supported by the given context.

Rules:
- Answer YES if the answer is fully supported
- Answer NO if there is any unsupported or incorrect information

Context:
{context_lines}

Answer:
{output}
"""
    return prompt