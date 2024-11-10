from langchain_community.graphs.neo4j_graph import Neo4jGraph
import json
import logging
from typing import List, Dict
from neo4j import GraphDatabase, Driver
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Neo4jConnection:
    def __init__(self, config_path: str):
        with open(config_path, "r") as file:
            self.config = json.load(file)
        self._driver = None

    @property
    def driver(self) -> Driver:
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.config["url"],
                auth=(self.config["username"], self.config["password"])
            )
        return self._driver

    @contextmanager
    def get_session(self):
        session = self.driver.session()
        try:
            yield session
        finally:
            session.close()

def store_in_neo4j(graph_documents: List[Dict], config_path: str):
    """
    Store graph documents in Neo4j with enhanced error handling and validation.
    
    Args:
        graph_documents: List of graph documents to store
        config_path: Path to Neo4j configuration file
    """
    connection = Neo4jConnection(config_path)
    
    try:
        # Initialize schema
        setup_neo4j_schema(connection)
        
        # Store documents
        for doc in graph_documents:
            store_document(connection, doc)
            
        logger.info(f"Successfully stored {len(graph_documents)} documents")
        
    except Exception as e:
        logger.error(f"Failed to store documents: {str(e)}")
        raise
    finally:
        if connection._driver:
            connection._driver.close()

def setup_neo4j_schema(connection: Neo4jConnection):
    """Set up Neo4j schema with constraints and indexes."""
    queries = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE",
        "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.type)",
        "CREATE INDEX IF NOT EXISTS FOR ()-[r:RELATES_TO]-() ON (r.type)"
    ]
    
    with connection.get_session() as session:
        for query in queries:
            try:
                session.run(query)
                logger.info(f"Successfully executed schema query: {query}")
            except Exception as e:
                logger.error(f"Schema setup error: {str(e)}")
                raise

def store_document(connection: Neo4jConnection, doc: Dict):
    """Store a single graph document in Neo4j."""
    node_query = """
    MERGE (n:Entity {id: $id})
    SET n.type = $type,
        n.properties = $properties
    """
    
    relationship_query = """
    MATCH (source:Entity {id: $source})
    MATCH (target:Entity {id: $target})
    MERGE (source)-[r:RELATES_TO {type: $type}]->(target)
    SET r.properties = $properties
    """
    
    with connection.get_session() as session:
        # Store nodes
        for node in doc['nodes']:
            session.run(node_query, 
                       id=node['id'],
                       type=node['type'],
                       properties=node['properties'])
        
        # Store relationships
        for rel in doc['relationships']:
            session.run(relationship_query,
                       source=rel['source'],
                       target=rel['target'],
                       type=rel['type'],
                       properties=rel.get('properties', {}))