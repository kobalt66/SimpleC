import SimpleC


def openFile(fn):
    try:
        with open(fn, "r") as f:
            script = f.read()
            return script, None
    except Exception as e:
        return None, SimpleC.Error(e, SimpleC.PYTHON_EXCEPTION, -1, -1, fn)


while True:
    result = None 
    error = None
    script = ''
    fn = ''
    text = input('[@] > ')

    if text.strip() == "":
        continue
    if text.strip() == "run§":
        fn = input('[FileName] > ')
        if fn.strip() == "":
            continue
        
        script, error = openFile(fn)
        if error:
            error.throw()
        result, error = SimpleC.run(f'<{fn}>', script)
    else:
        result, error = SimpleC.run("<Test.sc>", text)

    if result:
        print(result)
    elif error:
        error.throw()
