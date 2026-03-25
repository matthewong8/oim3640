def read_file(filename):
    """Read and return the contents of a file."""
    import os
    
    # Try to open the file from the current directory first
    try:
        fin = open(filename)
        text = fin.read()
        fin.close()
        return text
    except FileNotFoundError:
        # If not found, try looking in the Projects folder
        projects_path = os.path.join(os.path.dirname(__file__), filename)
        try:
            fin = open(projects_path)
            text = fin.read()
            fin.close()
            return text
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            print(f"Make sure the file is in the Projects folder or provide the full path.")
            return None


def clean_text(text):
    """Convert text to lowercase and remove basic punctuation."""
    text = text.lower()

    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.replace("!", "")
    text = text.replace("?", "")
    text = text.replace(";", "")
    text = text.replace(":", "")
    text = text.replace('"', "")
    text = text.replace("(", "")
    text = text.replace(")", "")
    text = text.replace("-", "")
    text = text.replace("_", "")
    text = text.replace("/", "")

    return text


def count_words(words, stop_words=None):
    """Count word frequencies using a dictionary, optionally filtering stop words."""
    counts = {}

    for word in words:
        # Skip stop words if provided
        if stop_words and word in stop_words:
            continue
            
        if word in counts:
            counts[word] = counts[word] + 1
        else:
            counts[word] = 1

    return counts


def get_top_words(counts, top_n):
    """Return a list of the top N words and their counts."""
    items = list(counts.items())
    top_words = []

    while len(top_words) < top_n and len(items) > 0:
        biggest = items[0]

        for item in items:
            if item[1] > biggest[1]:
                biggest = item

        top_words.append(biggest)
        items.remove(biggest)

    return top_words


def analyze_vocabulary(words, counts):
    """Analyze vocabulary difficulty and complexity."""
    if not words:
        return None
    
    # Calculate average word length
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / len(words)
    
    # Find advanced words (longer than 8 characters)
    advanced_words = {}
    for word, count in counts.items():
        if len(word) > 8:
            advanced_words[word] = count
    
    # Sort advanced words by frequency
    advanced_words = dict(sorted(advanced_words.items(), key=lambda x: x[1], reverse=True))
    
    # Simple complexity score (0-100 scale based on average word length)
    # Typical range: 3-6 chars average for simple text, 5-7 for moderate, 7+ for complex
    complexity_score = min(100, int((avg_word_length / 10) * 100))
    
    return {
        'avg_length': round(avg_word_length, 2),
        'complexity_score': complexity_score,
        'advanced_words': advanced_words
    }


def identify_themes(top_words, counts):
    """Identify themes based on all words in the essay."""
    # Define themes and related keywords
    themes = {
        'Learning & Education': ['learn', 'education', 'student', 'class', 'school', 'study', 'knowledge', 'teach', 'course', 'academic', 'learning', 'taught', 'teacher', 'classes', 'students'],
        'Personal Growth': ['growth', 'develop', 'improve', 'challenge', 'experience', 'change', 'journey', 'progress', 'skill', 'developed', 'growing', 'development', 'improved', 'skills'],
        'Writing & Expression': ['write', 'writing', 'express', 'communication', 'language', 'story', 'voice', 'essay', 'paper', 'written', 'writer', 'expression', 'stories', 'papers'],
        'Reflection & Thought': ['think', 'thought', 'reflect', 'realize', 'understand', 'discover', 'perspective', 'insight', 'thinking', 'reflection', 'realized', 'understanding', 'discovered'],
        'Social & Relationships': ['community', 'people', 'friends', 'society', 'relationship', 'team', 'group', 'together', 'social', 'connection', 'friend', 'communities', 'groups']
    }
    
    theme_counts = {}
    
    # Count words that match each theme from all word counts
    for word, count in counts.items():
        for theme, keywords in themes.items():
            if word in keywords:
                if theme not in theme_counts:
                    theme_counts[theme] = 0
                theme_counts[theme] += count
    
    return theme_counts


def main():
    print("My College Essay Analyzer - Milestone 1")
    print()

    filename = input("Enter the name of your text file: ")

    text = read_file(filename)
    if text is None:
        return
    
    cleaned_text = clean_text(text)
    words = cleaned_text.split()

    # Comprehensive stop words list - common English words
    stop_words = {
        'the', 'and', 'of', 'to', 'that', 'i', 'in', 'a', 'this', 'is', 'it', 'for', 'with', 'be', 'or', 'as', 'by', 'at', 'from', 'on', 'are', 'was', 'have', 'has', 'had', 
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might',
        'my', 'their', 'they', 'when', 'but', 'he', 'she', 'we', 'you', 'your', 'which', 'what', 'how', 'who', 'where', 'why',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'am', 'are', 'were', 'been',
        'me', 'him', 'her', 'us', 'them', 'him', 'her', 'his', 'its', 'our', 'theirs',
        'so', 'if', 'then', 'than', 'these', 'those', 'through', 'during', 'before', 'after', 'above', 'below',
        'further', 'no', 'not', 'any', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'only', 'same', 'very', 'also', 'just', 'even', 'an', 'because', 'while', 'being', 'having',
        'about', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves',
        'instead', 'important', 'way', 'still', 'yet', 'now', 'here', 'there', 'well', 'good', 'best', 'too', 'much',
        'really', 'actually', 'quite', 'rather', 'somewhat', 'almost', 'never', 'always', 'sometimes', 'often'
    }

    counts = count_words(words, stop_words)
    top_words = get_top_words(counts, 10)

    print()
    print("----- Basic Writing Statistics -----")
    print("Total words:", len(words))
    print("Unique words (excluding stop words):", len(counts))
    
    # Analyze vocabulary difficulty
    vocab_analysis = analyze_vocabulary(words, counts)
    if vocab_analysis:
        print("Average word length:", vocab_analysis['avg_length'], "characters")
        print("Complexity score:", vocab_analysis['complexity_score'], "/ 100")
    print()

    print("----- Top 10 Most Common Words -----")
    for item in top_words:
        word = item[0]
        count = item[1]
        print(word, ":", count)
    
    # Identify and display themes
    themes = identify_themes(top_words, counts)
    
    if themes:
        print()
        print("----- Common Themes -----")
        for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
            print(theme, ":", count)
    else:
        print()
        print("----- Common Themes -----")
        print("No major themes detected in the essay.")
    
    # Display advanced vocabulary
    if vocab_analysis and vocab_analysis['advanced_words']:
        print()
        print("----- Advanced Vocabulary (8+ characters) -----")
        count = 0
        for word, freq in vocab_analysis['advanced_words'].items():
            if count < 10:  # Show top 10 advanced words
                print(word, ":", freq)
                count += 1



main()