**AirBnB Clone \- The Console**

This is a clone of the AirBnB app, focused on the backend part.    
It works like a command interpreter where we can create, update, delete, and show objects.  

**Project Description**

This project is about building the base of a full web app like AirBnB.    
We start with a command-line interface that manages objects using JSON file storage.

**How to Start It**

git clone [https://github.com/josep-prog/alu-AirBnB\_clone.git](https://github.com/josep-prog/alu-AirBnB_clone.git)

cd alu-AirBnB\_clone

**RUN THIS COMMAND**

python3 console.py

**How to Use It**

Once you're inside the console, you can use commands like:

create \<class\_name\> \- creates a new object

show \<class\_name\> \<id\> \- shows the object

destroy \<class\_name\> \<id\> \- deletes the object

all \- lists all objects

update \<class\_name\> \<id\> \<attr\_name\> "\<attr\_value\>" \- updates object

**Example :** 

$ create BaseModel  
$ show BaseModel 1234-1234-1234  
$ destroy BaseModel 1234-1234-1234  
$ all  
$ update BaseModel 1234-1234-1234 name "My\_Model"

**This is file structure .**

├── console.py  
├── models  
│   ├── amenity.py  
│   ├── base\_model.py  
│   ├── city.py  
│   ├── engine  
│   │   ├── file\_storage.py  
│   │   ├── \_\_init\_\_.py  
│   │   └── \_\_pycache\_\_  
│   │       ├── file\_storage.cpython-310.pyc  
│   │       └── \_\_init\_\_.cpython-310.pyc  
│   ├── \_\_init\_\_.py  
│   ├── place.py  
│   ├── \_\_pycache\_\_  
│   │   ├── amenity.cpython-310.pyc  
│   │   ├── base\_model.cpython-310.pyc  
│   │   ├── city.cpython-310.pyc  
│   │   ├── \_\_init\_\_.cpython-310.pyc  
│   │   ├── place.cpython-310.pyc  
│   │   ├── review.cpython-310.pyc  
│   │   ├── state.cpython-310.pyc  
│   │   └── user.cpython-310.pyc  
│   ├── review.py  
│   ├── state.py  
│   └── user.py  
└── tests  
    ├── \_\_init\_\_.py  
    ├── \_\_pycache\_\_  
    │   └── \_\_init\_\_.cpython-310.pyc  
    └── test\_model  
        ├── \_\_init\_\_.py  
        ├── \_\_pycache\_\_  
        │   ├── \_\_init\_\_.cpython-310.pyc  
        │   └── test\_base\_model.cpython-310.pyc  
        └── test\_base\_model.py

AUTHOR : Joseph Nishimwe  
Email: [j.nishimwe@alustudent.com](mailto:j.nishimwe@alustudent.com)

