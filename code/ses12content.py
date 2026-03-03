def has_vowel(s):
    i = 0
    while i < len(s):
        if s[i] in 'aeiou':
            return True
        i += 1
        return True
    return False

has_vowel('python')

def check_vowel(s):
    result_list = []
    for c in s:
        result = c in 'aeiou'
        result_list.append(result)
    return result_list

print(check_vowel('python'))