#!/usr/bin/python3
"""
Defines the BaseModel class - the foundation for all AirBnB clone models
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    Base class that defines all common attributes/methods for other classes
    
    Attributes:
        id (str): Unique identifier for each instance
        created_at (datetime): When instance was created
        updated_at (datetime): When instance was last updated
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new BaseModel instance
        
        Args:
            *args: Unused
            **kwargs: Dictionary of attribute key/value pairs
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
            self.created_at = self.updated_at = datetime.utcnow()
            self.register_with_storage()

    def register_with_storage(self):
        """Registers new instance with storage system"""
        from models import storage
        storage.new(self)

    def save(self):
        """
        Updates the updated_at timestamp and saves to storage
        
        Note:
            This persists the object to the storage engine
        """
        self.updated_at = datetime.utcnow()
        self.persist_to_storage()

    def persist_to_storage(self):
        """Persists the object to storage"""
        from models import storage
        storage.save()

    def to_dict(self):
        """
        Creates a dictionary representation of the instance
        
        Returns:
            dict: Dictionary containing all instance attributes
        """
        obj_dict = self.__dict__.copy()
        obj_dict["__class__"] = self.__class__.__name__
        for time_attr in ["created_at", "updated_at"]:
            if time_attr in obj_dict:
                obj_dict[time_attr] = obj_dict[time_attr].isoformat()
        return obj_dict

    def __str__(self):
        """
        Returns the string representation of the instance
        
        Returns:
            str: Formatted string showing class name, id and attributes
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"


if __name__ == "__main__":
    # Test code
    my_model = BaseModel()
    my_model.name = "Test Model"
    my_model.number = 89
    print("Original model:")
    print(my_model)
    print("--")
    
    print("Dictionary representation:")
    model_dict = my_model.to_dict()
    print(model_dict)
    
    print("--")
    print("JSON of my_model:")
    for key, value in model_dict.items():
        print(f"\t{key}: ({type(value)}) - {value}")
    
    print("--")
    print("Testing save:")
    old_updated = my_model.updated_at
    my_model.save()
    print(f"Updated at changed from {old_updated} to {my_model.updated_at}")
