from tiktoken import encoding_for_model

def count_tokens(text: str, model: str = "gpt-4"):
    tokenizer = encoding_for_model(model)
    return len(tokenizer.encode(text))
    