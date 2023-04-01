# Prints all executed lines 

## pip install tracealllines

### Tested against Windows 10 / Python 3.10 / Anaconda 




```python

from tracealllines import print_execution, enable_trace_all, disable_trace_all

colorprint = "green"


@print_execution(
    file=__file__, color=colorprint, logfile="c:\\logogog.txt", enabled=True
)
def fu():
    for x in range(2):
        print(x * 1)


@print_execution(file=__file__, color=colorprint, logfile=None, enabled=True)
def fu3():
    for x in range(3):
        print(x * 25)


@print_execution(file=__file__, color=colorprint, logfile=None, enabled=True)
def fu2():
    for x in range(2):
        print(x * 150)


if __name__ == "__main__":
    fu()
    fu3()
    fu2()
    file, color, logfile = __file__, colorprint, "c:\\logogog.txt"

    enable_trace_all(file, color, logfile)
    fu2()
    disable_trace_all()
    fu3()



```

![](https://github.com/hansalemaos/screenshots/blob/main/lineexecprinter.png?raw=true)