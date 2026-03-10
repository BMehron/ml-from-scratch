def longestOnes(self, nums: List[int], k: int) -> int:
    # Rephrase the problem as: find the longset subarray with max k zeros
    max_count = 0
    zero_count = 0
    left = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zero_count += 1
        if zero_count > k:
            while nums[left] == 1:
                left += 1
            left += 1
            zero_count -= 1
        max_count = max(max_count, right - left + 1)
    return max_count