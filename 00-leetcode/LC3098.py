class Solution:
    def minimumDeletions(self, word: str, k: int) -> int:
        # 没有说每个char都在，可以删除
        frequencies = list(Counter(word).values())
        res = float('inf')
        for target in range(1, max(frequencies) + 1):
            deletions = 0
            for freq in frequencies:
                if freq < target:
                    deletions += freq
                elif freq > target + k:
                    deletions += freq - (target + k)
            res = min(res, deletions)
        return res

