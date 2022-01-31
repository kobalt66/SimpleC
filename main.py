import SimpleC
outputData = None


def setOutputdir(dir):
    SimpleC.outputdir = dir


def retrunData():
    return outputData


while True:
    script = ''
    pn = ''
    text = input('[@] > ')

    if text.strip() == "":
        continue
    if text.strip() == "compile§":
        pn = input('[Project directory] > ')
        if pn.strip() == "":
            continue

        error = SimpleC.run(pn)

    if error:
        error.throw()
        outputData = "Something went wrong! (No data received)"
