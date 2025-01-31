import tiktoken

def count_tokens(text, model_name="gpt-4o"):
    """
    Count the number of tokens in a string using the specified OpenAI model's tokenizer.
    
    :param text: The input string to tokenize.
    :param model_name: The name of the OpenAI model (e.g., "gpt-4", "gpt-3.5-turbo").
    :return: The number of tokens in the string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    
    tokens = encoding.encode(text)
    return len(tokens)

input_string = input("Enter a string to count tokens: ")
token_count = count_tokens(input_string)
print(f"The string contains {token_count} tokens.")