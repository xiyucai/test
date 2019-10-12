# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
leetcode_name = {
    'twoSum' : '1.两数之和'
    'addTwoNumbers' : '2.两数相加'
    'lengthOfLongestSubstring' : '3.无重复字符的最长子串'
    'findMedianSortedArrays' : '4.寻找两个有序数组的中位数'
    'longestPalindrome' : '5. 最长回文子串'
}

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
        
class Solution:
    def twoSum(self, nums, target):
        '''
        1. 两数之和
        para:
            nums: List[int]
            target: int
        return；
            index : list[int]
        
        '''
        for i, n in enumerate(nums):
            for j, m in enumerate(nums[i + 1:]):
                if n + m == target:
                    return [i, j + i +1]
                

    def addTwoNumbers(self, l1, l2):
        '''
        2. 两数相加
        para:
            l1: List[int]
            l2: List[int]
        return；
            index : list[int]
        
        '''    
        def change_int(l1):
            num = ''
            for i in range(len(l1.val)):
                n = str(l1.val.pop())
                num = num + str(n)
            return int(num)
        
        result = []
        c_lst = list(str(c))
        for i in range(len(c_lst)):
            result.append(c_lst.pop())
            
        return ListNode(result)
    
    def lengthOfLongestSubstring(self, s):
        '''
        3. 无重复字符的最长子串
        给定一个字符串，请你找出其中不含有重复字符的 最长子串的长度。

        示例 1:

        输入: "abcbb"
        输出: 3 
        解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
        
        para:
            s: str
        return；
            tmp_ : int
        
        ''' 
        dic_ = {}
        tmp_ = 0
        j = 0
        for i in range(len(s)):
            if s[i] in s[j:i]:
                tmp = len(s[j:i])
                if tmp > tmp_:
                    tmp_ = tmp
                j = dic_[s[i]] + 1           
            else:
                if tmp_ < len(s[j:i+1]):
                    tmp_ = len(s[j:i+1])
            
            dic_[s[i]] = i
        return tmp_
    
    def findMedianSortedArrays(self, nums1, nums2):
            '''
            4. 寻找两个有序数组的中位数
            给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。
            请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
            你可以假设 nums1 和 nums2 不会同时为空。
            
            示例 1:

            nums1 = [1, 3]
            nums2 = [2]

            则中位数是 2.0
            
            示例 2：
            nums1 = [1, 2]
            nums2 = [3, 4]

            则中位数是 (2 + 3)/2 = 2.5

            para:
                nums1: List[int]
                nums2: List[int]
            return；
                median : float
            '''
            nums = sorted(nums1 + nums2)
            median_index = int(len(nums)/2)
            if len(nums) % 2 == 0 or len(nums) == 2:
                median = (nums[median_index] + nums[median_index - 1]) / 2
            else :
                median = nums[median_index]

            return median

    def def longestPalindrome(self, s):
            '''
            5. 最长回文子串
            给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000
            
            示例 1:

            输入: "babad"
            输出: "bab"
            注意: "aba" 也是一个有效答案。
            
            示例 2：
            
            输入: "cbbd"
            输出: "bb"

            para:
                s: str
            return；
                tmp_s_ : str
            '''
            dic_ = {}
            tmp_ = 0
            tmp_s_ = ''
            j = 0
            for i in range(len(s)):
                if s[i] in s[j:i]:
                    tmp = len(s[j:i+1])
                    tmp_s = s[dic_[s[i]]: i + 1]
                    if tmp > tmp_:
                        tmp_s_ = tmp_s
                        tmp_ = tmp
                    j = i            

                dic_[s[i]] = i

            if len(tmp_s_) == 0:
                try:
                    tmp_s_ = s[0]
                except:
                    tmp_s_ = s

            return tmp_s_

                
