def read_file(filename):
    """Read and return the contents of a file."""
    try:
        fin = open(filename)
        text = fin.read()
        fin.close()
        return text
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        print("Check the exact filename, including spaces and punctuation.")
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


def count_words(words):
    """Count word frequencies using a dictionary."""
    counts = {}

    for word in words:
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


def main():
    print("My College Essay Analyzer - Milestone 1")
    print()

    filename = input("Enter the name of your text file: ")

    text = read_file(filename)
    if text is None:
        return
    
    cleaned_text = clean_text(text)
    words = cleaned_text.split()

    counts = count_words(words)
    top_words = get_top_words(counts, 10)

    print()
    print("----- Basic Writing Statistics -----")
    print("Total words:", len(words))
    print("Unique words:", len(counts))
    print()

    print("----- Top 10 Most Common Words -----")
    for item in top_words:
        word = item[0]
        count = item[1]
        print(word, ":", count)



main()