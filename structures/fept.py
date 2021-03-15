# Implementation for this trie is adapted from: https://www.askpython.com/python/examples/trie-data-structure
class FrequentEpisodePrefixTree:
    """
    Represents a frequent episode prefix tree (FEPT) which stores all
    frequent episodes within a given event sequence in a space-efficient
    manner. It is a lexicographical rooted directed tree.
    """

    def __init__(self):
        self.root = FrequentEpisodePrefixTreeNode("", None, None)
        self.n_frequent_episodes = 0
        self.n_frequent_episode_rules = 0

    def insert(self, label, minimal_occurrences, support):
        """
        Insert a new node into the FEPT.
        """

        node = self.root
        for letter in label:
            if letter in node.children:
                node = node.children[letter]
            else:
                new_node = FrequentEpisodePrefixTreeNode(
                    label, minimal_occurrences, support)
                node.children[letter] = new_node
                node = new_node

        self.n_frequent_episodes += 1
        return node

    def exists(self, label):
        """
        Check if a node exists in the tree already
        """

        node = self.root
        for letter in label:
            if letter in node.children:
                node = node.children[letter]
            else:
                return False
        return True

    def dfs(self, node):
        """
        Perform a depth-first search starting from a given node
        """

        # Do not append root node to output
        if node.label:
            self.frequent_episodes.append(node)

        for child in node.children.values():
            if node.label:
                episode_rule = self.get_episode_rule(node, child)
                if episode_rule:
                    self.episode_rules.append(episode_rule)
                    self.n_frequent_episode_rules += 1

            self.dfs(child)

    def get_all_frequent_episodes_and_episode_rules(self):
        """
        Collects all the frequently occurring episodes
        and stores them in a array
        """

        node = self.root
        self.frequent_episodes = []
        self.episode_rules = []

        self.dfs(node)

        return self.frequent_episodes, self.episode_rules

    def get_episode_rule(self, node, child):
        """
        Generates an episode rule for a given node and its child
        """

        # Get the confidence of the rule
        rule_conf = (child.support / node.support)

        if rule_conf >= self.min_conf:
            return f"{node.label} -> {child.label} (Support: {child.support}) (Confidence: {rule_conf * 100:.2f}%)"

        # Else return nothing
        return

    def output_to_file(self, min_conf):
        """
        Outputs the frequently occurring episodes and episode
        rules to .txt files
        """

        self.min_conf = min_conf

        # Get frequent episodes and episode rules
        frequent_episodes, episode_rules = self.get_all_frequent_episodes_and_episode_rules()

        # Output frequent epsidodes
        with open("frequent_episodes.txt", "w") as f:
            print("Episode\t\t\tSupport", file=f)
            for episode in frequent_episodes:
                print(f"{episode.label:<16}{episode.support}", file=f)

        # Output episode rules
        with open("episode_rules.txt", "w") as f:
            for rule in episode_rules:
                print(rule, file=f)


class FrequentEpisodePrefixTreeNode:
    """
    Represents a node of the FEPT.
    Stores the nodes label, minimal_occurences set and its support value
    """

    def __init__(self, label, minimal_occurrences, support):
        self.label = label
        self.minimal_occurrences = minimal_occurrences
        self.support = support
        self.children = {}
