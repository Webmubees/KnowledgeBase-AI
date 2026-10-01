from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


MODEL_NAME = "google/flan-t5-small"


tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)


def generate_answer(
    question,
    context
):

    prompt = f"""
You are a knowledge base assistant.

Answer the question using only the information
provided in the context.

If the context does not contain enough information
to answer the question, say:

"I don't have enough information in the knowledge base to answer this question."

Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer.strip()