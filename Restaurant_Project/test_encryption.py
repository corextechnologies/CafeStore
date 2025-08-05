#!/usr/bin/env python
"""
Test script to verify encryption functionality
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restaurant_Project.settings')
django.setup()

from Base_App.models import Items, ItemList
from Base_App.encryption import encrypt_value, decrypt_value
from django.conf import settings

def test_encryption():
    """Test the encryption functionality"""
    print("Testing encryption functionality...")
    
    # Test basic encryption/decryption
    test_value = "Test Item Name"
    encrypted = encrypt_value(test_value)
    decrypted = decrypt_value(encrypted)
    
    print(f"Original: {test_value}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_value == decrypted}")
    
    # Test integer encryption
    test_int = 1500
    encrypted_int = encrypt_value(test_int)
    decrypted_int = decrypt_value(encrypted_int)
    
    print(f"\nInteger Original: {test_int}")
    print(f"Integer Encrypted: {encrypted_int}")
    print(f"Integer Decrypted: {decrypted_int}")
    print(f"Integer Match: {str(test_int) == decrypted_int}")
    
    # Test model field encryption
    print("\nTesting model field encryption...")
    
    # Create a test category
    try:
        category = ItemList.objects.create(Name="Test Category")
        print(f"Created category: {category.Name}")
        
        # Create a test item
        item = Items.objects.create(
            name="Test Item",
            description="This is a test item description",
            price=1500,
            Category=category
        )
        print(f"Created item: {item.name}")
        print(f"Item price: {item.price}")
        print(f"Item description: {item.description}")
        
        # Test retrieval
        retrieved_item = Items.objects.get(id=item.id)
        print(f"\nRetrieved item: {retrieved_item.name}")
        print(f"Retrieved price: {retrieved_item.price}")
        print(f"Retrieved description: {retrieved_item.description}")
        
        # Clean up
        item.delete()
        category.delete()
        print("\nTest data cleaned up successfully")
        
    except Exception as e:
        print(f"Error testing model encryption: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_encryption() 