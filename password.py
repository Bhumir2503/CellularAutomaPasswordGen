import numpy as np
import random
import string
import argparse


class CellularAutomataPasswordGenerator:
    """
    A password generator using cellular automata principles.
    
    This implementation uses a 1D elementary cellular automaton (like Rule 30)
    to generate pseudorandom patterns, which are then mapped to password characters.
    """
    
    def __init__(self, width=100, iterations=50, rule=30):
        """
        Initialize the cellular automata password generator.
        
        Args:
            width (int): Width of the cellular automaton (number of cells)
            iterations (int): Number of iterations to run the automaton
            rule (int): Rule number (0-255) for the elementary cellular automaton
        """
        self.width = width
        self.iterations = iterations
        self.rule = rule
        self.rule_binary = format(rule, '08b')  # Convert rule to binary
        self.cells = np.zeros(width, dtype=int)
        
        # Initialize with a random seed in the middle
        self.cells[width // 2] = 1
        
        # Characters to use for password generation
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        
    def apply_rule(self, left, center, right):
        """Apply the cellular automaton rule to a cell and its neighbors."""
        # Convert three cells to an index (0-7)
        index = 7 - (4 * left + 2 * center + right)
        # Return the new state based on the rule
        return int(self.rule_binary[index])
    
    def evolve(self):
        """Evolve the cellular automaton by one generation."""
        new_cells = np.zeros_like(self.cells)
        
        for i in range(self.width):
            left = self.cells[(i - 1) % self.width]
            center = self.cells[i]
            right = self.cells[(i + 1) % self.width]
            new_cells[i] = self.apply_rule(left, center, right)
            
        self.cells = new_cells
    
    def run_automaton(self):
        """Run the cellular automaton for the specified number of iterations."""
        # Create a matrix to store all states
        history = np.zeros((self.iterations, self.width), dtype=int)
        
        # Store the initial state
        history[0] = self.cells
        
        # Evolve for iterations-1 steps
        for i in range(1, self.iterations):
            self.evolve()
            history[i] = self.cells
            
        return history
    
    def generate_password(self, length=16, include_lowercase=True, include_uppercase=True, 
                          include_digits=True, include_special=True):
        """
        Generate a password of the specified length using cellular automaton patterns.
        
        Args:
            length (int): Length of the password
            include_lowercase (bool): Include lowercase letters
            include_uppercase (bool): Include uppercase letters
            include_digits (bool): Include digits
            include_special (bool): Include special characters
            
        Returns:
            str: The generated password
        """
        # Determine which character sets to use
        char_sets = []
        if include_lowercase:
            char_sets.append(self.lowercase)
        if include_uppercase:
            char_sets.append(self.uppercase)
        if include_digits:
            char_sets.append(self.digits)
        if include_special:
            char_sets.append(self.special_chars)
            
        if not char_sets:
            raise ValueError("At least one character set must be selected")
            
        # Create a pool of all allowed characters
        char_pool = ''.join(char_sets)
        
        # Run the automaton
        history = self.run_automaton()
        
        # Use the last row and random rows for extra entropy
        last_row = history[-1]
        random_rows = [history[random.randint(0, self.iterations-1)] for _ in range(3)]
        
        # XOR the rows together for more randomness
        combined = last_row.copy()
        for row in random_rows:
            combined = np.logical_xor(combined, row).astype(int)
        
        # Use chunks of the combined row to select characters
        chunk_size = max(1, self.width // length)
        password = []
        
        for i in range(length):
            # Get a chunk of cells to determine the next character
            start_idx = (i * chunk_size) % (self.width - chunk_size)
            chunk = combined[start_idx:start_idx + chunk_size]
            
            # Convert the chunk to an integer
            value = int(''.join(map(str, chunk)), 2) % len(char_pool)
            
            # Add the character to the password
            password.append(char_pool[value])
            
        # Ensure all required character types are present
        self._ensure_character_types(password, include_lowercase, include_uppercase, 
                                    include_digits, include_special)
        
        return ''.join(password)
    
    def _ensure_character_types(self, password, include_lowercase, include_uppercase, 
                               include_digits, include_special):
        """Ensure that the password contains at least one of each required character type."""
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_special = any(c in self.special_chars for c in password)
        
        # Replace characters if necessary
        if include_lowercase and not has_lower:
            self._replace_character(password, self.lowercase)
            
        if include_uppercase and not has_upper:
            self._replace_character(password, self.uppercase)
            
        if include_digits and not has_digit:
            self._replace_character(password, self.digits)
            
        if include_special and not has_special:
            self._replace_character(password, self.special_chars)
    
    def _replace_character(self, password, char_set):
        """Replace a random character in the password with one from the given character set."""
        idx = random.randint(0, len(password) - 1)
        password[idx] = random.choice(char_set)


def main():
    parser = argparse.ArgumentParser(description='Generate a password using cellular automata')
    parser.add_argument('--length', type=int, default=16, help='Length of the password')
    parser.add_argument('--rule', type=int, default=30, choices=range(256), 
                        help='Rule number (0-255) for the cellular automaton')
    parser.add_argument('--width', type=int, default=100, help='Width of the cellular automaton')
    parser.add_argument('--iterations', type=int, default=50, 
                        help='Number of iterations to run the automaton')
    parser.add_argument('--no-lowercase', action='store_true', help='Exclude lowercase letters')
    parser.add_argument('--no-uppercase', action='store_true', help='Exclude uppercase letters')
    parser.add_argument('--no-digits', action='store_true', help='Exclude digits')
    parser.add_argument('--no-special', action='store_true', help='Exclude special characters')
    parser.add_argument('--count', type=int, default=1, help='Number of passwords to generate')
    
    args = parser.parse_args()
    
    generator = CellularAutomataPasswordGenerator(
        width=args.width,
        iterations=args.iterations,
        rule=args.rule
    )
    
    for i in range(args.count):
        password = generator.generate_password(
            length=args.length,
            include_lowercase=not args.no_lowercase,
            include_uppercase=not args.no_uppercase,
            include_digits=not args.no_digits,
            include_special=not args.no_special
        )
        print(f"Password {i+1}: {password}")


if __name__ == "__main__":
    main()