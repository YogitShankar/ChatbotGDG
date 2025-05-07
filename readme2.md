
## Prerequisites

### Required packages
1. **Python 3.8+**
2. **pip** (Python package installer)
3. **FAISS** (Fast Approximate Nearest Neighbors library)
4. **Transformers**
5. **Torch** (Ensure compatibility with CUDA if using GPU)
6. **TQDM** (for progress bars)
7. **LangChain**
8. **Numpy**

### Hardware Requirements
- A machine with sufficient RAM (at least 8GB).
- GPU with CUDA support (optional but recommended for faster embedding generation).

## Installation Steps


### 1. Create a Virtual Environment

conda create -n venv python=3.12 -y
conda activate venv


### 3. Install Dependencies
Now install the packages mentioned above


## File and Directory Structure
Ensure your files are organized as follows:
```
project/
│
├── data/
│   ├── problems.txt          # Contains problem statements
│   ├── editorials.txt        # Contains editorials
│   └── metadata.json         # Contains problem metadata
│
├── src/
│   ├── chatbotCB.py          # Contains Chatbot class
│   ├── embeddings.py         # Contains Embedder class
│   ├── vectorstore.py        # Contains VectorDatabase class
│   ├── ragretriever.py       # Contains RAGRetriever class
│   └── main.py               # Main script to run the project
│
└── requirements.txt          # Dependencies list
```

## How to Run

### 1. Data Preparation
- Place your dataset files (`problems.txt`, `editorials.txt`, `metadata.json`) inside the `data/` folder.

### 2. Start the Chatbot
To interact with the chatbot:
open the notebook. In it user can input his query