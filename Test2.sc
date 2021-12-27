/*

This example code is the code that can be parsed at the current development state.
Past the code in a script and run it in the console.

*/

private var a = 1;

#lib = "someLib"
#define MetaVar 1

namespace nSpace
{
    namespace otherSpace
    {
        public static class someClass
        {
        #metif MetaVar
            public static protected someClass SomeFunc(var a) { return; }
        #metendif
        }
    }
    private class Class
    {
        public void func() { return; }
    }
}
