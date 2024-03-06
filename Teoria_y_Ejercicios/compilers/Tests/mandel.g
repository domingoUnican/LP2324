/* mandel.g */

const xmin = -2.0;
const xmax = 1.0;
const ymin = -1.5;
const ymax = 1.5;
const width = 80.0;
const height = 40.0;
const threshhold = 1000;

func in_mandelbrot(x0 float, y0 float, n int) bool {
    var x float = 0.0;
    var y float = 0.0;
    var xtemp float;
    while n > 0 {
        xtemp = x*x - y*y + x0;
        y = 2.0*x*y + y0;
        x = xtemp;
        n = n - 1;
        if x*x + y*y > 4.0 {
            return false;
        }
    }
    return true;
}

func mandel() int {
     var dx float = (xmax - xmin)/width;
     var dy float = (ymax - ymin)/height;

     var y float = ymax;
     var x float;

     while y >= ymin {
         x = xmin;
         while x < xmax {
             if in_mandelbrot(x,y,threshhold) {
                print '*';
             } else {
                print '.';
             }
             x = x + dx;
         }
         print '\n';
         y = y - dy;
     }
     return 0;
}

func main() int {
    return mandel();
}





