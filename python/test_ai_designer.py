#!/usr/bin/env python3
"""
Test script for AI House Designer
Tests the AI parser and floor plan generator functionality
"""

import sys
from ai_house_parser import AIHouseParser
from floor_plan_generator import FloorPlanGenerator


def test_parser():
    """Test the AI house parser"""
    print("\n" + "=" * 70)
    print("TEST 1: AI House Parser")
    print("=" * 70)
    
    parser = AIHouseParser()
    
    # Test cases
    test_cases = [
        {
            'description': "3000 sqft Ranch style house, 4 bedrooms, 4 bathrooms. Jack and Jill bathroom. Gameroom. 3 car garage. Attic man den.",
            'expected': {
                'sqft': 3000,
                'style': 'Ranch',
                'bedrooms': 4,
                'bathrooms': 4.0,
                'garage': 3,
            }
        },
        {
            'description': "2500 sq ft Colonial, 3 bed, 2.5 bath, 2 car garage, office, mudroom",
            'expected': {
                'sqft': 2500,
                'style': 'Colonial',
                'bedrooms': 3,
                'bathrooms': 2.5,
                'garage': 2,
            }
        },
        {
            'description': "Modern 1800 sqft home with 5 bedrooms, 3 bathrooms, 2 car garage",
            'expected': {
                'sqft': 1800,
                'style': 'Modern',
                'bedrooms': 5,
                'bathrooms': 3.0,
                'garage': 2,
            }
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest case {i}:")
        print(f"  Input: {test['description']}")
        
        requirements = parser.parse(test['description'])
        expected = test['expected']
        
        # Check each expected value
        checks = [
            ('Square footage', requirements.total_sqft, expected['sqft']),
            ('Style', requirements.style, expected['style']),
            ('Bedrooms', requirements.bedrooms, expected['bedrooms']),
            ('Bathrooms', requirements.bathrooms, expected['bathrooms']),
            ('Garage', requirements.garage_cars, expected['garage']),
        ]
        
        test_passed = True
        for name, actual, expected_val in checks:
            if actual == expected_val:
                print(f"  ✓ {name}: {actual}")
            else:
                print(f"  ✗ {name}: Expected {expected_val}, got {actual}")
                test_passed = False
        
        if test_passed:
            passed += 1
            print("  PASSED")
        else:
            failed += 1
            print("  FAILED")
    
    print(f"\n{'-' * 70}")
    print(f"Parser Tests: {passed} passed, {failed} failed")
    return failed == 0


def test_floor_plan_generator():
    """Test the floor plan generator"""
    print("\n" + "=" * 70)
    print("TEST 2: Floor Plan Generator")
    print("=" * 70)
    
    parser = AIHouseParser()
    
    # Test case
    description = "3000 sqft Ranch, 4 bedrooms, 4 bathrooms, gameroom, 3 car garage"
    print(f"\nTest: {description}")
    
    requirements = parser.parse(description)
    generator = FloorPlanGenerator(requirements)
    rooms = generator.generate_floor_plan()
    
    # Verify room generation
    checks = [
        ('Total rooms created', len(rooms) > 0, True),
        ('Has master bedroom', any(r.room_type == 'master_bedroom' for r in rooms), True),
        ('Has kitchen', any(r.room_type == 'kitchen' for r in rooms), True),
        ('Has living room', any(r.room_type == 'living_room' for r in rooms), True),
        ('Has garage', any(r.room_type == 'garage' for r in rooms), True),
        ('Has gameroom', any(r.room_type == 'gameroom' for r in rooms), True),
        ('Correct bedroom count', sum(1 for r in rooms if 'bedroom' in r.room_type), requirements.bedrooms),
    ]
    
    passed = True
    for name, actual, expected in checks:
        if actual == expected:
            print(f"  ✓ {name}: {actual}")
        else:
            print(f"  ✗ {name}: Expected {expected}, got {actual}")
            passed = False
    
    # Print summary
    total_sqft = sum(r.sqft for r in rooms)
    print(f"\n  Generated {len(rooms)} rooms")
    print(f"  Total area: {total_sqft:.0f} sq ft")
    
    # List rooms
    print("\n  Room list:")
    for room in rooms:
        print(f"    - {room.name}: {room.sqft:.0f} sq ft ({room.width/1000:.1f}m x {room.length/1000:.1f}m)")
    
    print(f"\n{'-' * 70}")
    if passed:
        print("Floor Plan Generator Test: PASSED")
    else:
        print("Floor Plan Generator Test: FAILED")
    
    return passed


def test_ai_house_designer_without_freecad():
    """Test AI house designer without FreeCAD"""
    print("\n" + "=" * 70)
    print("TEST 3: AI House Designer (without FreeCAD)")
    print("=" * 70)
    
    from ai_house_designer import AIHouseDesigner
    
    designer = AIHouseDesigner()
    description = "2000 sqft Ranch, 3 bed, 2 bath, 2 car garage"
    
    print(f"\nTest: {description}")
    
    try:
        requirements, rooms, doc = designer.design_from_description(description)
        
        # Verify results
        checks = [
            ('Requirements generated', requirements is not None, True),
            ('Rooms generated', rooms is not None and len(rooms) > 0, True),
            ('Has correct style', requirements.style, 'Ranch'),
            ('Has correct sqft', requirements.total_sqft, 2000),
        ]
        
        passed = True
        print("\nVerification:")
        for name, actual, expected in checks:
            if actual == expected:
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name}: Expected {expected}, got {actual}")
                passed = False
        
        # Try to export summary
        try:
            summary_file = designer.export_summary("test_house_summary.txt")
            print(f"  ✓ Summary exported to: {summary_file}")
        except Exception as e:
            print(f"  ✗ Failed to export summary: {e}")
            passed = False
        
        print(f"\n{'-' * 70}")
        if passed:
            print("AI House Designer Test: PASSED")
        else:
            print("AI House Designer Test: FAILED")
        
        return passed
        
    except Exception as e:
        print(f"\n  ✗ Error: {e}")
        print(f"\n{'-' * 70}")
        print("AI House Designer Test: FAILED")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("AI HOUSE DESIGNER TEST SUITE")
    print("=" * 70)
    
    results = []
    
    # Run tests
    results.append(('Parser', test_parser()))
    results.append(('Floor Plan Generator', test_floor_plan_generator()))
    results.append(('AI House Designer', test_ai_house_designer_without_freecad()))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {name:30} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\n{total_passed}/{total_tests} test suites passed")
    print("=" * 70)
    
    return all(passed for _, passed in results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
