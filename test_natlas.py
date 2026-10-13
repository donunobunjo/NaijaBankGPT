from datetime import datetime

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)


MODEL_NAME = "NCAIR1/N-ATLaS"


print("=" * 60)
print("N-ATLaS TEST")
print("=" * 60)

print("\nLoading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Tokenizer loaded successfully.")


print("\nLoading N-ATLaS model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto",
)

print("Model loaded successfully.")


def generate_response(
    user_text: str,
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful multilingual Nigerian "
                "language AI assistant."
            ),
        },
        {
            "role": "user",
            "content": user_text,
        },
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False,
        date_string=datetime.now().strftime("%d %b %Y"),
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        add_special_tokens=False,
    )

    # Put inputs on the same device as the model.
    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            use_cache=True,
            repetition_penalty=1.12,
            temperature=0.1,
        )

    generated_tokens = outputs[
        0
    ][inputs["input_ids"].shape[1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    )

    return response.strip()


query = (
    "Rewrite this sentence in clear English: "
    "My ATM card was declined."
)

print("\nUser:")
print(query)

print("\nN-ATLaS response:")
print("-" * 60)

response = generate_response(query)

print(response)

print("-" * 60)
print("\nTest completed.")