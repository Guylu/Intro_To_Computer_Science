import itertools

INSTANCES = 1
FIRST = 0
SECOND = 1
EMPTY = 0


class Node:
    def __init__(self, data, pos=None, neg=None):
        self.data = data
        self.positive_child = pos
        self.negative_child = neg

    def get_data(self):
        return self.data

    def get_positive_child(self):
        return self.positive_child

    def get_negative_child(self):
        return self.negative_child


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms

    def get_illness(self):
        return self.illness

    def get_symptoms(self):
        return self.symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    """
    this class will generate a decision tree, and given records, will try to
    diagnose an illness.
    """

    def __init__(self, root):
        """
        constructor to place root of the tree
        :param root: reference to root
        """
        self.root = root

    def diagnose(self, symptoms):
        """
        given symptoms this func will diagnose an illness with the decision tree
        :param symptoms: list of symptoms
        :return: an illness
        """
        leaf = self.root
        while True:
            if leaf.get_data() in symptoms:
                leaf = leaf.get_positive_child()
            else:
                leaf = leaf.get_negative_child()
            if leaf.get_positive_child() is None:
                return leaf.get_data()

    def calculate_success_rate(self, records):
        """
        will calculate how many times the decision tree has preformed
        successfully
        :param records: list of record types
        :return: successes / length of records
        """
        success = 0
        for record in records:
            diag = self.diagnose(record.get_symptoms())
            if record.get_illness() == diag:
                success += 1
        return success / len(records)

    def all_illnesses(self):
        """
        will return a list of all the illnesses sorted by num of appearances
        :return:
        """
        illnesses = {}
        self.all_illnesses_helper(self.root, illnesses)
        # helper function that fills the dict with all the illnesses appearances
        sorted_illnesses = sorted(illnesses.items(), key=lambda x: x[INSTANCES],
                                  reverse=True)
        # the lambda func will sort the dict items(list) by  num of appearances
        # and wll reverse the result
        return [tup[FIRST] for tup in sorted_illnesses]
        # returns a list of the first indexes - the illness name.

    def all_illnesses_helper(self, node, illnesses):
        """
        will create a dict - {["illness"] = #appearances in tree
        :param node: node in tree
        :param illnesses: the dict to fill
        :return:
        """
        if not node.get_positive_child():
            if node.get_data() not in illnesses:
                illnesses[node.get_data()] = 1  # initialize spot
            else:
                illnesses[node.get_data()] += 1
        else:
            self.all_illnesses_helper(node.get_positive_child(), illnesses)
            self.all_illnesses_helper(node.get_negative_child(), illnesses)
            # recursive check

    def most_rare_illness(self, records):
        """
        will return the most rare illness the tree
        :param records: list of type record
        :return:
        """
        illnesses = {}
        # first of all fill with 0 all the illnesses.
        for illness in self.all_illnesses():
            illnesses[illness] = 0
        for record in records:
            diagnose = self.diagnose(record.get_symptoms())
            if diagnose in illnesses:
                illnesses[diagnose] += 1
        sorted_illnesses = sorted(illnesses.items(), key=lambda x: x[INSTANCES])
        # return only the most rare:
        return sorted_illnesses[FIRST][FIRST]

    def paths_to_illness(self, illness):
        """
        will receive an illness and return the path to get to it
        :param illness: illness to find
        :return: path consisting of true/false..
        """
        paths = []
        final = []
        self.paths_to_illness_helper(self.root, illness, paths, final)
        return final

    def paths_to_illness_helper(self, node, illness, paths, final):
        """
        will receive an illness and return the path to get to it
        :param node: node in tree
        :param illness: illness to find
        :param paths: current looking path
        :param final: finalized path
        :return: all of the paths to the illness
        """
        if not node.get_positive_child():
            if node.get_data() == illness:
                # final path!
                final.append(paths[:])
        else:
            # try true:
            paths.append(True)
            self.paths_to_illness_helper(node.get_positive_child(),
                                         illness, paths, final)
            paths.pop()
            # try false:
            paths.append(False)
            self.paths_to_illness_helper(node.get_negative_child(),
                                         illness, paths, final)
            paths.pop()


def build_tree(records, symptoms):
    """
    will build a decision tree with the given records and symptoms
    :param records: list of records
    :param symptoms: list of symptoms
    :return: root of generated tree
    """
    default_illness = records[FIRST].get_illness()
    return build_tree_helper(records, symptoms, default_illness)


def build_tree_helper(records, symptoms, default_illness):
    if len(symptoms) != EMPTY:
        # not a leaf:
        pos_records = []
        neg_records = []
        # split into records holding the symptom, and those that dont
        for record in records:
            if symptoms[FIRST] in record.get_symptoms():
                pos_records.append(record)
            else:
                neg_records.append(record)
        # create node recursively:
        return Node(
            symptoms[FIRST],
            build_tree_helper(pos_records, symptoms[SECOND:], default_illness),
            build_tree_helper(neg_records, symptoms[SECOND:], default_illness))
    else:  # leaf
        if len(records) == EMPTY:
            # a list of symptoms that no illness can answer for
            return Node(default_illness, None, None)
        rec_dict = num_appearances(records)
        # lambda to see witch illness can provide the best answer for the path:
        best_guess = max(rec_dict, key=lambda x: rec_dict[x])
        return Node(best_guess, None, None)


def num_appearances(records):
    """
    create a dict of appearances of illnesses in a list of records.
    :param records: list of records
    :return:
    """
    rec_dict = {}
    for record in records:
        if record.get_illness() not in rec_dict:
            rec_dict[record.get_illness()] = 1
        else:
            rec_dict[record.get_illness()] += 1
    return rec_dict


def optimal_tree(records, symptoms, depth):
    """
    will create the optimal tree given a depth
    :param records: list of records
    :param symptoms: list of symptoms
    :param depth: hpw many layers of symptoms to check - depth of tree
    :return: root of optimal tree
    """
    tree_list = []
    for comb in itertools.combinations(symptoms, depth):
        tree_list.append(Diagnoser(build_tree(records, list(comb))))

    # if only 1 tree no need to check everything else:
    if len(tree_list) == 1:
        return tree_list[FIRST]

    max_tree = tree_list[FIRST]
    max_tree_diag = tree_list[FIRST].calculate_success_rate(records)

    for tree in tree_list[SECOND:]:
        test = tree.calculate_success_rate(records)
        if test > max_tree_diag:
            max_tree = tree
            max_tree_diag = test

    return max_tree.root


if __name__ == "__main__":
    pass
