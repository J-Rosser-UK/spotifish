class LexoRank:

    ALPHABET_SIZE = 26
    RESERVED_START = "aaaa"
    RESERVED_END = "zzzzzz"

    @staticmethod
    def calculate_top(second):
        # Use the reserved starting rank as the first rank
        first = LexoRank.RESERVED_START.ljust(len(second), 'a')

        # Ensure the second rank is greater than the first
        if first >= second:
            raise ValueError(f"Second rank '{second}' must be greater than the reserved start rank '{first}'.")

        # Convert each character in the ranks to a number (0 for 'a', 1 for 'b', etc.)
        first_codes = [ord(char) - ord('a') for char in first]
        second_codes = [ord(char) - ord('a') for char in second]

        # Calculate the difference between the two ranks
        diff = sum((b - a) * (LexoRank.ALPHABET_SIZE ** i) for i, (a, b) in enumerate(zip(reversed(first_codes), reversed(second_codes))))

        # Reduce the difference to get as close as possible to the second rank
        diff -= 1

        # Build the new rank just below the second rank
        new_rank = []
        for i in range(len(second)):
            position = len(second) - 1 - i
            current_diff = (diff // (LexoRank.ALPHABET_SIZE ** i)) % LexoRank.ALPHABET_SIZE
            code = ord(first[position]) + current_diff

            # Adjust for character overflow
            if code > ord('z'):
                code -= LexoRank.ALPHABET_SIZE
                diff += LexoRank.ALPHABET_SIZE ** (i + 1)

            new_rank.append(chr(code))

        return ''.join(reversed(new_rank))
    
    @staticmethod
    def calculate_rank(first, second):
        # Check if the first rank is not greater than or equal to the second rank.
        # This is essential to ensure that we have a valid range for finding a middle rank.
        if first >= second:
            raise ValueError(f"First rank '{first}' must be less than second rank '{second}'.")

        # Equalize the lengths of the two ranks by padding the shorter one with 'a's.
        # This is necessary because we're going to compare the ranks character by character.
        max_length = max(len(first), len(second))
        first, second = first.ljust(max_length, 'a'), second.ljust(max_length, 'a')

        # Convert each character in the ranks to a number (0 for 'a', 1 for 'b', etc.).
        # This conversion allows us to perform arithmetic operations on the ranks.
        first_codes = [ord(char) - ord('a') for char in first]
        second_codes = [ord(char) - ord('a') for char in second]

        # Calculate the difference between the two ranks.
        # This is done by subtracting the code of each character in 'first' from the corresponding character in 'second',
        # multiplied by the alphabet size to the power of the character's position (reversed).
        diff = sum((b - a) * (LexoRank.ALPHABET_SIZE ** i) for i, (a, b) in enumerate(zip(reversed(first_codes), reversed(second_codes))))

        # If the difference is very small (1 or 0), we can't find a mid rank in between.
        # So we append a middle character (halfway between 'a' and 'z') to the first rank.
        if diff <= 1:
            return first + chr((ord('a') + ord('z')) // 2)
        
        # If we have enough space to find a middle rank, start building it character by character.
        mid_rank = []
        diff //= 2  # Divide the difference by 2 to find the middle value.
        for i in range(len(first)):
            position = len(first) - 1 - i  # Calculate the position from the end.
            current_diff = (diff // (LexoRank.ALPHABET_SIZE ** i)) % LexoRank.ALPHABET_SIZE  # Calculate the difference at this position.
            code = ord(first[position]) + current_diff  # Calculate the ASCII code for the new character.

            # If the new ASCII code is beyond 'z', wrap it around and adjust the difference for the next character.
            if code > ord('z'):
                code -= LexoRank.ALPHABET_SIZE
                diff += LexoRank.ALPHABET_SIZE ** (i + 1)
            
            mid_rank.append(chr(code))  # Append the new character to the mid rank.

        # Reverse and join the characters to form the final mid rank.
        return ''.join(reversed(mid_rank))
    

    



# # Usage
# new_rank = lexorank.calculate_rank("aabc", "aabd")
# print(new_rank)


# first = "aaa"
# new = "aaaan"

# for i in range(0,5):
#     save = new
#     new = LexoRank.calculate_rank(first, new)
#     print(first, new, save)


# # Usage
# new_rank = lexorank.calculate_top("aabd")
# print(new_rank)

# new = "zzz"

# for i in range(0,5):
#     save = new
#     new = LexoRank.calculate_top(new)
#     print(first, new, save)