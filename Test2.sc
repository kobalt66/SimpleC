private var a = 1;

#lib = "someLib"
#define MetaVar 1

namespace nSpace
{
    namespace otherSpace
    {
        public static class someClass // Check!
        {
        #metif MetaVar
            public static protected someClass SomeFunc(var a) { return; } // Check!
        #metendif
        }
    }
    private class Class
    {
        public void func() { return; }
    }
}
