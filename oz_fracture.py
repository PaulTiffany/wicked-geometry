import re
import requests
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from scipy.signal import savgol_filter, find_peaks
from datetime import datetime

def fetch_oz():
    """Fetch The Wonderful Wizard of Oz from Project Gutenberg."""
    print("Fetching text from Project Gutenberg...")
    url = "https://www.gutenberg.org/cache/epub/55/pg55.txt"
    response = requests.get(url)
    text = response.text
    
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if start == -1 or end == -1:
        start = text.find("Chapter I")
        end = len(text)
    
    return text[start:end]

def locate_chapters(text):
    """Find chapter boundaries in the text."""
    chapter_pattern = re.compile(r'Chapter ([IVXLCDM]+)[:\.]?\s*(.+?)(?:\n|$)', re.IGNORECASE)
    
    chapters = {}
    for match in chapter_pattern.finditer(text):
        chapter_num_str = match.group(1)
        chapter_title = match.group(2).strip() if match.group(2) else ""
        
        # Convert Roman to Arabic
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        values = [roman_map.get(c, 0) for c in chapter_num_str.upper()]
        arabic = 0
        for i, val in enumerate(values):
            if i + 1 < len(values) and val < values[i + 1]:
                arabic -= val
            else:
                arabic += val
        
        chapters[arabic] = (match.start(), chapter_title)
    
    return chapters

def get_embeddings(text, window_size=1000, step=200):
    """Create sliding window embeddings of the text."""
    windows = []
    positions = []
    for i in range(0, len(text) - window_size, step):
        chunk = text[i:i+window_size]
        if len(chunk.strip()) > 50:
            windows.append(chunk)
            positions.append(i)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(windows, show_progress_bar=False)
    
    return embeddings, positions, windows

def compute_curvature(embeddings):
    """Estimate extrinsic curvature via cosine distance."""
    curvature = []
    for i in range(1, len(embeddings)):
        k = cosine(embeddings[i-1], embeddings[i])
        curvature.append(k)
    return np.array(curvature)

