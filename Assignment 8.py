n = int(input("Enter number of items: "))

weights = list(map(int, input("Enter weights: ").split()))
values = list(map(int, input("Enter values: ").split()))

capacity = int(input("Enter capacity: "))

# Bottom-Up Approach
dp = [[0] * (capacity + 1) for i in range(n + 1)]

for i in range(1, n + 1):
    for w in range(capacity + 1):
        if weights[i - 1] <= w:
            dp[i][w] = max(
                values[i - 1] + dp[i - 1][w - weights[i - 1]],
                dp[i - 1][w]
            )
        else:
            dp[i][w] = dp[i - 1][w]

print("Bottom-Up Maximum Value:", dp[n][capacity])

# Top-Down Approach
memo = {}

def knapsack(i, w):
    if i == n or w == 0:
        return 0

    if (i, w) in memo:
        return memo[(i, w)]

    if weights[i] <= w:
        memo[(i, w)] = max(
            values[i] + knapsack(i + 1, w - weights[i]),
            knapsack(i + 1, w)
        )
    else:
        memo[(i, w)] = knapsack(i + 1, w)

    return memo[(i, w)]

print("Top-Down Maximum Value:", knapsack(0, capacity))