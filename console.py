#!/usr/bin/env python3
"""
AirBnB Clone Console - Command interpreter module
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


def split_curly_braces(e_arg):
    """
    Splits curly braces for update method dictionary attributes
    """
    curly_braces = re.search(r"\{(.*?)\}", e_arg)
    if curly_braces:
        id_part = shlex.split(e_arg[:curly_braces.span()[0]])
        obj_id = [i.strip(",") for i in id_part][0]
        str_data = curly_braces.group(1)
        try:
            arg_dict = ast.literal_eval("{" + str_data + "}")
        except Exception:
            print("** invalid dictionary format **")
            return None, None
        return obj_id, arg_dict
    else:
        commands = e_arg.split(",")
        if commands:
            obj_id = commands[0].strip('"\' ') if commands[0] else ""
            attr_name = commands[1].strip('"\' ') if len(commands) > 1 else ""
            attr_value = commands[2].strip('"\' ') if len(commands) > 2 else ""
            return f"{obj_id}", f"{attr_name} {attr_value}"


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class for AirBnB clone
    """
    prompt = "(hbnb) "
    valid_classes = [
        "BaseModel", "User", "Amenity",
        "Place", "Review", "State", "City"
    ]

    def emptyline(self):
        """Handles empty line input"""
        return False

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of specified class
        Usage: create <class_name>
        """
        commands = shlex.split(arg)
        if not commands:
            print("** class name missing **")
            return
        class_name = commands[0]
        if class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return
        new_instance = eval(class_name)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Shows string representation of an instance
        Usage: show <class_name> <id>
        """
        commands = shlex.split(arg)
        if not commands:
            print("** class name missing **")
            return
        if commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(commands) < 2:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = f"{commands[0]}.{commands[1]}"
        print(objects.get(key, "** no instance found **"))

    def do_destroy(self, arg):
        """Deletes an instance based on class name and id
        Usage: destroy <class_name> <id>
        """
        commands = shlex.split(arg)
        if not commands:
            print("** class name missing **")
            return
        if commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(commands) < 2:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = f"{commands[0]}.{commands[1]}"
        if key in objects:
            del objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of instances
        Usage: all or all <class_name>
        """
        objects = storage.all()
        commands = shlex.split(arg)
        if not commands:
            print([str(obj) for obj in objects.values()])
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            print([str(obj) for key, obj in objects.items()
                 if key.split('.')[0] == commands[0]])

    def do_count(self, arg):
        """Counts instances of a class
        Usage: <class_name>.count()
        """
        objects = storage.all()
        commands = shlex.split(arg)
        if not commands:
            print("** class name missing **")
            return
        if commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        count = sum(1 for obj in objects.values()
                   if obj.__class__.__name__ == commands[0])
        print(count)

    def do_update(self, arg):
        """Updates an instance with new attributes
        Usage: update <class> <id> <attr_name> "<attr_value>"
               <class>.update(<id>, <attr_name>, <attr_value>)
               <class>.update(<id>, <dictionary>)
        """
        commands = shlex.split(arg)
        if not commands:
            print("** class name missing **")
            return
        if commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(commands) < 2:
            print("** instance id missing **")
            return
        objects = storage.all()
        key = f"{commands[0]}.{commands[1]}"
        if key not in objects:
            print("** no instance found **")
            return
        if len(commands) < 3:
            print("** attribute name missing **")
            return
        if len(commands) < 4 and '{' not in arg:
            print("** value missing **")
            return

        obj = objects[key]
        if '{' in arg:
            obj_id, arg_dict = split_curly_braces(arg)
            if arg_dict:
                for attr_name, attr_value in arg_dict.items():
                    setattr(obj, attr_name, attr_value)
                obj.save()
        else:
            attr_name = commands[2]
            attr_value = commands[3]
            try:
                attr_value = eval(attr_value)
            except Exception:
                pass
            setattr(obj, attr_name, attr_value)
            obj.save()

    def default(self, arg):
        """Handles alternative command syntax"""
        method_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.do_count
        }

        match = re.search(r"^(\w+)\.(\w+)\((.*?)\)$", arg)
        if not match:
            print("*** Unknown syntax: {}".format(arg))
            return False

        class_name, method, args = match.groups()
        if method not in method_dict:
            print("*** Unknown syntax: {}".format(arg))
            return False

        if method == "update":
            match_dict = re.search(r'^"([^"]+)"(?:,\s*(.*))?$', args.strip())
            if match_dict:
                obj_id = match_dict.group(1)
                rest = match_dict.group(2) or ""
                if '{' in rest:
                    obj_id = obj_id.strip('"\'')
                    call = f"{class_name} {obj_id} {rest}"
                else:
                    parts = [p.strip(' "\'') for p in rest.split(',')]
                    call = f"{class_name} {obj_id} {' '.join(parts)}"
            else:
                call = f"{class_name} {args}"
        else:
            call = f"{class_name} {args}"

        return method_dict[method](call)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
