# Contact Management System - Data Structure Performance Comparison
# Complete implementation with all data structures and performance testing

import time
import random
import string
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
import gc

# ==================== CONTACT CLASS ====================
class Contact:
    """Represents a contact with name, phone, and email."""
    
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email
    
    def __repr__(self):
        return f"Contact('{self.name}', '{self.phone}', '{self.email}')"
    
    def __str__(self):
        return f"{self.name} | {self.phone} | {self.email}"

# ==================== ABSTRACT BASE CLASS ====================
class ContactManager(ABC):
    """Abstract base class for all contact management implementations."""
    
    @abstractmethod
    def insert(self, contact: Contact) -> None:
        pass
    
    @abstractmethod
    def search(self, name: str) -> Optional[Contact]:
        pass
    
    @abstractmethod
    def delete(self, name: str) -> bool:
        pass
    
    @abstractmethod
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        pass
    
    @abstractmethod
    def size(self) -> int:
        pass

# ==================== ARRAY-BASED IMPLEMENTATION ====================
class ArrayContacts(ContactManager):
    """Array-based contact management system."""
    
    def __init__(self):
        self.contacts = []
    
    def insert(self, contact: Contact) -> None:
        """Insert a new contact. O(1) amortized time complexity."""
        self.contacts.append(contact)
    
    def search(self, name: str) -> Optional[Contact]:
        """Search for a contact by name. O(n) time complexity."""
        for contact in self.contacts:
            if contact.name == name:
                return contact
        return None
    
    def delete(self, name: str) -> bool:
        """Delete a contact by name. O(n) time complexity."""
        for i, contact in enumerate(self.contacts):
            if contact.name == name:
                self.contacts.pop(i)
                return True
        return False
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        """Update a contact's information. O(n) time complexity."""
        contact = self.search(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            return True
        return False
    
    def size(self) -> int:
        return len(self.contacts)

# ==================== LINKED LIST IMPLEMENTATION ====================
class ListNode:
    """Node for singly linked list."""
    
    def __init__(self, contact: Contact):
        self.contact = contact
        self.next = None

class LinkedListContacts(ContactManager):
    """Linked list-based contact management system."""
    
    def __init__(self):
        self.head = None
        self._size = 0
    
    def insert(self, contact: Contact) -> None:
        """Insert a new contact at the head. O(1) time complexity."""
        new_node = ListNode(contact)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def search(self, name: str) -> Optional[Contact]:
        """Search for a contact by name. O(n) time complexity."""
        current = self.head
        while current:
            if current.contact.name == name:
                return current.contact
            current = current.next
        return None
    
    def delete(self, name: str) -> bool:
        """Delete a contact by name. O(n) time complexity."""
        if not self.head:
            return False
        
        if self.head.contact.name == name:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.contact.name == name:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        """Update a contact's information. O(n) time complexity."""
        contact = self.search(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            return True
        return False
    
    def size(self) -> int:
        return self._size

# ==================== HASH MAP IMPLEMENTATION ====================
class HashMapContacts(ContactManager):
    """Hash map-based contact management system."""
    
    def __init__(self):
        self.contacts = {}
    
    def insert(self, contact: Contact) -> None:
        """Insert a new contact. O(1) average time complexity."""
        self.contacts[contact.name] = contact
    
    def search(self, name: str) -> Optional[Contact]:
        """Search for a contact by name. O(1) average time complexity."""
        return self.contacts.get(name)
    
    def delete(self, name: str) -> bool:
        """Delete a contact by name. O(1) average time complexity."""
        if name in self.contacts:
            del self.contacts[name]
            return True
        return False
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        """Update a contact's information. O(1) average time complexity."""
        contact = self.search(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            return True
        return False
    
    def size(self) -> int:
        return len(self.contacts)

# ==================== BINARY SEARCH TREE IMPLEMENTATION ====================
class BSTNode:
    """Node for binary search tree."""
    
    def __init__(self, contact: Contact):
        self.contact = contact
        self.left = None
        self.right = None

class BSTContacts(ContactManager):
    """Binary search tree-based contact management system."""
    
    def __init__(self):
        self.root = None
        self._size = 0
    
    def insert(self, contact: Contact) -> None:
        """Insert a new contact. O(log n) average, O(n) worst case."""
        def _insert(node, contact):
            if not node:
                return BSTNode(contact)
            
            if contact.name < node.contact.name:
                node.left = _insert(node.left, contact)
            else:
                node.right = _insert(node.right, contact)
            return node
        
        self.root = _insert(self.root, contact)
        self._size += 1
    
    def search(self, name: str) -> Optional[Contact]:
        """Search for a contact by name. O(log n) average, O(n) worst case."""
        def _search(node, name):
            if not node:
                return None
            
            if name == node.contact.name:
                return node.contact
            elif name < node.contact.name:
                return _search(node.left, name)
            else:
                return _search(node.right, name)
        
        return _search(self.root, name)
    
    def delete(self, name: str) -> bool:
        """Delete a contact by name. O(log n) average, O(n) worst case."""
        def _find_min(node):
            while node.left:
                node = node.left
            return node
        
        def _delete(node, name):
            if not node:
                return None, False
            
            deleted = False
            if name < node.contact.name:
                node.left, deleted = _delete(node.left, name)
            elif name > node.contact.name:
                node.right, deleted = _delete(node.right, name)
            else:
                deleted = True
                if not node.left:
                    return node.right, deleted
                elif not node.right:
                    return node.left, deleted
                
                # Node with two children
                temp = _find_min(node.right)
                node.contact = temp.contact
                node.right, _ = _delete(node.right, temp.contact.name)
            
            return node, deleted
        
        self.root, deleted = _delete(self.root, name)
        if deleted:
            self._size -= 1
        return deleted
    
    def update(self, name: str, phone: str = None, email: str = None) -> bool:
        """Update a contact's information. O(log n) average, O(n) worst case."""
        contact = self.search(name)
        if contact:
            if phone:
                contact.phone = phone
            if email:
                contact.email = email
            return True
        return False
    
    def size(self) -> int:
        return self._size

# ==================== UTILITY FUNCTIONS ====================
class DataGenerator:
    """Utility class for generating test data."""
    
    @staticmethod
    def random_name(length: int = 8) -> str:
        """Generate a random name."""
        return ''.join(random.choices(string.ascii_letters, k=length)).title()
    
    @staticmethod
    def random_phone() -> str:
        """Generate a random phone number."""
        return ''.join(random.choices(string.digits, k=10))
    
    @staticmethod
    def random_email(name: str) -> str:
        """Generate a random email based on name."""
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'example.com']
        return f"{name.lower()}@{random.choice(domains)}"
    
    @staticmethod
    def generate_contacts(n: int) -> List[Contact]:
        """Generate n random contacts."""
        contacts = []
        names_used = set()
        
        for _ in range(n):
            # Ensure unique names
            while True:
                name = DataGenerator.random_name()
                if name not in names_used:
                    names_used.add(name)
                    break
            
            phone = DataGenerator.random_phone()
            email = DataGenerator.random_email(name)
            contacts.append(Contact(name, phone, email))
        
        return contacts

# ==================== PERFORMANCE TESTING ====================
class PerformanceTester:
    """Class for testing and comparing performance of different data structures."""
    
    def __init__(self):
        self.results = []
        self.structures = {
            'Array': ArrayContacts,
            'LinkedList': LinkedListContacts,
            'HashMap': HashMapContacts,
            'BST': BSTContacts
        }
    
    def time_operation(self, operation_func, trials: int = 5) -> tuple:
        """Time an operation with multiple trials and return mean and spread."""
        times = []
        
        for _ in range(trials):
            gc.collect()  # Garbage collection for more accurate timing
            start_time = time.perf_counter_ns()
            operation_func()
            end_time = time.perf_counter_ns()
            times.append(end_time - start_time)
        
        mean_time = sum(times) / len(times)
        spread = (max(times) - min(times)) / 2
        
        return mean_time / 1_000_000, spread / 1_000_000  # Convert to milliseconds
    
    def test_operations(self, data_sizes: List[int], trials: int = 3):
        """Test all operations for all data structures with different data sizes."""
        print("Starting Performance Tests...")
        print("=" * 60)
        
        for size in data_sizes:
            print(f"\nTesting with {size:,} contacts:")
            print("-" * 40)
            
            # Generate test data
            contacts = DataGenerator.generate_contacts(size)
            search_names = [contact.name for contact in contacts[:min(100, size)]]
            
            for structure_name, structure_class in self.structures.items():
                print(f"Testing {structure_name}...")
                
                # Initialize structure
                structure = structure_class()
                
                # Test INSERT operations
                def insert_all():
                    nonlocal structure
                    structure = structure_class()  # Reset structure
                    for contact in contacts:
                        structure.insert(contact)
                
                insert_time, insert_spread = self.time_operation(insert_all, trials)
                
                # Prepare structure for other operations
                structure = structure_class()
                for contact in contacts:
                    structure.insert(contact)
                
                # Test SEARCH operations
                def search_operations():
                    for name in search_names:
                        structure.search(name)
                
                search_time, search_spread = self.time_operation(search_operations, trials)
                
                # Test UPDATE operations
                def update_operations():
                    for name in search_names[:10]:  # Test fewer updates
                        structure.update(name, phone="1234567890", email="updated@test.com")
                
                update_time, update_spread = self.time_operation(update_operations, trials)
                
                # Test DELETE operations
                def delete_operations():
                    for name in search_names[:10]:  # Test fewer deletions
                        structure.delete(name)
                
                delete_time, delete_spread = self.time_operation(delete_operations, trials)
                
                # Store results
                result = {
                    'Structure': structure_name,
                    'Size': size,
                    'Insert_Time_ms': insert_time,
                    'Insert_Spread': insert_spread,
                    'Search_Time_ms': search_time / len(search_names),  # Average per search
                    'Search_Spread': search_spread / len(search_names),
                    'Update_Time_ms': update_time / 10,  # Average per update
                    'Update_Spread': update_spread / 10,
                    'Delete_Time_ms': delete_time / 10,  # Average per delete
                    'Delete_Spread': delete_spread / 10
                }
                
                self.results.append(result)
                
                print(f"  Insert: {insert_time:.3f}ms ±{insert_spread:.3f}ms")
                print(f"  Search (avg): {result['Search_Time_ms']:.6f}ms ±{result['Search_Spread']:.6f}ms")
                print(f"  Update (avg): {result['Update_Time_ms']:.3f}ms ±{result['Update_Spread']:.3f}ms")
                print(f"  Delete (avg): {result['Delete_Time_ms']:.3f}ms ±{result['Delete_Spread']:.3f}ms")
    
    def generate_report(self):
        """Generate performance analysis report."""
        if not self.results:
            print("No results to report. Run tests first.")
            return
        
        df = pd.DataFrame(self.results)
        
        print("\n" + "=" * 80)
        print("PERFORMANCE ANALYSIS REPORT")
        print("=" * 80)
        
        print("\n1. INSERTION PERFORMANCE")
        print("-" * 40)
        insert_pivot = df.pivot_table(
            values='Insert_Time_ms', 
            index='Size', 
            columns='Structure', 
            aggfunc='mean'
        )
        print(insert_pivot.round(3))
        
        print("\n2. SEARCH PERFORMANCE (Average per search)")
        print("-" * 50)
        search_pivot = df.pivot_table(
            values='Search_Time_ms', 
            index='Size', 
            columns='Structure', 
            aggfunc='mean'
        )
        print(search_pivot.round(6))
        
        print("\n3. ANALYSIS SUMMARY")
        print("-" * 30)
        
        # Find best performer for each operation at largest size
        largest_size = df['Size'].max()
        largest_df = df[df['Size'] == largest_size]
        
        best_insert = largest_df.loc[largest_df['Insert_Time_ms'].idxmin(), 'Structure']
        best_search = largest_df.loc[largest_df['Search_Time_ms'].idxmin(), 'Structure']
        best_update = largest_df.loc[largest_df['Update_Time_ms'].idxmin(), 'Structure']
        best_delete = largest_df.loc[largest_df['Delete_Time_ms'].idxmin(), 'Structure']
        
        print(f"Best for Insert: {best_insert}")
        print(f"Best for Search: {best_search}")
        print(f"Best for Update: {best_update}")
        print(f"Best for Delete: {best_delete}")
        
        return df
    
    def create_visualizations(self, df: pd.DataFrame):
        """Create performance visualization graphs."""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Data Structure Performance Comparison', fontsize=16, fontweight='bold')
        
        operations = ['Insert_Time_ms', 'Search_Time_ms', 'Update_Time_ms', 'Delete_Time_ms']
        titles = ['Insert Performance', 'Search Performance', 'Update Performance', 'Delete Performance']
        
        for i, (operation, title) in enumerate(zip(operations, titles)):
            ax = axes[i // 2, i % 2]
            
            for structure in df['Structure'].unique():
                structure_data = df[df['Structure'] == structure]
                ax.plot(structure_data['Size'], structure_data[operation], 
                       marker='o', label=structure, linewidth=2)
            
            ax.set_xlabel('Dataset Size')
            ax.set_ylabel('Time (ms)')
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            if operation == 'Search_Time_ms':
                ax.set_yscale('log')  # Log scale for search times
        
        plt.tight_layout()
        plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()

# ==================== MAIN EXECUTION ====================
def main():
    """Main function to run the complete performance comparison."""
    print("Contact Management System Performance Comparison")
    print("=" * 60)
    
    # Test with different data sizes
    data_sizes = [100, 1000, 5000, 10000]
    
    # Initialize and run performance tests
    tester = PerformanceTester()
    tester.test_operations(data_sizes, trials=3)
    
    # Generate report and visualizations
    df = tester.generate_report()
    
    if df is not None:
        tester.create_visualizations(df)
        
        # Save results to CSV
        df.to_csv('performance_results.csv', index=False)
        print(f"\nResults saved to 'performance_results.csv'")
        print("Visualization saved as 'performance_comparison.png'")

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    # Run the complete analysis
    main()

# ==================== ADDITIONAL DEMO FUNCTIONS ====================
def demo_basic_operations():
    """Demonstrate basic operations with all data structures."""
    print("\nBasic Operations Demo")
    print("=" * 30)
    
    # Create sample contacts
    contacts = [
        Contact("Alice Johnson", "5551234567", "alice@email.com"),
        Contact("Bob Smith", "5559876543", "bob@email.com"),
        Contact("Charlie Brown", "5555555555", "charlie@email.com")
    ]
    
    structures = {
        'Array': ArrayContacts(),
        'LinkedList': LinkedListContacts(),
        'HashMap': HashMapContacts(),
        'BST': BSTContacts()
    }
    
    # Test each structure
    for name, structure in structures.items():
        print(f"\nTesting {name}:")
        
        # Insert contacts
        for contact in contacts:
            structure.insert(contact)
        print(f"  Inserted {len(contacts)} contacts")
        
        # Search for a contact
        found = structure.search("Bob Smith")
        print(f"  Search result: {found}")
        
        # Update a contact
        updated = structure.update("Alice Johnson", phone="5550000000")
        print(f"  Updated Alice's phone: {updated}")
        
        # Delete a contact
        deleted = structure.delete("Charlie Brown")
        print(f"  Deleted Charlie: {deleted}")
        
        print(f"  Final size: {structure.size()}")

# Uncomment to run demo
# demo_basic_operations()
