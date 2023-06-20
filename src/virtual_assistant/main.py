import sys
from string import punctuation
import re

class AddingExistingUser(Exception):
    """exception class when trying to create an existing user."""

    def __str__(self) -> str:
        return "A user with this name already exists."
    

class InvalidPhoneNumber(Exception):
    """Exception raised for an invalid phone number format."""
    
    def __str__(self) -> str:
        return "Phone number format is incorrect."
    

class NonExistentUser(Exception):
    """Exception class when attempting to change a non-existent user."""
    
    def __str__(self) -> str:
        return "User with that name does not exist."
    

class EmptyUsernameError(Exception):
    """Exception class when no username is specified."""

    def __str__(self) -> str:
        return "Please enter username."


def input_error(funk):
    """Decorator function to handle input errors.

    Args:
        funk (function): The function to be decorated.

    Returns:
        function: The decorated function."""

    def inner(*args, **kwargs):
        """Inner function of the input_error decorator.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the decorated function or an error message.

        Raises:
            EmptyUsernameError: If no username is specified.
            KeyError: If the name of an existing user is not entered.
            UnboundLocalError: If username and phone number are not entered.
            AddingExistingUser: If a user with the same name already exists.
            InvalidPhoneNumber: If the phone number format is incorrect.
            NonExistentUser: If the user does not exist."""

        try:
            return funk(*args, **kwargs)
        except EmptyUsernameError as err:
            return err
        except KeyError:
            return "Please enter the name of an existing user"
        except UnboundLocalError:
            return "Please enter username and phone number"        
        except AddingExistingUser as err:
            return err
        except InvalidPhoneNumber as err:
            return err
        except NonExistentUser as err:
            return err
        
    return inner


def separates_name_phone(args: list[str]) -> tuple[str]:
    """Separates the name and phone number from the given arguments.

    Args:
        args (list): List of string arguments.

    Returns:
        tuple: A tuple containing the name (str) and phone number (str)."""

    index = len(args)  
    for i, arg in enumerate(args):
        if re.search(r'\d', arg):
            index = i
            break

    name = ' '.join(args[:index])    
    phone = ''.join(args[index:])

    return name, phone


def format_phone(phone: str) -> str:
    """Formats the phone number.

    Args:
        phone (str): Phone number string.

    Returns:
        str: Formatted phone number.
        
    Raises:
        InvalidPhoneNumber: If the phone number format is incorrect."""

    formatted_phone = ''.join(filter(str.isdigit, phone))
    if  not (8 < len(formatted_phone) < 13):
        raise InvalidPhoneNumber
    formatted_phone = '+380'[:13 - len(formatted_phone)] + formatted_phone
    formatted_phone = f"{formatted_phone[:3]}({formatted_phone[3:6]}){formatted_phone[6:9]}-{formatted_phone[9:11]}-{formatted_phone[11:]}"

    return formatted_phone


@input_error
def add_new_user(args: list[str]) -> str:
    """Adds a new user to the users dictionary.

    Args:
        args (list): List of string arguments.

    Returns:
        str: Success message if the user is added successfully.

    Raises:
        EmptyUsernameError: If no username is specified.
        AddingExistingUser: If a user with the same name already exists.
        InvalidPhoneNumber: If the phone number format is incorrect."""

    user, phone  = separates_name_phone(args) 

    if not user:
        raise EmptyUsernameError

    if user in users:
        raise AddingExistingUser
    
    users[user] = format_phone(phone)

    return "User added successfully."


@input_error
def change_phone(args: list[str]) -> str:
    """Changes the phone number of an existing user.

    Args:
        args (list): List of string arguments.

    Returns:
        str: Success message if the phone number is changed successfully.

    Raises:
        NonExistentUser: If the user does not exist.
        InvalidPhoneNumber: If the phone number format is incorrect.
    """

    user, phone  = separates_name_phone(args)
    
    if user not in users:
        raise NonExistentUser  
    users[user] = (phone := format_phone(phone))

    return f"The phone number of the user {user} was changed to {phone}"

@input_error
def show_phone(args: list[str]) -> str:
    """Retrieves the phone number of a user.

    Args:
        args (list): List of string arguments.

    Returns:
        str: The phone number of the user.

    Raises:
        NonExistentUser: If the user does not exist."""
    
    user = ' '.join(args)
    return users[user]


def show_all() -> str:
    """Displays all the users and their phone numbers.

    Returns:
        str: A formatted string representing all the users and their phone numbers.
        "The users list is empty" if there are no users."""
    
    if not users:
        return "The users list is empty"
    formatted_users = ''
    for name, phone in sorted(users.items()):
        formatted_users += f"{name.ljust(46, '_')}{phone.rjust(13, '_')} \n"
    return formatted_users


def main() -> None:
    """Main function to handle user inputs and execute commands."""

    while True:

        command = input('>>> ').strip(punctuation + '\n\t ') 

        if command.lower() in handlers["exit"]:
            print("Good bye!")
            break
        
        if command.lower() == 'hello':
            print("How can I help you?")
            continue
        
        if command.lower() == 'show all':
             print(show_all())
             continue

        args_list = command.split()
        if args_list[0] in handlers:
            print(handlers[args_list[0]](args_list[1:]))
            continue
        else:
            print(f"Enter one of the commands: {', '.join(list(handlers.keys()))}.")
  
    sys.exit(0)


users = {}

handlers = {'add': add_new_user, 
            'change': change_phone, 
            'phone': show_phone, 
            'show all': show_all, 
            "exit": ("exit", "close", "goodbye")
            }


if __name__ == '__main__':    
    main()





       
            