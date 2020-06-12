from django.test import TestCase

# Create your tests here.
import  os
print(os.path.abspath("./"))
print(os.getcwd())
A='besettest.py'
B="interface\\testFiles"

c=os.path.splitext(A)
print(c)