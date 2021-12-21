// test SimpleC program
#lib = "libname"
#define METAVAR 1000

namespace SomeSPACE
{
    #metif METAVAR
    public class Person 
    {
        using someNameSpace;

        public str name;
        public int age;
        public flt size;
        
        Person(str name, int age, flt, size)
            : name(name), age(age), size(size)
        {

        }

        public protected flt getAge()
        {
            return age;
        }
    }
    #metendif
}

/*
    Block Comment * 7//
*/

// asdf asdf asdf asdf asdf asdf asdf asdf 