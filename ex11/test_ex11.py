import ex11
from ex11 import Node, Diagnoser, Record, build_tree, optimal_tree, parse_data

flu_leaf = Node("influenza", None, None)
cold_leaf = Node("cold", None, None)
inner_vertex = Node("fever", flu_leaf, cold_leaf)
healthy_leaf = Node("healthy", None, None)
root = Node("cough", inner_vertex, healthy_leaf)
doctor = Diagnoser(root)


def test_diagnose1():
    assert doctor.diagnose(["cough"]) == "cold"


def test_diagnose2():
    assert doctor.diagnose(["cough", "fever"]) == "influenza"


def test_diagnose3():
    assert doctor.diagnose(["fever"]) == "healthy"


def test_success_rate1():
    Record1 = Record("meth", ["cough"])
    Record2 = Record("big", ["cough"])
    Record3 = Record("loud", ["fever"])
    records = [Record1, Record2, Record3]
    assert doctor.calculate_success_rate(records) == 0.0


def test_success_rate2():
    Record1 = Record("cold", ["cough"])
    Record2 = Record("big", ["cough"])
    Record3 = Record("loud", ["fever"])
    records = [Record1, Record2, Record3]
    assert round(doctor.calculate_success_rate(records), 2) == 0.33


def test_success_rate3():
    Record1 = Record("cold", ["cough"])
    Record2 = Record("big", ["cough"])
    Record3 = Record("influenza", ["cough", "fever"])
    records = [Record1, Record2, Record3]
    assert round(doctor.calculate_success_rate(records), 2) == 0.67


def perms(lst1, lst2):
    set1 = set(lst1)
    set2 = set(lst2)
    if set1 == set2:
        return True
    return False


