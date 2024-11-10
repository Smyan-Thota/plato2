import re

def load_and_split_text(file_path, chunk_size=500, chunk_overlap=50):
    """
    Load text from a file and split it into smaller chunks.
    """
    with open(file_path, "r", encoding='utf-8') as file:
        text = file.read()
    
    # Split text into sentences
    sentences = re.split(r"(?<=[.!?]) +", text)
    
    # Chunk the sentences
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(" ".join(current_chunk))
            # Add overlap by keeping last few sentences
            overlap_sentences = current_chunk[-int(chunk_overlap/10):]
            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s.split()) for s in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks 