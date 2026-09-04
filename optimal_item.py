
"""
=====================================================================
OPTIMAL SELECTION OF ITEMS WITHIN A WEIGHT CONSTRAINT
              (0/1 KNAPSACK PROBLEM)

Approaches included:
1. Brute Force
2. Top-Down DP (Memoization)
3. Bottom-Up DP (Tabulation)

Algorithms Lab – Dynamic Programming
=====================================================================

IN PLAIN ENGLISH:

You have a bag with a limited weight capacity.

Each item has:
- A weight
- A value

For every item, you have only two choices:

0 = Do not take the item
1 = Take the item

The goal is to select items whose total weight does not exceed
the capacity while maximizing the total value.

=====================================================================
"""

import timeit
import random


# =====================================================================
# 1. BRUTE FORCE
#    Time Complexity: O(2^n)
# =====================================================================

def knapsack_brute_force(weights, values, capacity, n=None):

    if n is None:
        n = len(weights)

    # Base condition
    if n == 0 or capacity == 0:
        return 0

    # If current item is heavier than capacity, skip it
    if weights[n - 1] > capacity:
        return knapsack_brute_force(
            weights,
            values,
            capacity,
            n - 1
        )

    # Include current item
    include = values[n - 1] + knapsack_brute_force(
        weights,
        values,
        capacity - weights[n - 1],
        n - 1
    )

    # Exclude current item
    exclude = knapsack_brute_force(
        weights,
        values,
        capacity,
        n - 1
    )

    return max(include, exclude)


# =====================================================================
# 2. TOP-DOWN DP — MEMOIZATION
#    Time Complexity : O(n * capacity)
#    Space Complexity: O(n * capacity)
# =====================================================================

def knapsack_top_down(weights, values, capacity):

    n = len(weights)

    # Dictionary to store already calculated results
    memo = {}

    def helper(i, remaining_capacity):

        # Base condition
        if i == 0 or remaining_capacity == 0:
            return 0

        # Check if result is already calculated
        if (i, remaining_capacity) in memo:
            return memo[(i, remaining_capacity)]

        # If item cannot fit, skip it
        if weights[i - 1] > remaining_capacity:

            result = helper(
                i - 1,
                remaining_capacity
            )

        else:

            # Take the item
            include = values[i - 1] + helper(
                i - 1,
                remaining_capacity - weights[i - 1]
            )

            # Do not take the item
            exclude = helper(
                i - 1,
                remaining_capacity
            )

            result = max(include, exclude)

        # Store result
        memo[(i, remaining_capacity)] = result

        return result

    return helper(n, capacity)


# =====================================================================
# 3. BOTTOM-UP DP — TABULATION
#    Time Complexity : O(n * capacity)
#    Space Complexity: O(n * capacity)
# =====================================================================

def build_knapsack_table(weights, values, capacity):

    n = len(weights)

    # Create DP table
    dp = [
        [0] * (capacity + 1)
        for _ in range(n + 1)
    ]

    # Fill the table
    for i in range(1, n + 1):

        for w in range(capacity + 1):

            # If item cannot fit
            if weights[i - 1] > w:

                dp[i][w] = dp[i - 1][w]

            else:

                # Do not take the item
                exclude = dp[i - 1][w]

                # Take the item
                include = (
                    values[i - 1]
                    + dp[i - 1][w - weights[i - 1]]
                )

                # Choose the better option
                dp[i][w] = max(include, exclude)

    return dp


# =====================================================================
# 4. RECONSTRUCT SELECTED ITEMS
# =====================================================================

def reconstruct_selected_items(dp, weights, values, capacity):

    n = len(weights)

    w = capacity

    selected = []

    # Move backwards through the DP table
    for i in range(n, 0, -1):

        # If value changed, item was selected
        if dp[i][w] != dp[i - 1][w]:

            selected.append(i - 1)

            w = w - weights[i - 1]

    # Reverse to get original order
    selected.reverse()

    return selected


