# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
        
class Solution:
    def twoSum(self, nums, target):
        '''
        两数之和
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
        两数相加
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
        无重复字符的最长子串
        给定一个字符串，请你找出其中不含有重复字符的 最长子串的长度。

        示例 1:

        输入: "abcbb"
        输出: 3 
        解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
        
        para:
            s: str
        return；
            index : int
        
        ''' 
        result = []
        lenth = []
        for j, n in enumerate(s):
            dup = []
            dup.append(n)
            for i in list(s[j + 1 :]):
                if i not in dup:
                    dup.append(i)
                else:
                    lenth.append(len(dup))
                    result.append(dup)
                    dup = []
            lenth.append(len(dup))
            
        return max(lenth)




                
