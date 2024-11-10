import tiktoken

def estimate_token_count(text, model="gpt-3.5-turbo"):
    """
    Estimate the number of tokens in a text.
    """
    try:
        encoder = tiktoken.encoding_for_model(model)
        return len(encoder.encode(text))
    except Exception as e:
        print(f"Error estimating tokens: {e}")
        # Fallback: rough estimate based on words
        return len(text.split()) * 1.3 