/* prog3.g - Functions */

/* Gone has user-defined functions.  Here's a function that determines
   if a number is prime or not. It's not terribly efficient. */

func isprime(n int) bool {
    var factor int = 2;
    var divisor int;
    while factor < (n / 2) {
        divisor = n / factor;
        if factor * divisor == n {
            return false;
        }
        factor = factor + 1;
    }
    return true;
}

func main() int {
   print isprime(15);    // Prints 0
   print isprime(37);    // Prints 1
   return 0;
}

/* Run the above program using python begone.py prog3.g. Make
   sure the output is correct (according to the comments) */

/* Challenge.  Modify the program to print all of the prime numbers less
   than 100 */


