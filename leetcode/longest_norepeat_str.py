# coding: utf8
__author__ = 'seven.wang'


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        i_s = 0
        i_e = 0
        result_max = 0
        for i in range(len(s)):
            # print i, i_s, i_e
            s_tmp = s[i_s:i_e]
            i_tmp = s_tmp.find(s[i])
            i_e = i + 1
            if i_tmp >= 0:
                i_s = i_s + i_tmp + 1
            if i_e - i_s > result_max:
                result_max = i_e - i_s
            # print i, i_s, i_e
        return result_max


print Solution().lengthOfLongestSubstring("aaaaaa")