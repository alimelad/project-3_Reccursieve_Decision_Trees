# Decision Tree Recurssion Project

## **Overview**

This project implements a Decision Tree framework to analyze and solve decision-making problems using recursive algorithms. 
---

### **Key Features**

1. **Tree Representation**
   - Each decision tree is represented as a list of dictionaries.
   - Nodes are defined with attributes such as:
     - `name`: Identifier for the node.
     - `type`: Node type (`d` for decision, `n` for nature, `t` for terminal).
     - `descendants`: List of child nodes (for `d` and `n` types).
     - `probabilities`: Transition probabilities (for `n` type).
     - `pay`: Payoff value (for `t` type).

2. **Recursive Algorithms**
   - Fully recursive implementations for key operations:
     - `show_recursive`: Displays the tree structure with indentation for levels.
     - `solve_recursive`: Computes optimal strategies and values using backward induction.
     - `play_recursive`: Simulates paths based on strategies.
     - `simulate_recursive`: Runs multiple simulations of strategies.

3. **Monte Carlo Simulations**
   - Compares multiple strategies by varying trial counts or probabilities.
   - Supports dynamic parameter adjustments for comprehensive analysis.

4. **Tree I/O**
   - **Load Tree**: Parses a decision tree from a file.
   - **Save Tree**: Exports a decision tree to a file.

---

### **Key Functions**

#### 1. **show_recursive**
**Description**: Prints the tree structure with recursion to reflect hierarchical levels.
- **Features**:
  - Indents nodes based on depth.
  - Displays node type, ancestors, and attributes.
- **Usage**:
```python
show_recursive(tree)
```

#### 2. **solve_recursive**
**Description**: Uses backward induction to compute the optimal strategy.
- **Features**:
  - Terminal nodes return payoffs.
  - Decision nodes select the maximum subvalue among descendants.
  - Nature nodes compute expected values based on probabilities.
- **Usage**:
```python
solve_recursive(tree)
```

#### 3. **play_recursive**
**Description**: Simulates the tree's traversal based on a given strategy.
- **Features**:
  - Supports decision, nature, and terminal nodes.
  - Randomly selects paths for nature nodes based on probabilities.
- **Usage**:
```python
play_recursive(tree, strategy)
```

#### 4. **simulate_recursive**
**Description**: Simulates multiple plays of the tree for a given strategy.
- **Features**:
  - Recursively executes `play_recursive` for a defined number of trials.
- **Usage**:
```python
simulate_recursive(strategy, tree, trials=20)
```

#### 5. **monte_carlo**
**Description**: Runs a Monte Carlo simulation to compare strategies.
- **Features**:
  - Varies the number of trials or probabilities.
  - Outputs results for each scenario.
- **Usage**:
```python
monte_carlo(first_strategy, second_strategy, tree, start=10, increment=10)
```

---

### **File Structure**

#### **Tree File Format**
- A decision tree is stored as a text file with comma-separated values.
- Each node is represented with its attributes:
```
node,0
name,decide
type,d
length,2
descendant,1
descendant,2
node,1
name,sure_thing
type,t
pay,50.0
...
```
- Nodes appear sequentially, with attributes like `type`, `descendants`, `pay`, and `probabilities` defined.

#### **Loading and Saving Trees**
- **Load Tree**:
```python
tree = load_tree("filename.txt")
```
- **Save Tree**:
```python
save_tree(tree, "filename.txt")
```

---

### **How to Run the Project**


   
1. **Run the Main Program**
   Execute the program to access the interactive menu:
```bash
python decision_tree_project.py
```

2. **Interactive Menu Options**
   - Load a tree file.
   - Display the tree structure.
   - Solve the tree for optimal strategies.
   - Simulate a strategy.
   - Run Monte Carlo simulations.
   - Save the tree to a file.

---

### **Example Workflow**

1. **Load a Tree**:
   ```python
   tree = load_tree("big_tree.txt")
   ```

2. **Display the Tree**:
   ```python
   show_recursive(tree)
   ```

3. **Solve for Optimal Strategy**:
   ```python
   solve_recursive(tree)
   ```

4. **Simulate a Strategy**:
   ```python
   strategy = [0] * len(tree)  # Example strategy
   results = simulate_recursive(strategy, tree)
   ```

5. **Run Monte Carlo Analysis**:
   ```python
   monte_carlo(strategy_one, strategy_two, tree, start=10, increment=5)
   ```
