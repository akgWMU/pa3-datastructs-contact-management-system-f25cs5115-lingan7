#!/usr/bin/env python3
"""
Additional Analysis - Lingamuthu Kalyanasundaram
CS-5115-100 - Programming Prep for Grad Stu
Extended analysis beyond the basic requirements
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from contact_manager import *

def load_and_analyze_results():
    """Load performance results and conduct additional statistical analysis."""
    
    # Load the generated CSV results
    df = pd.read_csv('performance_results.csv')
    
    print("=== EXTENDED STATISTICAL ANALYSIS ===")
    print("\n1. Performance Growth Rates:")
    
    # Calculate growth rates between dataset sizes
    structures = df['Structure'].unique()
    operations = ['Insert_Time_ms', 'Search_Time_ms', 'Update_Time_ms', 'Delete_Time_ms']
    
    growth_analysis = {}
    
    for structure in structures:
        struct_data = df[df['Structure'] == structure].sort_values('Size')
        growth_analysis[structure] = {}
        
        for op in operations:
            times = struct_data[op].values
            sizes = struct_data['Size'].values
            
            # Calculate growth factor between largest and smallest dataset
            if len(times) >= 2 and times[0] > 0:
                growth_factor = times[-1] / times[0]  # 10K vs 100 contacts
                size_factor = sizes[-1] / sizes[0]    # 100x size increase
                
                # Calculate complexity approximation
                if growth_factor <= size_factor ** 0.1:  # Nearly constant
                    complexity = "O(1)"
                elif growth_factor <= size_factor ** 0.5:  # Sub-linear
                    complexity = f"O(log n) - factor {growth_factor:.1f}"
                elif growth_factor <= size_factor * 1.2:  # Linear
                    complexity = f"O(n) - factor {growth_factor:.1f}"
                else:  # Super-linear
                    complexity = f"O(n²) or worse - factor {growth_factor:.1f}"
                
                growth_analysis[structure][op] = {
                    'growth_factor': growth_factor,
                    'estimated_complexity': complexity
                }
    
    # Display growth analysis
    for structure, ops in growth_analysis.items():
        print(f"\n{structure}:")
        for op, data in ops.items():
            op_name = op.replace('_Time_ms', '').replace('_', ' ').title()
            print(f"  {op_name:12}: {data['estimated_complexity']}")
    
    return df, growth_analysis

def memory_usage_analysis():
    """Analyze theoretical memory usage for different structures."""
    
    print("\n=== MEMORY USAGE ANALYSIS ===")
    
    contact_base_size = 200  # Estimated bytes per contact (strings + object overhead)
    
    memory_analysis = {
        'Array': {
            'per_contact': contact_base_size + 8,  # 8 bytes for pointer
            'overhead': 64,  # List object overhead
            'description': 'Contiguous storage, minimal overhead'
        },
        'LinkedList': {
            'per_contact': contact_base_size + 16,  # 8 bytes for next pointer + 8 for node
            'overhead': 32,  # Head pointer
            'description': 'Node overhead, scattered memory'
        },
        'HashMap': {
            'per_contact': contact_base_size + 24,  # Key + value + hash overhead
            'overhead': 256,  # Initial hash table
            'description': 'Hash table overhead, load factor ~0.75'
        },
        'BST': {
            'per_contact': contact_base_size + 24,  # Left + right pointers + node
            'overhead': 32,  # Root pointer
            'description': 'Binary tree structure, balanced depth'
        }
    }
    
    sizes = [100, 1000, 5000, 10000]
    
    print("\nEstimated Memory Usage (MB):")
    print("Size".ljust(8), end="")
    for structure in memory_analysis:
        print(structure.ljust(12), end="")
    print()
    
    for size in sizes:
        print(f"{size:<8}", end="")
        for structure, data in memory_analysis.items():
            total_bytes = (data['per_contact'] * size) + data['overhead']
            if structure == 'HashMap':
                total_bytes *= 1.33  # Load factor overhead
            total_mb = total_bytes / (1024 * 1024)
            print(f"{total_mb:.2f}MB".ljust(12), end="")
        print()

def create_advanced_visualizations(df):
    """Create additional visualizations for deeper analysis."""
    
    plt.style.use('seaborn-v0_8')
    
    # 1. Logarithmic scaling analysis
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Advanced Performance Analysis - Logarithmic Scaling', fontsize=16)
    
    operations = ['Search_Time_ms', 'Insert_Time_ms', 'Update_Time_ms', 'Delete_Time_ms']
    titles = ['Search Times (Log Scale)', 'Insert Times', 'Update Times (Log Scale)', 'Delete Times (Log Scale)']
    log_scales = [True, False, True, True]
    
    for i, (op, title, use_log) in enumerate(zip(operations, titles, log_scales)):
        ax = axes[i // 2, i % 2]
        
        for structure in df['Structure'].unique():
            struct_data = df[df['Structure'] == structure]
            ax.plot(struct_data['Size'], struct_data[op], 
                   marker='o', label=structure, linewidth=2, markersize=6)
        
        ax.set_xlabel('Dataset Size')
        ax.set_ylabel('Time (ms)')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        if use_log:
            ax.set_yscale('log')
        
        # Add theoretical complexity lines for comparison
        sizes = np.array([100, 1000, 5000, 10000])
        if op == 'Search_Time_ms':
            # O(1) line for hash map comparison
            ax.axhline(y=0.001, color='red', linestyle='--', alpha=0.5, label='O(1) ideal')
            # O(log n) line
            log_line = 0.0001 * np.log2(sizes / 100)
            ax.plot(sizes, log_line, 'g--', alpha=0.5, label='O(log n) ideal')
    
    plt.tight_layout()
    plt.savefig('advanced_performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Performance efficiency comparison
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Calculate efficiency score (lower time = higher efficiency)
    efficiency_data = []
    for _, row in df.iterrows():
        # Weighted efficiency score (search and update are most common operations)
        efficiency = (
            1/row['Search_Time_ms'] * 0.4 +      # 40% weight on search
            1/row['Update_Time_ms'] * 0.3 +      # 30% weight on update  
            1/row['Insert_Time_ms'] * 0.2 +      # 20% weight on insert
            1/row['Delete_Time_ms'] * 0.1        # 10% weight on delete
        )
        efficiency_data.append({
            'Structure': row['Structure'],
            'Size': row['Size'],
            'Efficiency_Score': efficiency
        })
    
    eff_df = pd.DataFrame(efficiency_data)
    
    # Create efficiency heatmap
    pivot_eff = eff_df.pivot_table(values='Efficiency_Score', 
                                  index='Structure', 
                                  columns='Size', 
                                  aggfunc='mean')
    
    sns.heatmap(pivot_eff, annot=True, fmt='.0f', cmap='viridis', 
                cbar_kws={'label': 'Efficiency Score (Higher = Better)'})
    plt.title('Overall Efficiency Comparison\n(Weighted by Common Operation Frequency)')
    plt.ylabel('Data Structure')
    plt.xlabel('Dataset Size')
    plt.tight_layout()
    plt.savefig('efficiency_heatmap.png', dpi=300, bbox_inches='tight')
    plt.show()

def statistical_significance_test(df):
    """Perform statistical tests on performance differences."""
    
    print("\n=== STATISTICAL SIGNIFICANCE TESTS ===")
    
    # Compare HashMap vs BST for search operations (most critical)
    hash_search = df[(df['Structure'] == 'HashMap') & (df['Size'] == 10000)]['Search_Time_ms'].iloc[0]
    bst_search = df[(df['Structure'] == 'BST') & (df['Size'] == 10000)]['Search_Time_ms'].iloc[0]
    
    # Since we have spreads, we can estimate confidence intervals
    hash_spread = df[(df['Structure'] == 'HashMap') & (df['Size'] == 10000)]['Search_Spread'].iloc[0]
    bst_spread = df[(df['Structure'] == 'BST') & (df['Size'] == 10000)]['Search_Spread'].iloc[0]
    
    print(f"\nSearch Performance at 10K contacts:")
    print(f"HashMap: {hash_search:.6f}ms ± {hash_spread:.6f}ms")
    print(f"BST:     {bst_search:.6f}ms ± {bst_spread:.6f}ms")
    print(f"HashMap is {bst_search/hash_search:.1f}x faster than BST")
    
    # Calculate effect size (Cohen's d approximation)
    pooled_std = np.sqrt((hash_spread**2 + bst_spread**2) / 2)
    if pooled_std > 0:
        cohens_d = abs(hash_search - bst_search) / pooled_std
        print(f"Effect size (Cohen's d): {cohens_d:.2f}")
        
        if cohens_d > 2.0:
            print("Effect: Very Large (highly significant difference)")
        elif cohens_d > 1.0:
            print("Effect: Large (significant difference)")
        elif cohens_d > 0.5:
            print("Effect: Medium (moderate difference)")
        else:
            print("Effect: Small (minimal practical difference)")

def practical_recommendations():
    """Generate practical recommendations based on analysis."""
    
    print("\n=== PRACTICAL RECOMMENDATIONS ===")
    
    scenarios = {
        "Mobile Contact App": {
            "typical_size": "500-2000 contacts",
            "operations": "Frequent search, occasional updates",
            "constraints": "Memory limited, battery conscious",
            "recommendation": "HashMap",
            "reasoning": "Instant search response, acceptable memory overhead for mobile use"
        },
        
        "Enterprise CRM": {
            "typical_size": "10,000-100,000 contacts", 
            "operations": "Heavy search/update, bulk imports",
            "constraints": "Performance critical, concurrent access",
            "recommendation": "HashMap with BST backup",
            "reasoning": "HashMap for primary operations, BST for sorted views and range queries"
        },
        
        "Email Auto-complete": {
            "typical_size": "1,000-5,000 contacts",
            "operations": "Prefix searching, real-time suggestions",
            "constraints": "Sub-millisecond response time",
            "recommendation": "HashMap + Trie hybrid",
            "reasoning": "HashMap for exact matches, Trie for prefix matching"
        },
        
        "IoT Device Directory": {
            "typical_size": "100-1,000 devices",
            "operations": "Infrequent updates, status monitoring", 
            "constraints": "Memory constrained, simple implementation",
            "recommendation": "Array or BST",
            "reasoning": "Simple implementation, predictable memory usage, good enough performance"
        }
    }
    
    for scenario, details in scenarios.items():
        print(f"\n{scenario}:")
        print(f"  Typical Size: {details['typical_size']}")
        print(f"  Usage Pattern: {details['operations']}")
        print(f"  Constraints: {details['constraints']}")
        print(f"  Recommendation: {details['recommendation']}")
        print(f"  Reasoning: {details['reasoning']}")

def main():
    """Run extended analysis."""
    print("Contact Management System - Extended Analysis")
    print("=" * 60)
    print("Student: Lingamuthu Kalyanasundaram")
    print("Date: September 24, 2025")
    print("=" * 60)
    
    # Load and analyze results
    df, growth_analysis = load_and_analyze_results()
    
    # Memory analysis
    memory_usage_analysis()
    
    # Statistical analysis
    statistical_significance_test(df)
    
    # Advanced visualizations
    create_advanced_visualizations(df)
    
    # Practical recommendations
    practical_recommendations()
    
    print("\n" + "=" * 60)
    print("Extended analysis complete!")
    print("Generated files:")
    print("- advanced_performance_analysis.png")
    print("- efficiency_heatmap.png")
    print("=" * 60)

if __name__ == "__main__":
    main()
