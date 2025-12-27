#!/usr/bin/env python3
"""
Example usage of the HouseDesigner class
This script demonstrates how to create custom houses with different dimensions
"""

import sys
import os

# Add current directory to path to import house_designer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from house_designer import HouseDesigner
except ImportError:
    print("Error: Could not import house_designer module")
    print("Make sure house_designer.py is in the same directory")
    sys.exit(1)


def create_small_house():
    """Create a small house (6m x 8m)"""
    print("\n" + "=" * 60)
    print("Creating Small House (6m x 8m)")
    print("=" * 60)
    
    designer = HouseDesigner(doc_name="SmallHouse")
    designer.house_length = 8000   # 8 meters
    designer.house_width = 6000    # 6 meters
    designer.wall_height = 2800    # 2.8 meters
    
    doc = designer.build_house()
    
    try:
        designer.save_design("small_house.FCStd")
    except Exception as e:
        print(f"Warning: Could not save file: {e}")
    
    return designer


def create_large_house():
    """Create a large house (12m x 15m)"""
    print("\n" + "=" * 60)
    print("Creating Large House (12m x 15m)")
    print("=" * 60)
    
    designer = HouseDesigner(doc_name="LargeHouse")
    designer.house_length = 15000  # 15 meters
    designer.house_width = 12000   # 12 meters
    designer.wall_height = 3500    # 3.5 meters
    designer.window_width = 1500   # Larger windows
    designer.window_height = 1800
    
    doc = designer.build_house()
    
    try:
        designer.save_design("large_house.FCStd")
    except Exception as e:
        print(f"Warning: Could not save file: {e}")
    
    return designer


def create_tall_house():
    """Create a tall narrow house (5m x 10m)"""
    print("\n" + "=" * 60)
    print("Creating Tall House (5m x 10m)")
    print("=" * 60)
    
    designer = HouseDesigner(doc_name="TallHouse")
    designer.house_length = 10000  # 10 meters
    designer.house_width = 5000    # 5 meters
    designer.wall_height = 4000    # 4 meters (tall)
    designer.wall_thickness = 250  # Thicker walls
    
    doc = designer.build_house()
    
    try:
        designer.save_design("tall_house.FCStd")
    except Exception as e:
        print(f"Warning: Could not save file: {e}")
    
    return designer


def main():
    """Main function to demonstrate different house designs"""
    print("\n" + "=" * 60)
    print("FreeCAD House Designer - Examples")
    print("=" * 60)
    print("\nThis script creates three different house designs:")
    print("1. Small House (6m x 8m)")
    print("2. Large House (12m x 15m)")
    print("3. Tall House (5m x 10m)")
    print("\nSelect which house to create:")
    print("  1 - Small House")
    print("  2 - Large House")
    print("  3 - Tall House")
    print("  4 - All houses")
    print("  0 - Exit")
    
    # When running in FreeCAD without interactive input, create all houses
    try:
        choice = input("\nEnter your choice (0-4): ").strip()
    except EOFError:
        # No interactive input available, create all
        choice = "4"
    
    if choice == "1":
        create_small_house()
    elif choice == "2":
        create_large_house()
    elif choice == "3":
        create_tall_house()
    elif choice == "4":
        create_small_house()
        create_large_house()
        create_tall_house()
    elif choice == "0":
        print("Exiting...")
        return
    else:
        print(f"Invalid choice: {choice}")
        return
    
    print("\n" + "=" * 60)
    print("Example houses created successfully!")
    print("Open the .FCStd files in FreeCAD to view them.")
    print("=" * 60)


if __name__ == "__main__":
    main()
