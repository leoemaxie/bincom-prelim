def recursive_search(arr, target, index=0):
    # Base case: if index is out of bounds
    if index >= len(arr):
        return -1
    # If the target is found at the current index
    if arr[index] == target:
        return index
    # Recur for the next index
    return recursive_search(arr, target, index + 1)

# Input list and target number
numbers = list(map(int, input("Enter a list of numbers separated by spaces: ").split()))
target = int(input("Enter the number to search for: "))

# Perform the search
result = recursive_search(numbers, target)

# Output the result
if result != -1:
    print(f"Number found at index {result}")
else:
    print("Number not found in the list")