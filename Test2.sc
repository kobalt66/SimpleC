#lib = "someLib"
#define MetaVar 1

namespace nSpace 
{
    public static class someClass // Check!
    {
        using someLib;  // Check!
        private var a = 12; // Check!
        private static void SomeFunction() // Check!
        {
            var c = 1;
            var b = (1 - (-1)) * 2^4;
        }
        private void Func() 
        {
            var a = someClass;
            byt b = $0xFF;
            int i = 120120;
            flt f = 1e-12;
            dbl d = 0.0000000000000000000000000000000000000000000000001;
            str s = "String";
            chr c = 'c';

            return a + b / i * f - -(d ^ s) + c;
        }
        
    #metif MetaVar
        public static protected someClass SomeFunc(var a) { return (12 * 12^24) / -(1 - 1); } // Check!
    #metendif
    }
}

public class Class2
{
    using someLib;
    using nix;
    using alles;

    public static protected someClass SomeFunction()
    {
        var c = 1;
        var b = (1 - (-1)) * 2^4;
    }
}
