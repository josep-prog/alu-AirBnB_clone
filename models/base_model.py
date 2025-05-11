#!/usr/bin/python3
"""
Defines the BaseModel class - the foundation for all AirBnB clone models
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Base class that defines all common attributes/methods for other classes
    
    Attributes:
        id (str): Unique identifier for each instance (UUID)
        created_at (datetime): When instance was created
        updated_at (datetime): When instance was last updated
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance
        
        Args:
            *args: Unused (reserved for future extensions)
            **kwargs: Dictionary of attribute key/value pairs for deserialization
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ("created_at", "updated_at"):
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            models.storage.new(self)

    def save(self):
        """
        Updates the updated_at timestamp and saves to storage
        """
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """
        Creates a dictionary representation of the instance for serialization
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """
        Returns the informal string representation of the instance
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


if __name__ == "__main__":
    # Test cases
    print("-- Create a new model --")
    my_model = BaseModel()
    my_model.name = "My_First_Model"
    my_model.my_number = 89
    print(my_model)
    
    print("-- Test save --")
    old_updated = my_model.updated_at
    my_model.save()
    print(f"Updated at changed from {old_updated} to {my_model.updated_at}")
    
    print("-- Test to_dict --")
    model_dict = my_model.to_dict()
    print(model_dict)
    print("Dictionary keys and types:")
    for key, value in model_dict.items():
        print(f"\t{key}: ({type(value).__name__}) - {value}")
    
    print("-- Create from dictionary --")
    new_model = BaseModel(**model_dict)
    print(new_model)
    print(f"Same model? {my_model.id == new_model.id}")