# =====================================================================
# 5. MAIN BOTTOM-UP FUNCTION
# =====================================================================

def knapsack_bottom_up(weights, values, capacity):

    dp = build_knapsack_table(
        weights,
        values,
        capacity
    )

    n = len(weights)

    max_value = dp[n][capacity]

    selected = reconstruct_selected_items(
        dp,
        weights,
        values,
        capacity
    )

    return max_value, selected, dp


# =====================================================================
# 6. PRINT DP TABLE
# =====================================================================

def print_dp_table(dp, capacity):

    print("\nDP Table:")

    print("Item/Capacity", end="")

    for w in range(capacity + 1):
        print(f"{w:4}", end="")

    print()

    for i, row in enumerate(dp):

        print(f"{i:>13}", end="")

        for value in row:
            print(f"{value:4}", end="")

        print()


# =====================================================================
# 7. DEMO / DRIVER CODE
# =====================================================================

if __name__ == "__main__":

    weights = [2, 3, 4, 5]

    values = [3, 4, 5, 6]

    capacity = 5


    print("====================================================")
    print("             0/1 KNAPSACK PROBLEM")
    print("====================================================")

    print("\nItems (weight, value):")

    for i in range(len(weights)):
        print(
            f"  Item {i}: "
            f"weight={weights[i]}, "
            f"value={values[i]}"
        )

    print(f"\nKnapsack capacity: {capacity}")


    # ---------------------------------------------------------------
    # Brute Force
    # ---------------------------------------------------------------

    brute_result = knapsack_brute_force(
        weights,
        values,
        capacity
    )

    print(f"\n[1] Brute force : {brute_result}")


    # ---------------------------------------------------------------
    # Top-Down Memoization
    # ---------------------------------------------------------------

    memo_result = knapsack_top_down(
        weights,
        values,
        capacity
    )

    print(f"[2] Top-down    : {memo_result}")


    # ---------------------------------------------------------------
    # Bottom-Up Tabulation
    # ---------------------------------------------------------------

    max_value, selected, dp = knapsack_bottom_up(
        weights,
        values,
        capacity
    )

    print(f"[3] Bottom-up   : {max_value}")


    # ---------------------------------------------------------------
    # Selected items
    # ---------------------------------------------------------------

    print(
        f"    Selected items (0-indexed): {selected}"
    )

    total_weight = 0
    total_value = 0

    for idx in selected:

        print(
            f"      item {idx}: "
            f"weight={weights[idx]}, "
            f"value={values[idx]}"
        )

        total_weight += weights[idx]
        total_value += values[idx]


    print(f"\nTotal weight : {total_weight}")
    print(f"Total value  : {total_value}")


    # ---------------------------------------------------------------
    # DP Table
    # ---------------------------------------------------------------

    print_dp_table(dp, capacity)


    # ---------------------------------------------------------------
    # Check all approaches
    # ---------------------------------------------------------------

    assert brute_result == max_value
    assert memo_result == max_value

    print(
        "\n[check] All three approaches agree "
        "on the maximum value."
    )


    # ---------------------------------------------------------------
    # Timing comparison
    # ---------------------------------------------------------------

    random.seed(42)

    n_big = 22

    big_weights = [
        random.randint(1, 15)
        for _ in range(n_big)
    ]

    big_values = [
        random.randint(1, 20)
        for _ in range(n_big)
    ]

    big_capacity = 50


    t_brute = timeit.timeit(
        lambda: knapsack_brute_force(
            big_weights,
            big_values,
            big_capacity
        ),
        number=1
    )

    t_bottom_up = timeit.timeit(
        lambda: knapsack_bottom_up(
            big_weights,
            big_values,
            big_capacity
        ),
        number=1
    )


    print(
        f"\nTiming with {n_big} items, "
        f"capacity {big_capacity}:"
    )

    print(
        f"  brute force : {t_brute:.5f} sec"
    )

    print(
        f"  bottom-up   : {t_bottom_up:.8f} sec"
        f"  (much faster)"
    )

