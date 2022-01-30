#lib = "Test3"

#define electron 1.602e-19
#define gravity 9.81
#define string "sdfsdfsdf"

public class Program
{
    public static function void Main(var args)
    {
        list[] intList = int[12];
        list[] balls = { Ball(10, 1), Ball(5, 2), Ball(2.3, 3), Ball(3.14159, 4) }

        while (true)
            for (int i = 0; i < balls.Length; i++;)
            {
                Ball Var = balls[i];
                Var.Fg();
                
                str msg = Var.id + " : y = " + Var.position.y;
                Console.WriteLine(msg)
            }
    }
}

public class Ball
{
    public flt mass;
    public int id;
    public Vec2 position = Vec2(0, 0);
    
    constructor(flt Mass, int Id) : mass(Mass), id(Id)

    public protected function void Fg()
    {
        flt force = mass * gravity;
        position.y -= force;
    }
}

struct Vec2 
{
    public flt x;
    public flt y;
    constructor(flt X, flt Y) : x(X), y(Y)
}
