# Encrypts one character using shift1 and shift2.
def _encrypt_char(ch: str, shift1: int, shift2: int) -> str:

    # Check if the character is a lowercase letter.
    if ch.islower():

        # a-m use shift1 multiplied by shift2.
        if ch <= 'm':
            # ord() changes the letter into a number so we can do maths with it.
            # % 13 keeps the result inside the first 13 letters.
            offset = (ord(ch) - ord('a') + shift1 * shift2) % 13

            # chr() changes the number back into a letter.
            return chr(offset + ord('a'))

        # n-z use shift2 instead.
        else:
            # Start from 'n', subtract shift2, and wrap around using % 13.
            offset = (ord(ch) - ord('n') - shift2) % 13
            return chr(offset + ord('n'))

    # Check if the character is an uppercase letter.
    elif ch.isupper():

        # A-M use shift1.
        if ch <= 'M':
            # Subtract shift1 and keep the result within A-M.
            offset = (ord(ch) - ord('A') - shift1) % 13
            return chr(offset + ord('A'))

        # N-Z use shift2 squared.
        else:
            # shift2 ** 2 means shift2 multiplied by itself.
            offset = (ord(ch) - ord('N') + shift2 ** 2) % 13
            return chr(offset + ord('N'))

    # Check if the character is a number.
    elif ch.isdigit():

        # Convert the digit to a number, apply the shifts, and wrap around 0-9.
        offset = (ord(ch) - ord('0') + (shift1 - shift2)) % 10
        return chr(offset + ord('0'))

    # Characters that are not letters or numbers are left unchanged.
    else:
        return ch


# Reads the input file, encrypts it, and saves the encrypted version.
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:

    # Open the input file so we can read its contents.
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Encrypt every character in the file.
    # ''.join() puts all the encrypted characters back into one string.
    encrypted = ''.join(_encrypt_char(ch, shift1, shift2) for ch in text)

    # Open the output file and write the encrypted text into it.
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted)

# Main part of the program.
def main() -> None:

    # Name of the original text file.
    raw_path = "raw_text.txt"

    # Name of the file where the encrypted text will be saved.
    encrypted_path = "encrypted_text.txt"

    # Keep asking for the shifts until valid numbers are entered.
    while True:
        try:
            # Get shift1 from the user and turn it into an integer.
            shift1 = int(input("Enter shift1 (non-negative integer): ").strip())

            # Get shift2 from the user and turn it into an integer.
            shift2 = int(input("Enter shift2 (non-negative integer): ").strip())

            # Make sure neither shift is negative.
            if shift1 < 0 or shift2 < 0:
                print("Both shifts must be non-negative integers. Please try again.\n")
                continue

            # Both values are valid, so leave the loop.
            break

        # This happens if the user enters something that is not an integer.
        except ValueError:
            print("Invalid input. Please enter integer values.\n")

    # Encrypt the raw text file and save the result.
    encrypt_file(shift1, shift2, raw_path, encrypted_path)

    # Tell the user that the encryption is finished.
    print(f"Encrypted '{raw_path}' -> '{encrypted_path}'")


# This makes sure main() only runs when this file is run directly.
if __name__ == "__main__":
    main()