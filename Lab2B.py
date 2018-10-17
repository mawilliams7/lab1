"""
CS 2302
Mark Williams
Lab 2A
Diego Aguirre/Manoj Saha
10-12-18
Purpose: Use linked lists to find duplicate passwords in a list
         of passwords.
"""


from Node import Node
import time


def merge(left_value, right_value, left_password, right_password):
  """
  Merges two stacks(lists) into one stack(list)
  
  Args:
    left_value: A list of password counts
    right_value: A list of password counts
    left_password: A list of password strings
    right_password: A list of password strings
  
  Returns:
    merged_list_values: A sorted list of numbers that reflect the
						password counts
    merged_list_passwords: A sorted list of password strings, sorted by
						   their corresponding count in 
						   merged_list_values.

  """
  merged_list_values = []
  merged_list_passwords = []
  i = 0
  j = 0
  while i < len(left_value) and j < len(right_value):
    if left_value[i] <= right_value[j]:
      merged_list_values.append(left_value[i])
      merged_list_passwords.append(left_password[i])
      i += 1
    else:
      merged_list_values.append(right_value[j])
      merged_list_passwords.append(right_password[j])
      j += 1
  while i < len(left_value):
    merged_list_values.append(left_value[i])
    merged_list_passwords.append(left_password[i])
    i += 1
  while j < len(right_value):
    merged_list_values.append(right_value[j])
    merged_list_passwords.append(right_password[j])
    j += 1
  return merged_list_values, merged_list_passwords


def merge_sort_with_stacks(linked_list):
  """
  Sorts a linked list using a reduced merge sort algorithm with stack
  implementation. In Python, lists have the same functionality
  as generic stacks so lists are used here.
  
  Args:
    linked_list: A linked list of Node objects
  
  Returns:
    sorted_password_list: A linked list of Node objects sorted based on
                          count

  """
  if linked_list == None:
    return None
  # Stacks for password counts
  stack1 = []
  stack2 = []
  # Stacks for passwords
  stack3 = []
  stack4 = []
  helper = linked_list
  # This code skips the separation part of merge sort and directly
  # creates a list of lists that each contain one password count
  while helper != None:
    temp_value = []
    temp_value.append(helper.count)
    stack1.append(temp_value)
    temp_password = []
    temp_password.append(helper.password)
    stack3.append(temp_password)
    helper = helper.next
  while len(stack1) > 1:
    while len(stack1) > 1:
      left_value = stack1.pop()
      right_value = stack1.pop()
      left_password = stack3.pop()
      right_password = stack3.pop()
      merged_values, merged_passwords = merge(left_value, right_value,
                                          left_password, right_password)
      stack2.append(merged_values)
      stack4.append(merged_passwords)
    while len(stack2) > 1:
      left_value = stack2.pop()
      right_value = stack2.pop()
      left_password = stack4.pop()
      right_password = stack4.pop()
      merged_values, merged_passwords = merge(left_value, right_value,
                                          left_password, right_password)
      stack1.append(merged_values)
      stack3.append(merged_passwords)
  sorted_password_list = None
  sorted_values = None
  sorted_passwords = None
  if len(stack1) == 0:
    sorted_values = stack2.pop()
    sorted_passwords = stack4.pop()
  else:
    sorted_values = stack1.pop()
    sorted_passwords = stack3.pop()
  for value in range(len(sorted_values)):
    sorted_password_list = Node(sorted_passwords[value], 
                          sorted_values[value], sorted_password_list)
  return sorted_password_list


def length_linked_list(linked_list):
  """
  Reads a password file and generates a linked list without duplicates
  based on its contents.
  
  Args:
    password_file: A file object that points to the file with the 
                   passwords
  
  Returns:
    password_list: A linked list of Node objects

  """
  helper = linked_list
  counter = 0
  while helper != None:
    counter = counter + 1
    helper = helper.next
  return counter


