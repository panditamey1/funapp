def get_subsequences(predefined_list, numbers):
    subsequences = []
    in_sequence = False
    current_sequence = []

    for num in numbers:
        if num in predefined_list:
            if not in_sequence:
                if current_sequence:
                    subsequences.append(current_sequence)
                current_sequence = []
                in_sequence = True
            current_sequence.append(num)
        else:
            if in_sequence:
                current_sequence.append(num)
                subsequences.append(current_sequence)
                current_sequence = []
                in_sequence = False
            else:
                if current_sequence:
                    subsequences.append(current_sequence)
                    current_sequence = []

    # Append the last sequence if it ends at the last element
    if current_sequence:
        subsequences.append(current_sequence)

    return subsequences

def categorize_subsequences(subsequences, predefined_list):
    successful_doubles = []
    failed_doubles = []
    successful_triples = []
    failed_triples = []

    for seq in subsequences:
        if len(seq) >= 2:
            if seq[0] in predefined_list and seq[1] in predefined_list:
                successful_doubles.append(seq)
            else:
                failed_doubles.append(seq)
        if len(seq) >= 3:
            if seq[0] in predefined_list and seq[1] in predefined_list and seq[2] in predefined_list:
                successful_triples.append(seq)
            else:
                failed_triples.append(seq)

    return successful_doubles, failed_doubles, successful_triples, failed_triples

# Example usage:
predefined_list = [1, 4, 5, 7, 9]
numbers = [10, 1, 7, 11, 5, 1, 4, 6, 4, 32, 5, 9, 12]

subsequences = get_subsequences(predefined_list, numbers)
print(subsequences)
successful_doubles, failed_doubles, successful_triples, failed_triples = categorize_subsequences(subsequences, predefined_list)

print("Successful Doubles:", successful_doubles)
print("Failed Doubles:", failed_doubles)
print("Successful Triples:", successful_triples)
print("Failed Triples:", failed_triples)
