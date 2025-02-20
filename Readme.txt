Packages Requirements:

install sentence-transformers, python-Docx, numpy, Word2Vec, Qdrant DB, genism, python-docx, numpy, scikit-learn

# command: pip install gensim transformers python-docx numpy scikit-learn
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

Steps to execute:

1) start the DB using the docker desktop. Open powershell in desktop and use the command given below:
# docker run -p 6333:6333 -d qdrant/qdrant

2) Open Vscode, run the Bag_of_words.py to update words dynamically.
# python .\bag_of_words.py

3) Then run the knowledge_graphs using command to get cosine_similarity for specific term in Database.
# python .\knowledge_graphs.py

4) Run the main code file:
# python .\main.py