/*

This example code is the code that can be parsed at the current development state.
Past the code in a script and run it in the console.

*/

/*private var a = 1;

#lib = "someLib"
#define MetaVar 1

namespace nSpace
{
    namespace otherSpace
    {
        public static class someClass
        {
            const int b = 0;
            constructor(var a, int c)
            : b(a), b(c)
            {
            }

            public static function void Func(var a, bol checked) 
            {
                return null;
            }
        }
    }
    namespace otherSpace2
    {
        struct TestStruct
        {
            const int b = 0; 
            constructor(var a, int c)
                : b(a), b(c)
            {
            }
        }
    }
}
*/

/*public class CLASS
{
    public function int Func()
    {    
        while (i < 0) flt a = 1.0;
        for (int i = 100; i < 10; i--) continue;
                             
        int a = 5;
        if ((a % 2) ? 0) return a;
        elif (!((a % 2) ? 0)) return null;
        else return 10;
    }
}*/

/*public class CLASS
{
    int i = 1;
    public function var Func()
    {                        
        CLASS test = CLASS();
        test.i++;
        return test;
    }

    override CLASS::Func()
    {
        CLASS newClass = CLASS();

        newClass.i *= 100;
        
        var a = newClass.i;
        
        return newClass;
    }
}*/

namespace testSpace
{
    namespace otherSpace
    {
        public class CLASS
        {
            using testSpace.otherSpace;

            int i;
            str name;

            constructor(int I, str name)
                : name(name)
            {
                i = I;
            }

            public function var Func()
            {
                CLASS newClass = CLASS(1, "CLASS NAME");
                str name = newClass.name;
                return newClass.i;
            }
        }
    }
}
