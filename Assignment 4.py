"""
=====================================================================
NTH FIBONACCI NUMBER — CALCULATED EFFICIENTLY

Approaches included:
Naive Recursion, Memoized Recursion,
Iterative Tabulation, and Fast Doubling

Algorithms Lab – Efficient Fibonacci Number
=====================================================================
"""

import timeit


# =====================================================================
# 1. NAIVE RECURSION
# =====================================================================

def fib_recursive(n):
    if n <= 1:
        return n

    return fib_recursive(n - 1) + fib_recursive(n - 2)


# =====================================================================
# 2. MEMOIZED RECURSION
#    Top-Down Dynamic Programming
# =====================================================================

def fib_memo(n, memo=None):

    if memo is None:
        memo = {}

    if n <= 1:
        return n

    if n in memo:
        return memo[n]

    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)

    return memo[n]


# =====================================================================
# 3. ITERATIVE TABULATION
#    Bottom-Up Dynamic Programming
# =====================================================================

def fib_dp(n):

    if n <= 1:
        return n

    a, b = 0, 1

    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


# =====================================================================
# 4. FAST DOUBLING
#    Advanced O(log n) approach
# =====================================================================

def fib_fast_doubling(n):

    def _fib_pair(k):

        if k == 0:
            return (0, 1)

        a, b = _fib_pair(k // 2)

        c = a * (2 * b - a)
        d = a * a + b * b

        if k % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

    return _fib_pair(n)[0]


# =====================================================================
# 5. DEMO / DRIVER CODE
# =====================================================================

if __name__ == "__main__":

    n = 10

    print(f"Computing Fibonacci({n}) with four different approaches:\n")

    print(f"[1] Naive recursion    : {fib_recursive(n)}")
    print(f"[2] Memoized recursion : {fib_memo(n)}")
    print(f"[3] Iterative DP       : {fib_dp(n)}")
    print(f"[4] Fast doubling      : {fib_fast_doubling(n)}")


    # ---------------------------------------------------------------
    # First 15 Fibonacci numbers
    # ---------------------------------------------------------------

    print("\nFirst 15 Fibonacci numbers (using the iterative DP version):")

    print([fib_dp(i) for i in range(15)])


    # ---------------------------------------------------------------
    # Timing comparison
    # ---------------------------------------------------------------

    n_big = 28

    t_naive = timeit.timeit(
        lambda: fib_recursive(n_big),
        number=1
    )

    t_dp = timeit.timeit(
        lambda: fib_dp(n_big),
        number=1
    )

    print(f"\nTiming fib({n_big}):")

    print(f"  naive recursion : {t_naive:.5f} sec")
    print(f"  iterative DP    : {t_dp:.8f} sec  (thousands of times faster)")


    # ---------------------------------------------------------------
    # Very large n
    # ---------------------------------------------------------------

    n_huge = 100

    print(f"\nFibonacci({n_huge}) via iterative DP  : {fib_dp(n_huge)}")
    print(f"Fibonacci({n_huge}) via fast doubling : {fib_fast_doubling(n_huge)}")

