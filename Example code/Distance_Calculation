#lib = "std"

namespace std
{
    namespace physics
    {
        struct Vec2
        {
            flt x;
            flt y;
            constructor(flt X, flt X)
            {
                x = X;
                y = Y;
            }
        }
        struct Vec3
        {
            flt x;
            flt y;
            flt z;
            constructor(flt x, flt y, flt z) 
                : x(x), y(y), z(z) {}
        }
        struct Vec4
        {
            flt x;
            flt y;
            flt z;
            flt w;
            constructor(flt x , flt y, flt z, flt w) 
                : x(x), y(y), z(z), w(w) {}
        }
    }
}

private class Program
{
    using std.physics;
    private function int main(var args)
    {
        // Create points.
        Var2 one = Var2(1, 2);
        Var2 two = Var2(2, 3);

        // Calculation.
        flt distance = calculate_DistanceVECtwo(one, two);

        return 1;
    }

    private function flt calculate_DistanceVECtwo(var a, var b)
    {
        // Checking if the two points are two dimensional.
        bol check1 = !isClass(a, Vec2);
        bol check2 = !isClass(b, Vec2);
        if (check1 | check2) return;

        // Calculating the distance between two points.
        flt res1 = sqrt(b.y - a.y);
        flt res2 = sqrt(b.x - a.x);
        flt distance = res1 + res2;

        return distance;
    }
}