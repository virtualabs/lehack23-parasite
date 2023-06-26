#!/usr/bin/python3
import sys
import png

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        payload = open(sys.argv[1], 'rb').read()
        cover = png.Reader(sys.argv[2])
        outfile = open(sys.argv[3], 'wb')

        chunks = list(cover.chunks())
        chunks = chunks[:2] + [(b'tEXT', payload)] + chunks[2:]
        png.write_chunks(outfile, chunks)
    else:
        print('usage: %s [PDF file] [Cover PNG file] [Output PNG file]' % sys.argv[0])
