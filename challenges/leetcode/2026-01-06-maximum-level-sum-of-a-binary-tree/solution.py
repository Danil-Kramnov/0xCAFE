"""
Maximum Level Sum of a Binary Tree
https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/
"""

from typing import Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        """
        BFS approach: traverse level by level, track sum at each level
        Return the level with maximum sum (1-indexed)
        """
        if not root:
            return 0

        max_sum = float('-inf')
        max_level = 1
        current_level = 1

        queue = deque([root])

        while queue:
            level_size = len(queue)
            level_sum = 0

            # Process all nodes at current level
            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Update max if current level has greater sum
            if level_sum > max_sum:
                max_sum = level_sum
                max_level = current_level

            current_level += 1

        return max_level


def run_tests():
    """Test your solution here"""
    sol = Solution()

    # Test case 1: [1,7,0,7,-8,null,null]
    #       1
    #      / \
    #     7   0
    #    / \
    #   7  -8
    root1 = TreeNode(1)
    root1.left = TreeNode(7)
    root1.right = TreeNode(0)
    root1.left.left = TreeNode(7)
    root1.left.right = TreeNode(-8)

    result1 = sol.maxLevelSum(root1)
    print(f"Test 1: {result1} (expected 2)")
    assert result1 == 2, f"Failed! Got {result1}, expected 2"

    # Test case 2: [989,null,10250,98693,-89388,null,null,null,-32127]
    root2 = TreeNode(989)
    root2.right = TreeNode(10250)
    root2.right.left = TreeNode(98693)
    root2.right.right = TreeNode(-89388)
    root2.right.right.right = TreeNode(-32127)

    result2 = sol.maxLevelSum(root2)
    print(f"Test 2: {result2} (expected 2)")
    assert result2 == 2, f"Failed! Got {result2}, expected 2"

    print("✅ All tests passed!")


if __name__ == "__main__":
    run_tests()
