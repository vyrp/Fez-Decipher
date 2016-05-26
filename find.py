import cv2
import sys


def find(name, module=cv2):
    print "\n".join(filter(lambda s: name in s.lower(), dir(module)))


def find_not(name, module=cv2):
    print "\n".join(filter(lambda s: name not in s.lower(), dir(module)))

if __name__ == "__main__":
    find(sys.argv[1])

__all__ = ["find", "find_not"]
