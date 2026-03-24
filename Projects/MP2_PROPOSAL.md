## My Mini Project 2 Proposal (My College Essay Analyzer - Seeing my Progress/Growth as a writer)

**What I'm building:** I will be building an analysis tool that can help me analyze my college essays to identify possible repeats in words, patterns that occur in my writing, vocabulary difficulty, and perhaps how my writing differs overtime. 

**Why I chose this:** I chose this because I want this to be a tool to help me improve and grow as a writer myself. Writing is an important part of life, something that will never go away. So if I can make a tool that allows me to view the progress of my writing style and perhaps point out the mistakes/errors/commonalities that I have in my writing, this tool will definitely be very helpful especially for my time throughout college.

**Core features:**
- **Input Handling:** Accept one or more text files as input (e.g., via command-line arguments). Support batch processing for multiple essays to enable comparison.
- **Text Cleaning and Preprocessing:** Remove punctuation, convert to lowercase, and normalize words (e.g., stemming or lemmatization) to ensure accurate analysis.
- **Word Count and Uniqueness:** Calculate total word count and the number of unique words. Compute the ratio of unique to total words as a measure of vocabulary diversity.
- **Word Frequency Analysis:** Generate a list of the most frequent words (excluding stop words like "the," "and," "is"). Display the top 10-20 most repeated words with their counts, highlighting potential overuse (e.g., if a word appears more than 5% of the time).
- **Vocabulary Difficulty:** Calculate average word length (in characters) and use a simple readability score (e.g., based on syllable count or Flesch-Kincaid approximation) to gauge complexity. Flag words above a certain length (e.g., >8 characters) as potentially advanced vocabulary.
- **Pattern Detection:** Identify common phrases or sentence structures (e.g., repeated sentence starters like "In conclusion" or overuse of passive voice). Use basic NLP to detect n-grams (e.g., bigrams for word pairs).
- **Comparison Over Time:** For multiple essays, compare metrics across files (e.g., sorted by date). Show trends like increasing unique word ratio or decreasing average word length, with visualizations (e.g., bar charts for word frequency using Matplotlib).
- **Output:** Generate a summary report (text file or console output) with statistics, lists, and suggestions (e.g., "Consider replacing 'very' with more precise adverbs"). Optionally, export to CSV for further analysis.

**What I don't know yet:**
- How to ignore very common words like “the”, “and”, and “is” so results are more meaningful
- How to find the most frequent words
- How to clean text effectively by removing punctuation and normalizing words
- How to present the results easily so that it is simple to visualize and observe the results

**Potential Challenges and Solutions:**
- Handling large texts
- Accuracy of pattern detection: Start with basic rules
- Testing: Use sample essays (e.g., from past assignments) to validate outputs and ensure the tool highlights real improvements or issues.