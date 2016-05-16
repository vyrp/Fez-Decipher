# Fez-Decipher
A script that deciphers the text in the game [Fez](http://fezgame.com/) using computer vision and statical analysis.

:warning: This project contains spoilers for the game!

## Description

The deciphering of the language in Fez is divided in two phases.

### 1. Learning the symbol-to-letter table

With multi-scale template matching, the quantity of each symbol is determined using all screenshots of symbol-text present in the _database/_ folder.

Then, with statistical analysis, the most common english letters are determined. For the other letters, the help of a human is required.

We have then the mapping between symbols and english letters.

### 2. Translating a given symbol-text to english

Now, the useful part. Given a picture of a symbol-text, the script produces an image with the symbols replaced by english letters. Additionally, the user may opt for a text output.

## Dependencies
* Python 2.7
* Numpy
* Matplotlib
* OpenCV 3.x

## Usage

Setting up:

```$ python setup.py```


To generate the mapping:

```$ decipher-symbols.py```

Then for each image of symbol-text you want to translate:

```$ translate [-t|-i] <image>```

## Contributing

If you'd like to contribute, please use [Flake8](http://flake8.pycqa.org/en/latest/index.html) and its pre-commit hook:

```
$ pip install pep8-naming flake8
$ flake8 --install-hook
$ git config flake8.strict true
```

## References
* <http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html>
* <http://machinelearningmastery.com/using-opencv-python-and-template-matching-to-play-wheres-waldo/>
* <http://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/>
* <http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/>