def bubble_sort(password_list):
  """
  Sorts a linked list using the bubble sort algorithm.
  
  Args:
    password_list: A linked list of Node objects
  
  Returns:
    sorted_password_list: A linked list of Node objects sorted based on
                          count

  """
  helper = password_list
  unsorted_passwords = []
  unsorted_values =  []
  while helper != None:
    unsorted_passwords.append(helper.password)
    unsorted_values.append(helper.count)
    helper = helper.next
  for value in range(len(unsorted_values)-1,0,-1):
    for i in range(value):
      if unsorted_values[i]>unsorted_values[i+1]:
        temp = unsorted_values[i]
        unsorted_values[i] = unsorted_values[i+1]
        unsorted_values[i+1] = temp
        temp_password = unsorted_passwords[i]
        unsorted_passwords[i] = unsorted_passwords[i+1]
        unsorted_passwords[i+1] = temp_password
  sorted_password_list = None
  for value in range(len(unsorted_values)):
    sorted_password_list = Node(unsorted_passwords[value], 
                        unsorted_values[value], sorted_password_list)
  return sorted_password_list


def get_password_list_from_file(password_file):
  """
  Reads a password file and generates a linked list without duplicates
  based on its contents
  
  Args:
    password_file: A file object that points to the file with the 
                   passwords
  
  Returns:
    password_list: A linked list of Node objects

  """
  password_list = None
  for line in password_file.readlines():
    # combination: username/password combo
    combination = line.split()
    # Considers the case where a username/password entry is incomplete
    if len(combination) < 2:
      continue
    helper = password_list
    duplicate = False
    while helper != None:
      if helper.password == combination[1]:
        helper.count = helper.count + 1
        duplicate = True
        break
      helper = helper.next
    if not duplicate:
      password_list = Node(combination[1], 1, password_list)
  return password_list


def get_password_dict_from_file(password_file):
  """
  Reads a password file and generates a dictionary
  based on its contents.
  
  Args:
    password_file: A file object that points to the file with the 
                   passwords
  
  Returns:
    password_dict: A dictionary with keys as passwords and values as
                   that password's count

  """
  password_dict = dict()
  for line in password_file.readlines():
    combination = line.split()
    # Considers the case where a username/password entry is incomplete
    if len(combination) < 2:
      continue
    if combination[1] in password_dict:
      password_dict[combination[1]] = password_dict[combination[1]] + 1
    else:
      password_dict[combination[1]] = 1
  return password_dict


def create_list_from_dict(password_dict):
  """
  Creates a linked list of Node objects based on password dictionary.
  
  Args:
    password_dict: A dictionary with keys are passwords and values as
                   that password's count
  
  Returns:
    password_list: A linked list of Node objects

  """
  password_list = None
  for key in password_dict:
    password_list = Node(key, password_dict[key], password_list)
  return password_list


def read_from_file(filename):
  """
  Creates a Python file object based on filename.
  
  Args:
    filename: The name of the file that needs to be read
  
  Returns:
    password_file: A Python file object

  """
  password_file  = open(filename, "r")
  return password_file


def main():
  # Possible sample files: sample1, sample2, sample3, sample 4, sample 5
  start_loop = time.time()
  password_list1 = get_password_list_from_file(
                          read_from_file("sample1.txt"))
  print("It took " + str(time.time()-start_loop) + 
        " seconds to create the linked list using loops.")
  start_dict = time.time()
  password_dict = get_password_dict_from_file(
                          read_from_file("sample1.txt"))
  password_list2 = create_list_from_dict(password_dict)
  print("It took " + str(time.time()-start_dict) + 
        " seconds to create the linked list using a dictionary.")
  start1 = time.time()
  sorted_password_list = bubble_sort(password_list1)
  print("It took " + str(time.time() - start1) + 
        " seconds to sort the password list of size " + 
        str(length_linked_list(password_list1)) + 
        " with bubble sort.")
  helper1 = sorted_password_list
  print("The top 20 passwords according to this sorted list are:")
  for _ in range(20):
    print(helper1.password + ": " + str(helper1.count))
    helper1 = helper1.next
  sorted_password_list = None
  start2 = time.time()
  sorted_password_list = merge_sort_with_stacks(password_list2)
  print("It took " + str(time.time() - start2) + 
      " seconds to sort the password list of size " + 
      str(length_linked_list(password_list2)) + 
      " with merge sort.")
  helper2 = sorted_password_list
  print("The top 20 passwords according to this sorted list are:")
  for _ in range(20):
    print(helper2.password + ": " + str(helper2.count))
    helper2 = helper2.next


main()
