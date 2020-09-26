class CombiFinder:
    """
        arr - array to store combinations
        index - track how many items in array would be used to find sum
        difference - difference between `num` and sum of elements in `arr`
    """

    def find_combinations_util(self, arr: list, index: int, difference: int):
        # no need to continue increasing sum
        if difference < 0:
            return

        # combination is found
        if difference == 0:
            self.combinations.append(arr[:index])
            return

        # index in `self.fib` of number previously stored in `arr`
        # it helps in maintaining increasing order
        prev_value_index = 0 if (index == 0) else self.fib.index(arr[index - 1])

        # note loop starts from previous and includes only higher numbers
        # i.e. at array location index - 1
        for next_value_index in range(prev_value_index, self.len_fib):
            arr[index] = self.fib[next_value_index]

            # call recursively with reduced number
            self.find_combinations_util(arr, index + 1, difference - self.fib[next_value_index])

    def find_combinations(self, num: int):
        # calculating longest possible array for a given number
        arr = [0] * (num // 2) if not num % 2 else [0] * (num // 2 + 1)

        # generating Fibonacci sequence
        self.fib = [2]
        next_value = 3
        while num >= next_value:
            self.fib.append(next_value)
            next_value = self.fib[-1] + self.fib[-2]
        self.len_fib = len(self.fib)

        # find all combinations
        self.combinations = []
        self.find_combinations_util(arr, 0, num)

        return self.combinations
