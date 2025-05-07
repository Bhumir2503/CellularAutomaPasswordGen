import numpy as np

def password_strength_length(pw):
    #Password of length 16 or greater are considered uncrackable by today's standards so that is the max score 
    #Source: https://bitwarden.com/blog/how-long-should-my-password-be/
    length_score = len(pw)/16 * 100
    if (length_score > 100):
        length_score = 100

    return length_score



def password_strength_entropy(pw):
    entropy_points = 0
    
    pw_len = len(pw)
    charset_size = size_of_charset(pw)

    #Formula to calculate entropy of password
    #Using log base 2 will give how many bits are needed to encode the password
    entropy = np.log2(charset_size) / np.log2(2) * pw_len

    #128 bits of entropy or greater is considered uncrackable by today's standards so that is the max score
    #Source: https://nordvpn.com/blog/what-is-password-entropy/
    entropy_points = (entropy/128)*100

    #print("Entropy Points: ", entropy_points)
    
    if(entropy_points > 100):
        entropy_points = 100
    
    return entropy_points



def size_of_charset(pw):
    #Initialize length of charset to 0 by default
    charset = 0

    #Define list of special chars (same as in password.py)
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    if (any(char.islower() for char in pw)):
        charset += 26
    if (any(char.isupper() for char in pw)):
        charset += 26
    if (any(char.isdigit() for char in pw)):
        charset += 10
    
    #If password has any chars in common with list of special chars
    if (bool(set(special_chars) & set(pw))):
        charset += len(special_chars)

    #Returns the size of the charset
    return charset

def password_strength_complexity(pw):
    #Maximum size of charset for this experiment is 89 so that is the max score
    return size_of_charset(pw)/89 * 100


def password_strength_unpredictability(pw):
    common_passwords = set()
    filenames = ['10k-most-common.txt', 
                 '500-worst-passwords.txt',
                 '2020-200_most_used_passwords.txt',
                 '2023-200_most_used_passwords.txt',
                 '2024-197_most_used_passwords.txt',
                 '10-million-password-list-top-1000000.txt' ]
    for file in filenames:
        with open(file, 'r') as f:
            common_passwords.update(line.strip() for line in f)
    
    if pw in common_passwords:
        #Failed unpredictability test
        return 0
    else:
        #Passed unpredictability test
        return 100

    
def generate_cryptographic_score(pw):
    return (0.25 *  password_strength_length(pw)) + (0.25 * password_strength_entropy(pw)) + (0.25 * password_strength_complexity(pw)) + (0.25 * password_strength_unpredictability(pw))


#pw_input = input()
#print("Entered password:", pw_input)
#print("Cryptographic score: ", generate_cryptographic_score(pw_input))

