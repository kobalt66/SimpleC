import SimpleC
from SimpleC import openFile, fileType
outputData = None


def setOutputdir(dir):
    SimpleC.outputdir = dir


def setProjectdir(dir):
    SimpleC.projectdir = dir

def retrunData():
    return outputData


setProjectdir('Test Project/scripts')


while True:
    script = ''
    fn = ''
    text = input('[@] > ')

    if text.strip() == "":
        continue
    if text.strip() == "run§":
        fn = input('[FileName] > ')
        if fn.strip() == "":
            continue

        script, error = openFile(fn + fileType)
        if error:
            error.throw()
        error = SimpleC.run(f'{fn}', script)
    else:
        error = SimpleC.run("console", text)

    if error:
        error.throw()
        outputData = "Something went wrong! (No data received)"

    # if result:
    #     print(result)
    #     print('\n\n\t => Everything worked!')
    # elif error:
    #     error.throw()
