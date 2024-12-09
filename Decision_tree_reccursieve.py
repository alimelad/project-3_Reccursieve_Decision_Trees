import random

def show_recursive(tree, node_index=0, level=0):
    """Fully recursive function to print the tree structure."""
    print('   ' * level + '{}-'.format(node_index), end="")
    print('{}'.format(tree[node_index]['name']), end="")
    print('#{}'.format(tree[node_index]['ancestor']), end="")
    if tree[node_index]['type'] == 't':
        print("(t){}".format(tree[node_index]['pay']))
    elif tree[node_index]['type'] == 'd':
        print("(d)")
        for descendant in tree[node_index]['descendants']:
            show_recursive(tree, descendant, level + 1)
    elif tree[node_index]['type'] == 'n':
        print("(n)[", end="")
        print(', '.join(map(str, tree[node_index]['probabilities'])), end="")
        print(']')
        for descendant in tree[node_index]['descendants']:
            show_recursive(tree, descendant, level + 1)

def solve_recursive(tree, node_index=0):
    """Recursive function for solving decision tree with backward induction."""
    node = tree[node_index]
    if node['type'] == 't':
        # Base case for terminal node
        return node['pay']
    elif node['type'] == 'd':
        # Decision node: maximize value among descendants
        subvalues = [(descendant, solve_recursive(tree, descendant)) for descendant in node['descendants']]
        best_descendant, best_value = max(subvalues, key=lambda x: x[1])
        node['subvalue'] = best_value
        node['used'] = True
        return best_value
    elif node['type'] == 'n':
        # Nature node: calculate expected value
        expected_value = sum(prob * solve_recursive(tree, desc)
                             for prob, desc in zip(node['probabilities'], node['descendants']))
        node['subvalue'] = expected_value
        node['used'] = True
        return expected_value

def play_recursive(tree, strategy, node_index=0):
    """Recursive function to play the tree according to strategy."""
    node = tree[node_index]
    if node['type'] == 't':
        return node_index, node['name'], node['pay']
    elif node['type'] == 'd':
        next_node = strategy[node_index]
        return play_recursive(tree, strategy, next_node)
    elif node['type'] == 'n':
        random_prob = random.random()
        cumulative = 0.0
        for prob, desc in zip(node['probabilities'], node['descendants']):
            cumulative += prob
            if random_prob <= cumulative:
                return play_recursive(tree, strategy, desc)

def simulate_recursive(strategy, tree, trials=20):
    """Recursive function for simulating the strategy over multiple trials."""
    if trials == 0:
        return []
    result = play_recursive(tree, strategy)
    return [result] + simulate_recursive(strategy, tree, trials - 1)

def monte_carlo(first_strategy, second_strategy, tree, start, increment):
    """Monte Carlo simulation for decision tree strategies."""
    num_trials = start
    for _ in range(10):
        one_count, two_count = tournament(first_strategy, second_strategy, tree, num_trials)
        print(f"Trials: {num_trials}, Strategy 1 Wins: {one_count}, Strategy 2 Wins: {two_count}")
        num_trials += increment

def tournament(strategy_one, strategy_two, tree, num_trials):
    """Runs a tournament to compare two strategies."""
    wins_one = wins_two = 0
    for _ in range(num_trials):
        outcome_one = simulate_recursive(strategy_one, tree, 1)[0]
        outcome_two = simulate_recursive(strategy_two, tree, 1)[0]
        if outcome_one[2] >= outcome_two[2]:
            wins_one += 1
        else:
            wins_two += 1
    return wins_one, wins_two

def load_tree(filename):
    """Load a tree from a file."""
    tree = []
    with open(filename, 'r') as file:
        node_data = {}
        for line in file:
            key, value = line.strip().split(',', 1)
            if key == 'node':
                if node_data:
                    tree.append(node_data)
                node_data = {'descendants': [], 'probabilities': []}
            elif key.startswith('descendant'):
                node_data['descendants'].append(int(value))
            elif key.startswith('prob'):
                node_data['probabilities'].append(float(value))
            else:
                node_data[key] = value if key != 'pay' else float(value)
        tree.append(node_data)  # Add the last node
    return tree

def save_tree(tree, filename):
    """Save a tree to a file."""
    with open(filename, 'w') as file:
        for idx, node in enumerate(tree):
            file.write(f"node,{idx}\n")
            for key, value in node.items():
                if key in ['descendants', 'probabilities']:
                    for item in value:
                        file.write(f"{key},{item}\n")
                else:
                    file.write(f"{key},{value}\n")

def main():
    """Main interactive menu."""
    print("Welcome to the Recursive Decision Tree Program!")
    tree = []
    while True:
        print("\nMenu:")
        print("1. Load Tree")
        print("2. Show Tree")
        print("3. Solve Tree")
        print("4. Simulate Strategy")
        print("5. Monte Carlo")
        print("6. Save Tree")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            filename = input("Enter filename to load: ")
            tree = load_tree(filename)
        elif choice == '2':
            show_recursive(tree)
        elif choice == '3':
            solve_recursive(tree)
            print("Tree solved. Optimal strategy calculated.")
        elif choice == '4':
            strategy = [0] * len(tree)  # Example strategy
            results = simulate_recursive(strategy, tree)
            print("Simulation Results:", results)
        elif choice == '5':
            strategy_one = [0] * len(tree)  # Example strategies
            strategy_two = [0] * len(tree)
            monte_carlo(strategy_one, strategy_two, tree, start=10, increment=10)
        elif choice == '6':
            filename = input("Enter filename to save: ")
            save_tree(tree, filename)
        elif choice == '7':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()
