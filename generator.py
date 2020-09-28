def if_sum_equals_to_number(init_combination: [], input_num: int):
    sum = 0
    for i in range(len(init_combination)):
        sum += init_combination[i]
    if sum == input_num:
        return True
    return False


class Generator:

    def __init__(self):
        self.fibonacci = [2, 3]
        self.combinations = []

    def find_combination(self, input_num: int, fibonacci: [], max_fib: int):
        combinations = []  # all combinations for the input number
        init_combination = []  # combination with the largest possible fibonacci number
        number_to_loop = input_num
        seq_len = len(fibonacci)
        index = seq_len - 1  # starting from the largest number
        for _ in range(seq_len + 1):
            if index >= 0:
                diff = number_to_loop - fibonacci[index]
                if diff >= 0:  # obtain the largest possible number
                    if fibonacci[index] > max_fib:
                        max_fib = fibonacci[index]
                    init_combination.append(fibonacci[index])
                    number_to_loop = diff  # find the largest possible number for the remaining part
                else:
                    index -= 1  # next largest fibonacci number index
        if number_to_loop == 0:
            combinations.append(init_combination)
        else:
            if fibonacci and index >= 0:
                number_to_loop = input_num - max_fib
                max_fib_index = fibonacci.index(max_fib)
                new_fib_seq = fibonacci[0:max_fib_index]
                if new_fib_seq:
                    combinations_for_the_rest, sub_max_fib = self.find_combination(number_to_loop, new_fib_seq, 0)
                    for com in combinations_for_the_rest:
                        com.append(max_fib)
                        init_combination = com
                        combinations.append(init_combination)

        if if_sum_equals_to_number(init_combination, input_num):
            for i in range(len(init_combination)):  # generate combinations for each number in the initial combination
                number = init_combination[i]
                number_index = fibonacci.index(number)
                combinations_for_number, sub_max_fib = self.find_combination(number, self.fibonacci[0:number_index], 0)
                init_combination_copy = init_combination.copy()
                del init_combination_copy[i]  # delete the target number in copy for sub-combinations
                for j in range(len(combinations_for_number)):  # replace the target number by the sub-combinations
                    for left_number in init_combination_copy:
                        combinations_for_number[j].append(left_number)
                for sub_combination in combinations_for_number:
                    combinations.append(sub_combination)

        return combinations, max_fib

    def get_fib_sequence(self, input_num: int):
        for _ in range(input_num):  # loop N times to make sure the sequence contains every needed fib numbers
            current_length = len(self.fibonacci)
            last = self.fibonacci[current_length - 2]
            current = self.fibonacci[current_length - 1]
            next = last + current
            self.fibonacci.append(next)

    def generate_combinations(self, input_num: int):
        self.get_fib_sequence(input_num)
        self.generate_for_one_max(input_num, self.fibonacci)
        return self.combinations

    def generate_for_one_max(self, input_num: int, fibonacci: []):
        max_fib = 0
        combinations, max_fib = self.find_combination(input_num, fibonacci, max_fib)
        for combination in combinations:
            self.combinations.append(combination)

        if max_fib != self.fibonacci[0]:
            max_fib_index = fibonacci.index(max_fib)
            new_fib_seq = fibonacci[0:max_fib_index]
            self.generate_for_one_max(input_num, new_fib_seq)
