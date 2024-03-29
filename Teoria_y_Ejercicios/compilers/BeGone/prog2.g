/* prog2.g - Calculations */

/* Gone has constants, variables, integers, and floating point numbers.
   The following program is an example.  In this program, a rubber
   ball is dropped off a building with an initial height of 100 meters.
   On each bounce, the ball rebounds to 3/5 its original height. Print
   the height of the ball on the first 10 bounces. 
 */
   
const initial_height = 100.0;
const rebound = 0.6;
const total_bounces = 10;

func main() int {
   var bounce int = 0;
   var height float = initial_height;
   while bounce < total_bounces {
       bounce = bounce + 1;
       height = height * rebound;
       print(height);
   }
   return 0;
}

/* Run the above program using python begone.py prog2.g.  Make sure
   you understand the output. Try changing some of the initial constants */

/* Challenge.  Modify the program to solve the Tooth Fairy problem.
   Upon losing their first tooth, the tooth fairy offers the child a
   choice.  They can either receive $10 for every tooth lost or if they
   are willing to accept a single penny for the first tooth, the
   tooth fairy will double the amount given for each subsequent tooth.
   Which is a better deal?  A child typically has 20 baby teeth.  */





