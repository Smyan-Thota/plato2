import os
from src.data_loader import load_and_split_text
from src.knowledge_graph import extract_knowledge_graph
from src.neo4j_store import store_in_neo4j
from src.ollama_integration import initialize_ollama_model, query_local_model

def main():
    # Paths and Configurations
    file_path = "data/meditations.txt"
    neo4j_config_path = "config/neo4j_config.json"
    
    # Initialize Ollama Model
    model = initialize_ollama_model("openhermes")

    # Load and Split Data
    print("Loading and splitting text...")
    texts = load_and_split_text(file_path)

    # Extract Knowledge Graph
    print("Extracting knowledge graph...")
    graph_documents = extract_knowledge_graph(texts, model)

    # Store in Neo4j
    print("Storing knowledge graph in Neo4j...")
    store_in_neo4j(graph_documents, neo4j_config_path)

    # Query Example
    print("Querying the local model...")
    response = query_local_model("What does Marcus Aurelius say about virtue?")
    print(f"Model Response: {response}")

if __name__ == "__main__":
    main() 