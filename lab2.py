import heapq
import re

class Node:
    def _init_(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def _lt_(self, other):
        return self.f < other.f

def preprocess_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

def get_successors(node, doc1, doc2):
    successors = []
    idx1, idx2 = node.state

    if idx1 < len(doc1) and idx2 < len(doc2):
        new_state = (idx1 + 1, idx2 + 1)
        successor = Node(new_state, node)
        successors.append(successor)

    if idx1 < len(doc1):
        new_state = (idx1 + 1, idx2)
        successor = Node(new_state, node)
        successors.append(successor)

    if idx2 < len(doc2):
        new_state = (idx1, idx2 + 1)
        successor = Node(new_state, node)
        successors.append(successor)

    return successors

def heuristic(state, doc1, doc2):
    idx1, idx2 = state
    return ((len(doc1) - idx1) + (len(doc2) - idx2))/2

def a_star_plagiarism(doc1, doc2):
    start_state = (0, 0)
    goal_state = (len(doc1), len(doc2))
    start_node = Node(start_state)
    open_list = []
    heapq.heappush(open_list, (start_node.f, start_node))
    visited = set()

    while open_list:
        _, node = heapq.heappop(open_list)
        if node.state in visited:
            continue
        visited.add(node.state)

        if node.state == goal_state:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1]

        for successor in get_successors(node, doc1, doc2):
            idx1, idx2 = successor.state
            if idx1 < len(doc1) and idx2 < len(doc2):
                successor.g = node.g + edit_distance(doc1[idx1], doc2[idx2])
            else:
                successor.g = node.g + 1
            successor.h = heuristic(successor.state, doc1, doc2)
            successor.f = successor.g + successor.h
            heapq.heappush(open_list, (successor.f, successor))

    return None

def align_text(doc1, doc2):
    return a_star_plagiarism(doc1, doc2)

def detect_plagiarism(doc1, doc2, threshold=0.5):
    doc1 = [preprocess_text(sent) for sent in doc1]
    doc2 = [preprocess_text(sent) for sent in doc2]

    alignment = align_text(doc1, doc2)
    plagiarized = []
    for i, j in alignment:
        if i < len(doc1) and j < len(doc2):
            s1, s2 = doc1[i], doc2[j]
            max_len = max(len(s1), len(s2))
            if max_len > 0:
                similarity = 1 - (edit_distance(s1, s2) / max_len)
                if similarity >= threshold:
                    plagiarized.append((doc1[i], doc2[j], similarity))
    return plagiarized

doc1 = [
    "This is a test document.",
    "It has multiple sentences.",
    "Another sentence follows.",
    "hello world",
]

doc2 = [
    "This is a test doc.",
    "It contains several sentences.",
    "This sentence could be copied.",
    "world hello"   
]

plagiarism = detect_plagiarism(doc1, doc2)
if plagiarism:
    print("Potential plagiarism detected:")
    for pair in plagiarism:
        print(f"Doc1: {pair[0]} \nDoc2: {pair[1]} \nSimilarity: {pair[2]}")
else:
    print("No plagiarism detected.")
**
