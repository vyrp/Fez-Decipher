import cv2
import inspect
import os
import re
import shutil

_separator = re.compile(r"/|\\")
_type_name = re.compile(r"<type '(\w+)'>")


def foreach_file_in_folder(foldername, opname, func):
    """
    Executes `func` for each image in folder `foldername`.
    Writes output in folder `foldername`_`opname`.
    """
    foldername = _separator.split(foldername)[0]

    newfolder = foldername + "_" + opname
    if os.path.isdir(newfolder):
        shutil.rmtree(newfolder)
    os.mkdir(newfolder)

    print "Starting [%s]" % opname

    for filename in os.listdir(foldername):
        img = cv2.imread(os.path.join(foldername, filename))
        result_img = func(img)
        cv2.imwrite(os.path.join(newfolder, filename), result_img)

    print "Done"


def run(fn, argv):
    """
    Runs function `fn` with arguments `argv` foreach file in folder.
    """
    fn_name = fn.func_name
    args = inspect.getargspec(fn).args
    types = fn.types
    if len(argv) - 2 != len(args):
        str_args = ["<%s:%s>"
                    % (arg, _type_name.match(str(t)).group(1)) for arg, t in zip(args, types)]
        print "\nUsage:\n    %s.py <foldername:str> %s" % (fn_name, " ".join(str_args))
        exit(1)

    foreach_file_in_folder(argv[1], fn_name, fn(*[T(v) for T, v in zip(types, argv[2:])]))


def run_once(fn, argv):
    """
    Runs function `fn` with arguments `argv`.
    """
    fn_name = fn.func_name
    args = inspect.getargspec(fn).args
    types = fn.types
    if len(argv) - 1 != len(args):
        str_args = ["<%s:%s>"
                    % (arg, _type_name.match(str(t)).group(1)) for arg, t in zip(args, types)]
        print "\nUsage:\n    %s.py %s" % (fn_name, " ".join(str_args))
        exit(1)

    fn(*[T(v) for T, v in zip(types, argv[1:])])
