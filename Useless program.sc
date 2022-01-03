#lib = "Test3"
#import <std>

#define electron 1.602e-19
#define gravity 9.81

private class Program
{
    public protected function void main(var args)
    {
        var[] balls = { Ball(10, 1), Ball(5, 2), Ball(2.3, 3), Ball(3.14159, 4) }

        while (true)
            for (int i = 0; i < lengthof(balls); i++;)
            {
                balls[i].Fg();
                
                str msg = balls[i].id + " : y = " + balls[i].position.y;
                print(msg)
            }
    }
}

private class Ball
{
    public flt mass;
    public int id;
    public Vec2 position = Vec2(0, 0);
    
    constructor(flt mass, int id) : mass(mass), id(id) {}

    public protected function void Fg()
    {
        force = mass * gravity;
        position.y -= force;
    }
}
