# coding: utf8

import collections


__author__ = 'seven.wang'


def get_slide_window_max(nums, k):
    deque1 = collections.deque([])
    r_list = []
    for i in xrange(len(nums)):
        data = nums[i]
        while len(deque1) != 0 and deque1[-1] < data:
            deque1.pop()
        deque1.append(data)
        if i - k + 1 < 0:
            continue

        r_list.append(deque1[0])
        if r_list[i-k+1] == nums[i-k+1]:
            deque1.popleft()

    return r_list


def rotate(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: void Do not return anything, modify nums in-place instead.
    """
    if k == 0:
        return
    len_nums = len(nums)
    steps_num=k%len_nums
    nums.re

nums = [1,3,-1,-3,5,3,6,7]
k = 3

r_list = get_slide_window_max(nums, k)
for x in r_list:
    print x

print nums
rotate(nums, k)
print nums
