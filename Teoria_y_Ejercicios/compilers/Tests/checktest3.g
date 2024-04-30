/* checktest3.g - Introducing types

   All data in Gone has an associated type.  You need to start building
   the type system.  Go to the file Gone/typesys.py and look at the
   instructions there.   When you come back, start work on attaching
   types to objects.

   Your first task: attach types to simple literals.   Run this
   test using:

        bash % python3 -m gone.checker Tests/checktest3.g --show-types
*/

print 2;              // Verify that "int" type is attached
print 3.5;            // Verify that "float" type is attached
print 'h';            // Verify that "char" type is attached
