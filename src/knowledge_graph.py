import json
import logging
from typing import List, Dict, Any
from tqdm import tqdm
from retry import retry
from src.utils import estimate_token_count

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphExtractionError(Exception):
    """Custom exception for graph extraction errors"""
    pass

@retry(GraphExtractionError, tries=3, delay=2)
def extract_knowledge_graph(chunks: List[str], model: Any, max_tokens: int = 2048) -> List[Dict]:
    """
    Generate graph documents from text chunks with retry logic and progress tracking.
    
    Args:
        chunks: List of text chunks to process
        model: Language model instance
        max_tokens: Maximum tokens per chunk
        
    Returns:
        List of graph documents
    """
    graph_documents = []
    
    prompt_template = """
    Analyze the following text and extract a knowledge graph. 
    Return a JSON object with the following structure:
    {
        "nodes": [
            {
                "id": "entity_name",
                "type": "entity_type",
                "properties": {
                    "description": "entity description",
                    "context": "contextual information"
                }
            }
        ],
        "relationships": [
            {
                "source": "source_entity",
                "target": "target_entity",
                "type": "relationship_type",
                "properties": {
                    "context": "relationship context"
                }
            }
        ]
    }
    
    Text: {chunk}
    """
    
    for chunk in tqdm(chunks, desc="Processing text chunks"):
        token_count = estimate_token_count(chunk)
        if token_count > max_tokens:
            logger.warning(f"Chunk exceeded token limit: {token_count} tokens")
            continue

        prompt = prompt_template.format(chunk=chunk)
        try:
            response = model.query(prompt)
            graph_doc = json.loads(response)
            
            # Validate graph document structure
            if not _validate_graph_doc(graph_doc):
                raise GraphExtractionError("Invalid graph document structure")
                
            graph_documents.append(graph_doc)
            logger.info(f"Successfully processed chunk with {len(graph_doc['nodes'])} nodes")
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            raise GraphExtractionError("Failed to parse model response")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise GraphExtractionError(f"Error processing chunk: {str(e)}")
    
    return graph_documents

def _validate_graph_doc(doc: Dict) -> bool:
    """
    Validate the structure of a graph document.
    
    Args:
        doc: Graph document to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_keys = {'nodes', 'relationships'}
    if not all(key in doc for key in required_keys):
        return False
        
    for node in doc.get('nodes', []):
        if not all(key in node for key in ['id', 'type', 'properties']):
            return False
            
    for rel in doc.get('relationships', []):
        if not all(key in rel for key in ['source', 'target', 'type']):
            return False
            
    return True