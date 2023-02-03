from urllib import request
from bs4 import BeautifulSoup
from collections import Counter
import threading

# Parse the HTML and extracts text from History section.
def extract_text(url):
    page = request.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    history_section = soup.find(id="History")
    text = " ".join([p.text for p in history_section.find_all("p")])
    return text

# Iterates through parsed words and counts them 
# and converts characters to lower case
def count_words(text):
    words = text.lower().split()
    return Counter(words)

# Removes punctuation
def process_text(url):
    text = extract_text(url)
    word_counts = count_words(text)
    return word_counts.most_common(10)

# Creates a main method to point the program where to go and what to parse
def main():
    url = "https://en.wikipedia.org/wiki/Microsoft"
    results = []
    threads = []
    for i in range(5):
        t = threading.Thread(target=process_text, args=(url,))
        t.start()
        threads.append(t)

    # Multithreads for scalability
    for t in threads:
        t.join()
        results.append(process_text(url))

    # Counts how many times the Top Ten words are used
    word_counts = Counter()
    for result in results:
        for word, count in result:
            word_counts[word] += count

    # Prints the results
    print(word_counts.most_common(10))

if __name__ == "__main__":
    main()
