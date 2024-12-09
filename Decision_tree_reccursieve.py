import random

# Recursive Function: Show Tree
def show_recursive(tree, node_index=0, level=0):
    """Displays the decision tree structure recursively."""
    if node_index >= len(tree):
        print(f"Error: Node index {node_index} out of range.")
        return
    node = tree[node_index]
    if 'name' not in node:
        print(f"Error: 'name' key missing in node {node_index}. Node details: {node}")
        return
    print('   ' * level + f"{node_index}-{node.get('name', 'Unknown')}#{node.get('ancestor', -1)}", end="")
    if node['type'] == 't':
        print(f"(t) {node.get('pay', 0.0)}")
    elif node['type'] == 'd':
        print("(d)")
        for descendant in node.get('descendants', []):
            show_recursive(tree, descendant, level + 1)
    elif node['type'] == 'n':
        print(f"(n)[{', '.join(map(str, node.get('probabilities', [])))}]")
        for descendant in node.get('descendants', []):
            show_recursive(tree, descendant, level + 1)

# Recursive Function: Solve Tree
def solve_recursive(tree, node_index=0):
    """Recursively computes the optimal strategy using backward induction."""
    node = tree[node_index]
    if node['type'] == 't':  # Terminal node
        return node['pay']
    elif node['type'] == 'n':  # Nature node
        subvalue = sum(prob * solve_recursive(tree, desc)
                       for prob, desc in zip(node.get('probabilities', []), node.get('descendants', [])))
        node['subvalue'] = subvalue
        return subvalue
    elif node['type'] == 'd':  # Decision node
        subvalues = [(desc, solve_recursive(tree, desc)) for desc in node.get('descendants', [])]
        best_descendant, best_value = max(subvalues, key=lambda x: x[1])
        node['subvalue'] = best_value
        node['best_descendant'] = best_descendant
        return best_value

# Recursive Function: Simulate Strategy
def simulate_recursive(tree, strategy, node_index=0, trials=1):
    """Simulates paths through the tree based on the given strategy."""
    if trials == 0:
        return []
    node = tree[node_index]
    if node['type'] == 't':  # Terminal node
        return [(node_index, node['name'], node['pay'])]
    elif node['type'] == 'd':  # Decision node
        next_node = strategy.get(node_index, node['descendants'][0])
        return simulate_recursive(tree, strategy, next_node, trials)
    elif node['type'] == 'n':  # Nature node
        cumulative, random_value = 0, random.random()
        for prob, desc in zip(node.get('probabilities', []), node.get('descendants', [])):
            cumulative += prob
            if random_value <= cumulative:
                return simulate_recursive(tree, strategy, desc, trials)

# Recursive Function: Monte Carlo Simulation
def monte_carlo_recursive(tree, strategy, trials, current=0, results=None):
    """Recursively performs Monte Carlo simulations."""
    if results is None:
        results = []
    if trials == 0:
        return results
    outcome = simulate_recursive(tree, strategy, current)
    results.append(outcome[-1][-1])  # Collect final payoff
    return monte_carlo_recursive(tree, strategy, trials - 1, current, results)

# Recursive Function: Path Analysis
def path_analysis_recursive(tree, node_index=0, path=None):
    """Recursively explores all paths through the tree."""
    if path is None:
        path = []
    node = tree[node_index]
    path.append((node_index, node['name']))
    if node['type'] == 't':  # Terminal node
        print(" -> ".join(f"{idx}({name})" for idx, name in path))
    elif node['type'] in ['d', 'n']:
        for desc in node.get('descendants', []):
            path_analysis_recursive(tree, desc, path[:])

# Helper: Load Tree
def load_tree(filename):
    """Load a tree from a file and dynamically compute 'ancestor' keys."""
    tree = []
    with open(filename, 'r') as file:
        node_data = {}
        for line in file:
            key, value = line.strip().split(',', 1)
            if key == 'node':
                # Save the current node and initialize a new one
                if node_data:
                    tree.append(node_data)
                node_data = {'descendants': [], 'probabilities': [], 'ancestor': -1}  # Initialize ancestor
            elif key.startswith('descendant'):
                node_data['descendants'].append(int(value))
            elif key.startswith('prob'):
                node_data['probabilities'].append(float(value))
            elif key == 'pay':
                node_data[key] = float(value)
            else:
                node_data[key] = value
        if node_data:  # Add the last node
            tree.append(node_data)
    
    # Ensure all nodes have required keys
    for i, node in enumerate(tree):
        node.setdefault('name', f"Node_{i}")  # Assign default name if missing
        node.setdefault('type', 'unknown')  # Default type for debugging
        node.setdefault('descendants', [])
        node.setdefault('probabilities', [])
        node.setdefault('ancestor', -1)

    # Assign 'ancestor' values dynamically
    for parent_index, parent_node in enumerate(tree):
        for descendant_index in parent_node.get('descendants', []):
            if 0 <= descendant_index < len(tree):
                tree[descendant_index]['ancestor'] = parent_index
            else:
                print(f"Error: Descendant {descendant_index} out of bounds for parent {parent_index}")

    # Debug: Print tree to confirm structure
    print("\nFinal tree structure (after assigning ancestors):")
    for i, node in enumerate(tree):
        print(f"Node {i}: {node}")

    return tree

# Main Execution
def main():
    """Interactive menu for the Decision Tree project."""
    tree = []  # Placeholder for loaded tree
    strategy = {}  # Example strategy
    print("Welcome to the Recursive Decision Tree Program!")
    while True:
        print("\nMenu:")
        print("1. Load Tree")
        print("2. Show Tree")
        print("3. Solve Tree")
        print("4. Simulate Strategy")
        print("5. Monte Carlo Simulation")
        print("6. Path Analysis")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            filename = input("Enter filename to load: ")
            tree = load_tree(filename)
        elif choice == "2":
            show_recursive(tree)
        elif choice == "3":
            solve_recursive(tree)
            print("Tree solved. Optimal strategies computed.")
        elif choice == "4":
            simulate_recursive(tree, strategy)
        elif choice == "5":
            results = monte_carlo_recursive(tree, strategy, trials=10)
            print(f"Monte Carlo Results: {results}")
        elif choice == "6":
            path_analysis_recursive(tree)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")
