import io
import sys
def cs():
    print("cs320 ")

def is_():
    print("is ")

def my():
    print("my ")

def favorite():
    print("favorite ")

def class_():
    print("class ")

if __name__ == "__main__":
    output = io.StringIO()
    sys.stdout = output

    cs()
    is_()
    my()
    favorite()
    class_()

    sys.stdout = sys.__stdout__  # reset to normal stdout

    # now clean up the captured string to join into one line
    result = ' '.join(output.getvalue().split())
    print(result)
    # Arrange the function calls os that when part2.py is run, the output is:
    # cs320 is my favorite class

