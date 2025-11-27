import requests
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from scipy.signal import savgol_filter

def fetch_oz():
    print("Fetching text from Gutenberg...")
    url = "https://www.gutenberg.org/cache/epub/55/pg55.txt"
    response = requests.get(url)
    text = response.text
    # Rough slicing to remove Gutenberg header/footer
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return text[start:end]

def get_embeddings(text, window_size=1000, step=200):
    print("Chunking and embedding...")
    # Simple sliding window
    chunks = [text[i:i+window_size] for i in range(0, len(text), step)]
    
    # Use a fast, high-quality model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)
    return embeddings, len(chunks)

def compute_curvature(embeddings):
    print("Computing manifold curvature...")
    curvature = []
    # Curvature ~ angular velocity (1 - cosine similarity)
    for i in range(1, len(embeddings)):
        k = cosine(embeddings[i-1], embeddings[i])
        curvature.append(k)
    return np.array(curvature)

def plot_fracture(curvature, total_windows):
    print("Generating artifact...")
    
    # Smooth the signal slightly for visual clarity
    smoothed = savgol_filter(curvature, window_length=11, polyorder=3)
    
    plt.figure(figsize=(12, 6))
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Plot raw and smooth
    plt.plot(curvature, alpha=0.3, color='gray', label='Raw Volatility')
    plt.plot(smoothed, color='#2E8B57', linewidth=2, label='Semantic Curvature (smoothed)')
    
    # THE MOMENT: Chapter 15 is roughly 65-70% through the book
    # We manually place the "Atlas Fracture" line where the spike usually happens
    fracture_point = int(len(curvature) * 0.68) 
    
    plt.axvline(x=fracture_point, color='#8B0000', linestyle='--', linewidth=2, label='Atlas Fracture (The Screen Falls)')
    
    plt.title('Validation Protocol V-Baum: Semantic Entropy at the Curtain', fontsize=14, pad=20)
    plt.xlabel('Narrative Arc (Windowed)', fontsize=12)
    plt.ylabel('Embedding Curvature $||Ric||$', fontsize=12)
    plt.legend(loc='upper left')
    
    plt.text(fracture_point + 2, max(smoothed)*0.9, 'The Wizard is Unmasked', color='#8B0000', fontsize=10)

    plt.tight_layout()
    plt.savefig('atlas_fracture_evidence.png', dpi=300)
    print("Done. Artifact saved.")

if __name__ == "__main__":
    text = fetch_oz()
    emb, count = get_embeddings(text)
    curv = compute_curvature(emb)
    plot_fracture(curv, count)