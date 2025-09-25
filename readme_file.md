# Contact Management System - Data Structure Performance Comparison

## 📋 Assignment Overview

This project implements and compares the performance of four different data structures in the context of a contact management system:

1. **Array-based List** - Dynamic array implementation
2. **Singly Linked List** - Node-based linked structure
3. **Hash Map** - Dictionary-based key-value storage
4. **Binary Search Tree (BST)** - Tree-based sorted structure

## 🎯 Learning Objectives

- Understand the trade-offs between different data structures
- Analyze theoretical vs. empirical time complexity
- Learn to benchmark and profile code performance
- Practice implementing fundamental data structures
- Gain experience with real-world performance testing

## 🏗️ Project Structure

```
contact-management-system/
├── contact_manager.py          # Main implementation file
├── README.md                   # This documentation
├── requirements.txt            # Python dependencies
├── performance_results.csv     # Generated test results
├── performance_comparison.png  # Generated visualizations
└── report_template.md         # Template for your analysis report
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd contact-management-system
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the complete performance analysis:
```bash
python contact_manager.py
```

## 📊 Features

### Data Structures Implemented

| Data Structure | Insert | Search | Delete | Update | Space |
|---------------|--------|---------|--------|--------|-------|
| Array         | O(1)*  | O(n)    | O(n)   | O(n)   | O(n)  |
| Linked List   | O(1)   | O(n)    | O(n)   | O(n)   | O(n)  |
| Hash Map      | O(1)*  | O(1)*   | O(1)*  | O(1)*  | O(n)  |
| BST           | O(log n)*| O(log n)*| O(log n)*| O(log n)*| O(n) |

*Average case; worst case may differ

### Operations Tested

- **Insert**: Adding new contacts to the system
- **Search**: Finding contacts by name
- **Update**: Modifying contact information (phone/email)
- **Delete**: Removing contacts from the system

### Performance Metrics

- **Execution Time**: Measured in milliseconds with high precision
- **Scalability**: Tested with datasets of 100, 1K, 5K, and 10K contacts
- **Statistical Analysis**: Multiple trials with mean and spread calculations
- **Memory Efficiency**: Implicit through data structure design

## 🧪 Running Tests

### Complete Performance Analysis
```bash
python contact_manager.py
```

This will:
- Generate synthetic contact data
- Test all operations on all data structures
- Create performance visualizations
- Save results to CSV file
- Display comprehensive analysis report

### Basic Operations Demo
```python
# Add this to the end of contact_manager.py and uncomment
demo_basic_operations()
```

## 📈 Expected Results

Based on theoretical analysis, you should observe:

1. **Hash Map** excels at all operations with O(1) average performance
2. **BST** provides balanced performance with O(log n) operations
3. **Array** is efficient for insertions but slow for searches/deletions
4. **Linked List** is fast for insertions but slow for other operations

## 📝 Assignment Deliverables

### 1. Code Implementation ✅
- Complete implementation of all four data structures
- Proper error handling and edge case management
- Clean, well-documented code with type hints

### 2. Performance Analysis 📊
- Run performance tests with provided datasets
- Generate and analyze visualization graphs
- Document empirical results vs. theoretical expectations

### 3. Written Report 📄
Use the provided `report_template.md` to write a 2-3 page analysis covering:
- Design decisions and implementation details
- Performance comparison and analysis
- Real-world application implications
- Conclusions and recommendations

### 4. Visualizations 📈
- Performance comparison graphs (automatically generated)
- Analysis of scaling behavior
- Identification of performance bottlenecks

## 🔧 Customization Options

### Adding More Data Structures
You can extend the comparison by implementing additional structures:

```python
# Example: Add a Trie for prefix-based searching
class TrieContacts(ContactManager):
    # Implementation here
    pass

# Add to structures dictionary in PerformanceTester
self.structures['Trie'] = TrieContacts
```

### Modifying Test Parameters
Adjust test parameters in the `main()` function:

```python
# Change data sizes
data_sizes = [50, 500, 2500, 15000]

# Modify number of trials for more/less precision
tester.test_operations(data_sizes, trials=5)
```

### Custom Contact Fields
Extend the Contact class for more complex scenarios:

```python
class ExtendedContact(Contact):
    def __init__(self, name, phone, email, address=None, company=None):
        super().__init__(name, phone, email)
        self.address = address
        self.company = company
```

## 🎨 Visualization Features

The program automatically generates:
- Line plots showing performance scaling
- Logarithmic scaling for operations with wide performance ranges
- Error bars showing measurement uncertainty
- Professional styling with clear legends and labels

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Memory Issues**: Reduce dataset sizes for testing on limited systems
   ```python
   data_sizes = [100, 500, 1000]  # Smaller sizes
   ```

3. **Slow Performance**: Reduce number of trials
   ```python
   tester.test_operations(data_sizes, trials=1)
   ```

### Performance Notes

- BST performance depends on insertion order (can degrade to O(n) in worst case)
- Hash map performance assumes good hash function and load factor
- Large datasets may require significant memory and processing time

## 📚 Additional Resources

- [Big O Notation Explained](https://www.bigocheatsheet.com/)
- [Python Data Structures Documentation](https://docs.python.org/3/tutorial/datastructures.html)
- [Time Complexity Analysis](https://en.wikipedia.org/wiki/Time_complexity)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

## 🤝 Contributing

This is an educational project. Focus on:
- Understanding the implementations
- Analyzing the results
- Drawing meaningful conclusions
- Writing clear, professional reports

