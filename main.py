def word_count(book):
    words = book.split()
    return len(words)

def char_count(book):
    new_book = book.lower()
    freq = {}
    
    for c in new_book:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1
        
    return freq

def report(path, book):
    words = word_count(book)
    alphabet = list(map(chr, range(97, 123)))
    char_dict = char_count(book)
    sorted_char_dict = dict(sorted(char_dict.items(), key=lambda item: item[1], reverse=True))
    letters = []
    letter_count = []
    
    for char, val in sorted_char_dict.items():
        if char in alphabet:
            letters.append(char)
            letter_count.append(val)
    
    print("--- Begin report of "+path+ " ---")
    print(words, "words found in the document \n \n")
    
    for i in range(len(letters)):
        print("The", "'"+letters[i]+"'", "character was found", letter_count[i], "times.")
       
if __name__ == "__main__":
    file_path = "books/frankenstein.txt"
    with open(file_path) as f:
        file_contents = f.read()
        #print(char_count(file_contents))
        report(file_path, file_contents)
        