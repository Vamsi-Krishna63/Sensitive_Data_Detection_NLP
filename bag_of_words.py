import json

# Load initial bag of words from a file
def load_bag_of_words(file_path="bag_of_words.json"):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save updated bag of words to a file
def save_bag_of_words(bag_of_words, file_path="bag_of_words.json"):
    with open(file_path, 'w') as file:
        json.dump(bag_of_words, file, indent=4)

# Update bag of words dynamically
def update_bag_of_words(bag_of_words, new_term, category):
    bag_of_words[new_term] = category
    save_bag_of_words(bag_of_words)
    print(f"Added '{new_term}' under '{category}' category.")

# CLI for managing bag of words
def manage_bag_of_words():
    bag_of_words = load_bag_of_words()
    print("\nCurrent Bag of Words:")
    print(json.dumps(bag_of_words, indent=4))

    while True:
        action = input("\nChoose action - Add (A), View (V), Exit (E): ").strip().lower()
        if action == 'a':
            term = input("Enter the new sensitive term: ").strip()
            category = input("Enter the category: ").strip()
            update_bag_of_words(bag_of_words, term, category)
        elif action == 'v':
            print("\nCurrent Bag of Words:")
            print(json.dumps(bag_of_words, indent=4))
        elif action == 'e':
            print("Exiting Bag of Words Manager.")
            break
        else:
            print("Invalid action. Please choose again.")

if __name__ == "__main__":
    manage_bag_of_words()
