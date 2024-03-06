/* floattest.g

   Test all of the basic expressions on floats
*/

/* Floating point operations */

const fa = 1.0;        // Float constant
var fb float = 2.0;    // Float variable declaration (with value)
var fc float;          // Variable declaration (no value)

fc = fa + fb + 3.0;    // Assignment to an float

print fc;              // Float printing.  Outputs 6.0
print fa + fb;         // Outputs 3.0
print fa - fb;         // Outputs -1.0
print fb * fc;         // Outputs 12.0
print fc / fb;         // Outputs 3.0
print +fa;             // Outputs 1.0
print -fa;             // Outputs -1.0
print fa + fb * fc;       // Outputs 13.0