def test_all_illnesses1():
    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("influenza", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    results = doctor.all_illnesses()
    assert results[0] == "influenza"
    assert perms(results[1:], ["cold", "healthy"])


def test_all_illnesses2():
    flu_leaf = Node("cold", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("influenza", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    results = doctor.all_illnesses()
    assert results[0] == "cold"
    assert perms(results[1:], ["influenza", "healthy"])


def test_all_illnesses3():
    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("drugs", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    results = doctor.all_illnesses()
    assert perms(results, ["cold", "healthy", "influenza", "drugs"])


def test_rare_illness1():
    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("drugs", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    Record1 = Record("cold", ["cough"])
    Record2 = Record("cold", ["cough"])
    Record3 = Record("influenza", ["cough", "fever"])
    records = [Record1, Record2, Record3]

    assert doctor.most_rare_illness(records) in ["healthy", "drugs"]


def test_rare_illness2():
    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("drugs", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    Record1 = Record("healthy", [""])
    Record2 = Record("healthy", [""])
    Record3 = Record("cold", ["cough", ""])
    records = [Record1, Record2, Record3]

    assert doctor.most_rare_illness(records) in ["influenza", "drugs"]


def test_paths_to_illness1():
    flu_leaf = Node("influenza", None, None)
    cold_leaf = Node("influenza", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("drugs", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    assert sorted(doctor.paths_to_illness("influenza")) == sorted(
        [[True, True], [True, False]])


def test_paths_to_illness2():
    flu_leaf = Node("drugs", None, None)
    cold_leaf = Node("influenza", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    fever1 = Node("drugs", None, None)
    fever2 = Node("healthy", None, None)
    healthy_leaf = Node("fever", fever1, fever2)
    root = Node("cough", inner_vertex, healthy_leaf)
    doctor = Diagnoser(root)

    assert sorted(doctor.paths_to_illness("drugs")) == sorted(
        [[False, True], [True, True]])


def test_build_tree1():
    record1 = Record("influenza", ["cough", "fever"])
    record2 = Record("cold", ["cough"])
    record3 = Record("sick", ["strep", "cough"])
    records = [record1, record2, record3]

    no_fever_no_strep = Node("cold", None, None)
    no_fever_yes_strep = Node("sick", None, None)
    no_fever = Node("strep", no_fever_yes_strep, no_fever_no_strep)
    yes_fever_no_strep = Node("influenza", None, None)
    yes_fever_yes_strep = Node("N/A", None, None)
    yes_fever = Node("strep", yes_fever_yes_strep, yes_fever_no_strep)
    root = Node("fever", yes_fever, no_fever)

    tree = build_tree(records, ["fever", "strep"])

    assert tree.positive_child.negative_child.data == yes_fever_no_strep.data
    assert tree.negative_child.positive_child.data == no_fever_yes_strep.data
    assert tree.negative_child.negative_child.data == no_fever_no_strep.data


def test_build_tree2():
    record1 = Record("influenza", ["cough", "fever"])
    record2 = Record("cold", ["cough"])
    record3 = Record("cold", ["cough"])
    record4 = Record("dead", ["cough"])
    record5 = Record("dead", ["cough"])
    record6 = Record("dead", ["cough"])
    record7 = Record("sick", ["strep", "cough"])
    records = [record1, record2, record3, record4, record5,
               record6, record7]

    no_fever_no_strep = Node("dead", None, None)
    no_fever_yes_strep = Node("sick", None, None)
    no_fever = Node("strep", no_fever_yes_strep, no_fever_no_strep)
    yes_fever_no_strep = Node("influenza", None, None)
    yes_fever_yes_strep = Node("N/A", None, None)
    yes_fever = Node("strep", yes_fever_yes_strep, yes_fever_no_strep)
    root = Node("fever", yes_fever, no_fever)

    tree = build_tree(records, ["fever", "strep"])

    assert tree.positive_child.negative_child.data == yes_fever_no_strep.data
    assert tree.negative_child.positive_child.data == no_fever_yes_strep.data
    assert tree.negative_child.negative_child.data == no_fever_no_strep.data


def test_build_tree3():
    record1 = Record("influenza", ["cough", "fever"])
    record10 = Record("influenza", [])
    record11 = Record("influenza", [])

    record2 = Record("cold", ["cough"])
    record3 = Record("cold", ["cough"])
    record8 = Record("cold", ["cough"])
    record9 = Record("cold", ["cough"])

    record4 = Record("dead", ["cough"])
    record5 = Record("dead", ["cough"])
    record6 = Record("dead", ["cough"])

    record7 = Record("sick", ["strep", "cough"])

    records = [record1, record2, record3, record4, record5,
               record6, record7, record8, record9, record10, record11]

    no_fever_no_strep = Node("cold", None, None)
    no_fever_yes_strep = Node("sick", None, None)
    no_fever = Node("strep", no_fever_yes_strep, no_fever_no_strep)
    yes_fever_no_strep = Node("influenza", None, None)
    yes_fever_yes_strep = Node("N/A", None, None)
    yes_fever = Node("strep", yes_fever_yes_strep, yes_fever_no_strep)
    root = Node("fever", yes_fever, no_fever)

    tree = build_tree(records, ["fever", "strep"])

    assert tree.positive_child.negative_child.data == yes_fever_no_strep.data
    assert tree.negative_child.positive_child.data == no_fever_yes_strep.data
    assert tree.negative_child.negative_child.data == no_fever_no_strep.data


def test_build_tree4():
    record1 = Record("influenza", ["cough", "fever"])
    record10 = Record("influenza", [])
    record11 = Record("influenza", [])
    record12 = Record("influenza", [])
    record13 = Record("influenza", [])
    record14 = Record("influenza", [])

    record2 = Record("cold", ["cough"])
    record3 = Record("cold", ["cough"])
    record8 = Record("cold", ["cough"])
    record9 = Record("cold", ["cough"])

    record4 = Record("dead", ["cough"])
    record5 = Record("dead", ["cough"])
    record6 = Record("dead", ["cough"])

    record7 = Record("sick", ["strep", "cough"])

    records = [record1, record2, record3, record4, record5,
               record6, record7, record8, record9, record10, record11,
               record12, record13, record14]

    no_fever_no_strep = Node("influenza", None, None)
    no_fever_yes_strep = Node("sick", None, None)
    no_fever = Node("strep", no_fever_yes_strep, no_fever_no_strep)
    yes_fever_no_strep = Node("influenza", None, None)
    yes_fever_yes_strep = Node("N/A", None, None)
    yes_fever = Node("strep", yes_fever_yes_strep, yes_fever_no_strep)
    root = Node("fever", yes_fever, no_fever)

    tree = build_tree(records, ["fever", "strep"])

    assert tree.positive_child.negative_child.data == yes_fever_no_strep.data
    assert tree.negative_child.positive_child.data == no_fever_yes_strep.data
    assert tree.negative_child.negative_child.data == no_fever_no_strep.data


def test_build_tree5():
    record1 = Record("influenza", ["cough", "fever"])
    record10 = Record("influenza", [])
    record11 = Record("influenza", [])
    record12 = Record("influenza", [])
    record13 = Record("influenza", [])
    record14 = Record("influenza", [])

    record2 = Record("cold", ["cough"])
    record3 = Record("cold", ["cough"])
    record8 = Record("cold", ["cough"])
    record9 = Record("cold", ["cough"])

    record4 = Record("dead", ["cough"])
    record5 = Record("dead", ["cough"])
    record6 = Record("dead", ["cough"])

    record7 = Record("sick", ["strep", "cough"])
    record15 = Record("sick", ["strep"])

    records = [record1, record2, record3, record4, record5,
               record6, record7, record8, record9, record10, record11,
               record12, record13, record14, record15]

    no_cough_no_strep = Node("influenza", None, None)
    no_cough_yes_strep = Node("sick", None, None)
    no_cough = Node("strep", no_cough_yes_strep, no_cough_no_strep)
    yes_cough_no_strep = Node("cold", None, None)
    yes_cough_yes_strep = Node("sick", None, None)
    yes_cough = Node("strep", yes_cough_yes_strep, yes_cough_no_strep)
    root = Node("cough", yes_cough, no_cough)

    tree = build_tree(records, ["cough", "strep"])

    assert tree.positive_child.positive_child.data == yes_cough_yes_strep.data
    assert tree.positive_child.negative_child.data == yes_cough_no_strep.data
    assert tree.negative_child.positive_child.data == no_cough_yes_strep.data
    assert tree.negative_child.negative_child.data == no_cough_no_strep.data


def test_build_tree6():
    loaded = parse_data("custom_data.txt")

    tree = build_tree(loaded, ["cough", "headache"])

    assert tree.positive_child.positive_child.data == "cold"
    assert tree.positive_child.negative_child.data == "strep"
    assert tree.negative_child.positive_child.data == "meningitis"
    assert tree.negative_child.negative_child.data == "healthy"


def test_optimal_tree1():
    loaded = parse_data("optimal1.txt")

    tree = optimal_tree(loaded, ["psilocybin", "acid", "od"], 1)

    assert tree.positive_child.data == "dead"
    assert tree.negative_child.data == "drugs"


def print_tree(root_tree, level=1, answer=''):
    if not root_tree.positive_child:
        return
    print('    ' * (level - 1) + str(answer) + '+---' * (
                level > 0) + root_tree.data)
    if root_tree.positive_child:
        if root_tree.positive_child:
            print_tree(root_tree.positive_child, level + 1, 'P')
        if root_tree.negative_child:
            print_tree(root_tree.negative_child, level + 1, 'N')


def test_optimal_tree2():
    loaded = parse_data("optimal2.txt")

    tree = optimal_tree(loaded, ["od", "od2", "od3"], 2)

    print_tree(tree)

    if not (
            (tree.data == "od2" and tree.positive_child.data == "od3") or
            (tree.data == "od3" and tree.positive_child.data == "od2")
    ):
        assert False
    else:
        assert True
