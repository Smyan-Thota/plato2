# Plato2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j](https://img.shields.io/badge/Neo4j-4.4+-blue)](https://neo4j.com/)

A sophisticated Retrieval-Augmented Generation (RAG) system that processes philosophical texts using OpenHermes 2.5 for local inference and Neo4j for knowledge graph integration.

## 🚀 Features
- **Local Model Inference**: Utilizing OpenHermes 2.5 via Ollama for fast, private inference
- **Knowledge Graph Generation**: Automated extraction of entities and relationships
- **Neo4j Integration**: Efficient storage and querying of knowledge graphs
- **Text Processing**: Advanced chunking with overlap for context preservation
- **Real-time Querying**: Fast response times with local model integration

## 🛠️ Prerequisites
- Python 3.8+
- Neo4j Database
- Ollama with OpenHermes 2.5 model

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/plato2.git
cd plato2
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure Neo4j:
- Update `config/neo4j_config.json` with your Neo4j credentials

5. Add your text:
- Place your philosophical text in `data/meditations.txt`

## 🚀 Usage

Run the main script:
```bash
python src/main.py
```

## 📁 Project Structure
```
plato2/
│
├── src/
│   ├── main.py           # Entry point
│   ├── data_loader.py    # Text loading and chunking
│   ├── knowledge_graph.py # Knowledge graph extraction
│   ├── neo4j_store.py    # Neo4j integration
│   ├── ollama_integration.py # Local model integration
│   └── utils.py          # Utility functions
│
├── data/
│   └── meditations.txt   # Input text file
│
├── config/
│   └── neo4j_config.json # Neo4j configuration
│
└── requirements.txt      # Project dependencies
```

## 🤝 Contributing
Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 