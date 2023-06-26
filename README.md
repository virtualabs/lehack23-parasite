# Parasitizing servers for fun and profit

This repository contains all the resources (slides, proof of concept source code)
for my [presentation at leHACK in June 2023](https://lehack.org/track/parasitage-de-serveur-for-fun-and-profit/).

## Turning binary files into PNG images for web upload

I developed a small Python tool called *Flea* that is able to transform any
binary file into a valid (but weird looking) PNG file:

```
$ ./flea.py my-binary-file.pdf output-png-file.png
```

But also to take such a PNG file in input and extract the embedded data back:

```
$ ./flea.py --decode output-png-file.png
```

It can also embed a binary file inside a PNG in a *tEXt* chunk:

```
$ ./flea.py --cover something.png my-binary-file.pdf output-png-file.png
```

Extraction is performed the same way:

```
$ ./flea.py --decode output-png-file.png
```

## Creating a PNG/PDF polyglot file for Imgur

The script demonstrated in the presentation is provided as-is in this repo.