def detect_peaks(curvature, prominence_factor=2.0):
    """Detect significant curvature peaks."""
    smoothed = savgol_filter(curvature, window_length=min(11, len(curvature)//3*2+1), polyorder=3)
    prominence_threshold = prominence_factor * np.std(smoothed)
    peaks, properties = find_peaks(smoothed, prominence=prominence_threshold)
    
    # Sort by prominence
    sorted_indices = np.argsort(properties['prominences'])[::-1]
    peaks = peaks[sorted_indices]
    properties['prominences'] = properties['prominences'][sorted_indices]
    
    return peaks, properties, smoothed

def extract_context(text, position, context_chars=400):
    """Extract text context around a position."""
    start = max(0, position - context_chars)
    end = min(len(text), position + context_chars)
    snippet = text[start:end]
    
    # Try to start/end at sentence boundaries
    if start > 0:
        first_period = snippet.find('. ')
        if first_period != -1 and first_period < 100:
            snippet = snippet[first_period+2:]
    
    last_period = snippet.rfind('. ')
    if last_period != -1 and last_period > len(snippet) - 100:
        snippet = snippet[:last_period+1]
    
    return snippet.strip()

def find_nearest_chapter(position, chapters):
    """Find which chapter a position falls in."""
    chapter_positions = [(num, pos, title) for num, (pos, title) in chapters.items()]
    chapter_positions.sort(key=lambda x: x[1])
    
    for i, (num, pos, title) in enumerate(chapter_positions):
        if position < pos:
            if i == 0:
                return None
            return chapter_positions[i-1]
        elif i == len(chapter_positions) - 1:
            return (num, pos, title)
    
    return chapter_positions[-1]

def generate_report(peaks, properties, window_positions, windows, text, chapters, 
                   curvature, smoothed, metadata):
    """Generate a formatted analysis report."""
    
    report = []
    
    # Header
    report.append("=" * 90)
    report.append("VALIDATION PROTOCOL V-BAUM")
    report.append("Atlas Fracture Detection in Narrative Embedding Space")
    report.append("=" * 90)
    report.append("")
    
    # Metadata
    report.append("ANALYSIS METADATA")
    report.append("-" * 90)
    report.append(f"Document:           {metadata['document']}")
    report.append(f"Author:             {metadata['author']}")
    report.append(f"Publication:        {metadata['year']}")
    report.append(f"Source:             {metadata['source']}")
    report.append(f"Analysis Date:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Text Length:        {len(text):,} characters")
    report.append(f"Chapters Detected:  {len(chapters)}")
    report.append("")
    
    # Method
    report.append("METHOD")
    report.append("-" * 90)
    report.append(f"Embedding Model:    sentence-transformers/all-MiniLM-L6-v2")
    report.append(f"Window Size:        {metadata['window_size']} characters")
    report.append(f"Step Size:          {metadata['step_size']} characters")
    report.append(f"Total Windows:      {len(windows)}")
    report.append(f"Curvature Metric:   Cosine distance between consecutive embeddings")
    report.append(f"Peak Detection:     Prominence ≥ {metadata['prominence_factor']}σ")
    report.append(f"Peaks Detected:     {len(peaks)}")
    report.append("")
    
    # Summary Statistics
    report.append("CURVATURE STATISTICS")
    report.append("-" * 90)
    report.append(f"Mean Curvature:     {np.mean(curvature):.4f}")
    report.append(f"Std Deviation:      {np.std(curvature):.4f}")
    report.append(f"Maximum:            {np.max(curvature):.4f}")
    report.append(f"Minimum:            {np.min(curvature):.4f}")
    report.append("")
    
    # Peak Rankings
    report.append("=" * 90)
    report.append("DETECTED ATLAS FRACTURES")
    report.append("=" * 90)
    report.append("")
    report.append("Peaks ranked by prominence (semantic discontinuity strength).")
    report.append("Higher prominence indicates stronger atlas fracture.")
    report.append("")
    
    # Top 10 peaks in detail
    for i, (peak_idx, prominence) in enumerate(zip(peaks[:10], properties['prominences'][:10])):
        report.append("─" * 90)
        report.append(f"FRACTURE #{i+1}")
        report.append("─" * 90)
        
        char_pos = window_positions[peak_idx]
        chapter_info = find_nearest_chapter(char_pos, chapters)
        
        report.append(f"Window Index:       {peak_idx}")
        report.append(f"Character Position: {char_pos:,}")
        report.append(f"Prominence:         {prominence:.4f}")
        report.append(f"Curvature ||Ric||:  {smoothed[peak_idx]:.4f}")
        
        if chapter_info:
            num, pos, title = chapter_info
            report.append(f"Location:           Chapter {num}: \"{title}\"")
        
        report.append("")
        report.append("NARRATIVE CONTEXT:")
        report.append("─" * 90)
        
        context = extract_context(text, char_pos, context_chars=400)
        context = re.sub(r'\s+', ' ', context)
        
        # Word wrap at 86 chars
        words = context.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 86:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        
        for line in lines:
            report.append(line)
        
        report.append("─" * 90)
        report.append("")
    
    # Footer
    report.append("=" * 90)
    report.append("END OF REPORT")
    report.append("=" * 90)
    report.append("")
    report.append("INTERPRETATION NOTES:")
    report.append("")
    report.append("Atlas fractures represent moments where the narrative's semantic geometry")
    report.append("undergoes rapid transformation. These correspond to:")
    report.append("  • World-boundary crossings (entering/exiting bounded-observer spaces)")
    report.append("  • Identity transformations (character state transitions)")
    report.append("  • Institutional reconfigurations (authority/metric collapses)")
    report.append("  • Resolution changes (outer projection filter modifications)")
    report.append("")
    report.append("The dominant peak (#1) represents the most significant discontinuity in")
    report.append("the text's embedding space, indicating the primary atlas fracture.")
    report.append("")
    report.append("For methodology details, see:")
    report.append("Tiffany, P. (2025). The Wicked Prior as a Bounded-Observer Manifold:")
    report.append("Atlas Fracture, Stackelberg Parentage, and Grace-Flow Repair.")
    report.append("")
    
    return "\n".join(report)

def save_report(report_text, filename="vbaum_analysis_report.txt"):
    """Save report to file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\n✓ Analysis report saved: {filename}")

def plot_results(curvature, smoothed, peaks, properties, chapters, window_positions, text):
    """Generate visualization."""
    fig, ax = plt.subplots(figsize=(16, 8))
    
    ax.plot(curvature, alpha=0.25, color='gray', linewidth=0.8, label='Raw Curvature')
    ax.plot(smoothed, color='#2E8B57', linewidth=2.5, label='Smoothed Curvature ||Ric||', zorder=3)
    
    # Mark top 10 peaks
    top_n = min(10, len(peaks))
    colors = plt.cm.Reds(np.linspace(0.5, 1.0, top_n))
    
    for i, (peak_idx, prominence) in enumerate(zip(peaks[:top_n], properties['prominences'][:top_n])):
        ax.plot(peak_idx, smoothed[peak_idx], 'o', color=colors[i], 
               markersize=12, zorder=5, markeredgecolor='darkred', markeredgewidth=1.5)
        
        ax.annotate(f'#{i+1}', 
                   xy=(peak_idx, smoothed[peak_idx]),
                   xytext=(0, 15),
                   textcoords='offset points',
                   ha='center',
                   fontsize=9,
                   weight='bold',
                   color='darkred',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[i], alpha=0.7, edgecolor='none'))
    
    # Add chapter markers
    for num, (pos, title) in chapters.items():
        distances = [abs(wpos - pos) for wpos in window_positions]
        nearest_window = np.argmin(distances)
        
        if num in [1, 5, 10, 15, 20]:
            ax.axvline(x=nearest_window, color='lightgray', linestyle=':', 
                      linewidth=1, alpha=0.6, zorder=1)
            ax.text(nearest_window, ax.get_ylim()[1] * 0.95, f'Ch.{num}',
                   rotation=90, va='top', ha='right', fontsize=8, color='gray', alpha=0.7)
    
    ax.set_xlabel('Window Index (Narrative Arc)', fontsize=13, weight='bold')
    ax.set_ylabel('Embedding Curvature ||Ric||', fontsize=13, weight='bold')
    ax.set_title('Narrative Geometry Analysis: Atlas Fracture Detection', 
                fontsize=15, pad=20, weight='bold')
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5)
    
    fig.text(0.5, 0.02, 
            'Peaks represent semantic phase transitions where narrative curvature concentrates.\n' +
            'Higher prominence indicates stronger discontinuity in embedding space.',
            ha='center', fontsize=9, style='italic', color='#444')
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig('atlas_fracture_evidence.png', dpi=300, bbox_inches='tight')
    print("✓ Visualization saved: atlas_fracture_evidence.png")

def main():
    """Run narrative geometry analysis."""
    
    print("\n" + "="*90)
    print("VALIDATION PROTOCOL V-BAUM")
    print("="*90)
    print("\nInitializing analysis...\n")
    
    # Fetch and process
    text = fetch_oz()
    chapters = locate_chapters(text)
    
    print("Generating embeddings (this may take 20-30 seconds)...")
    embeddings, window_positions, windows = get_embeddings(text, window_size=1000, step=200)
    
    print("Computing curvature...")
    curvature = compute_curvature(embeddings)
    
    print("Detecting atlas fractures...")
    peaks, properties, smoothed = detect_peaks(curvature, prominence_factor=2.0)
    
    # Generate outputs
    print("\nGenerating analysis report...")
    
    metadata = {
        'document': 'The Wonderful Wizard of Oz',
        'author': 'L. Frank Baum',
        'year': '1900',
        'source': 'Project Gutenberg (epub/55)',
        'window_size': 1000,
        'step_size': 200,
        'prominence_factor': 2.0
    }
    
    report = generate_report(peaks, properties, window_positions, windows, text, 
                            chapters, curvature, smoothed, metadata)
    
    # Print to terminal
    print("\n" + report)
    
    # Save to file
    save_report(report, "vbaum_analysis_report.txt")
    
    # Generate plot
    print("\nGenerating visualization...")
    plot_results(curvature, smoothed, peaks, properties, chapters, window_positions, text)
    
    print("\n" + "="*90)
    print("✓ ANALYSIS COMPLETE")
    print("="*90)
    print("\nOutputs:")
    print("  • vbaum_analysis_report.txt  (detailed findings)")
    print("  • atlas_fracture_evidence.png (visualization)")
    print("\n")
    
    return {
        'peaks': peaks,
        'properties': properties,
        'curvature': curvature,
        'smoothed': smoothed,
        'report': report
    }

if __name__ == "__main__":
    results = main()
