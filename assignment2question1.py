# Encrypts one character using shift1 and shift2.
def _encrypt_char(ch: str, shift1: int, shift2: int) -> str:

    # Check if the character is a lowercase letter.
    if ch.islower():

        # a-n (first half, 14 letters) shift forward by shift1 * shift2.
        if ch <= 'n':
            # ord() changes the letter into a number so we can do maths with it.
            # % 14 keeps the result inside the 14 letters a-n.
            offset = (ord(ch) - ord('a') + shift1 * shift2) % 14

            # chr() changes the number back into a letter.
            return chr(offset + ord('a'))

        # o-z (second half, 12 letters) shift backward by shift1 + shift2.
        else:
            offset = (ord(ch) - ord('o') - (shift1 + shift2)) % 12
            return chr(offset + ord('o'))

    # Check if the character is an uppercase letter.
    elif ch.isupper():

        # A-M (13 letters) shift backward by shift1.
        if ch <= 'M':
            offset = (ord(ch) - ord('A') - shift1) % 13
            return chr(offset + ord('A'))

        # N-Z (13 letters) shift forward by shift2 squared.
        else:
            offset = (ord(ch) - ord('N') + shift2 ** 2) % 13
            return chr(offset + ord('N'))

    # Check if the character is a digit.
    elif ch.isdigit():

        # Digits shift forward by (shift1 - shift2), wrapped 0-9.
        offset = (ord(ch) - ord('0') + (shift1 - shift2)) % 10
        return chr(offset + ord('0'))

    # Characters that are not letters or digits are left unchanged.
    else:
        return ch


# Decrypts one character that was produced by _encrypt_char.
# Each rule below is the exact mathematical inverse of the matching
# rule in _encrypt_char: same range check, opposite sign on the shift.
def _decrypt_char(ch: str, shift1: int, shift2: int) -> str:

    if ch.islower():

        # a-n was shifted forward by shift1 * shift2, so shift back by
        # the same amount.
        if ch <= 'n':
            offset = (ord(ch) - ord('a') - shift1 * shift2) % 14
            return chr(offset + ord('a'))

        # o-z was shifted backward by shift1 + shift2, so shift forward.
        else:
            offset = (ord(ch) - ord('o') + (shift1 + shift2)) % 12
            return chr(offset + ord('o'))

    elif ch.isupper():

        # A-M was shifted backward by shift1, so shift forward.
        if ch <= 'M':
            offset = (ord(ch) - ord('A') + shift1) % 13
            return chr(offset + ord('A'))

        # N-Z was shifted forward by shift2 squared, so shift backward.
        else:
            offset = (ord(ch) - ord('N') - shift2 ** 2) % 13
            return chr(offset + ord('N'))

    elif ch.isdigit():

        # Digits were shifted forward by (shift1 - shift2), so shift back.
        offset = (ord(ch) - ord('0') - (shift1 - shift2)) % 10
        return chr(offset + ord('0'))

    else:
        return ch


# Reads the input file, encrypts it, and saves the encrypted version.
def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    encrypted = ''.join(_encrypt_char(ch, shift1, shift2) for ch in text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(encrypted)


# Reads the encrypted file, decrypts it, and saves the decrypted version.
def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:

    # Open the encrypted file so we can read its contents.
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Decrypt every character using the inverse rules.
    decrypted = ''.join(_decrypt_char(ch, shift1, shift2) for ch in text)

    # Write the decrypted text back out.
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(decrypted)


# Compares the original file with the decrypted file and reports whether
# the round trip (encrypt -> decrypt) was successful.
def verify_files(original_path: str, decrypted_path: str) -> bool:

    with open(original_path, 'r', encoding='utf-8') as f:
        original_text = f.read()

    with open(decrypted_path, 'r', encoding='utf-8') as f:
        decrypted_text = f.read()

    is_match = original_text == decrypted_text

    if is_match:
        print("Verification successful: decrypted file matches the original file.")
    else:
        print("Verification failed: decrypted file does NOT match the original file.")

    return is_match


# Main part of the program.
def main() -> None:

    raw_path = "raw_text.txt"
    encrypted_path = "encrypted_text.txt"
    decrypted_path = "decrypted_text.txt"

    # Keep asking for the shifts until valid numbers are entered.
    while True:
        try:
            shift1 = int(input("Enter shift1 (non-negative integer): ").strip())
            shift2 = int(input("Enter shift2 (non-negative integer): ").strip())

            if shift1 < 0 or shift2 < 0:
                print("Both shifts must be non-negative integers. Please try again.\n")
                continue

            break

        except ValueError:
            print("Invalid input. Please enter integer values.\n")

    # 1. Encrypt the raw text file and save the result.
    encrypt_file(shift1, shift2, raw_path, encrypted_path)
    print(f"Encrypted '{raw_path}' -> '{encrypted_path}'")

    # 2. Decrypt the encrypted file.
    decrypt_file(shift1, shift2, encrypted_path, decrypted_path)
    print(f"Decrypted '{encrypted_path}' -> '{decrypted_path}'")

    # 3. Verify the decrypted file matches the original.
    verify_files(raw_path, decrypted_path)


# This makes sure main() only runs when this file is run directly.
if __name__ == "__main__":
    main()
