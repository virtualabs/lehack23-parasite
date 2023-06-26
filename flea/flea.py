#!/usr/bin/python3

"""

Flea - a python-based tool to pack a binary file into a PNG file to send
       it over Imgur

Author: Damien "virtualabs" Cauquil
"""

import os.path
import argparse
import png
from PIL import Image
from math import sqrt
from struct import pack, unpack

from binascii import hexlify

FLEA_MAGIC = 0xF1EAF1EA

def encode_image(in_file, output, cover_image=None):
    """Encode a file into a PNG image, and store it 
    in `output`.
    """
    # First, we need to read the content of our file
    try:
        # Get file size and name
        docsize = os.path.getsize(in_file)
        _, docname = os.path.split(in_file)

        # Generate file metadata:
        # MAGIC + filesize + namesize + name
        docmeta = pack('<II', FLEA_MAGIC, docsize)
        docmeta += pack('<H', len(docname)) + bytes(docname, 'utf-8')

        # Load file into memory and prefix with metadata
        content = docmeta + open(in_file, 'rb').read()

        if cover_image is not None:
             cover = png.Reader(cover_image)
             chunks = list(cover.chunks())
             chunks = chunks[:2] + [(b'tEXT', bytes(content))] + chunks[2:]
             with open(output, 'wb') as f:
                 png.write_chunks(f, chunks)
                 f.close()
        else:
            # Compute image size
            nb_pixels = len(content)/3
            if nb_pixels*3 < len(content):
                nb_pixels += 1
            width = int(sqrt(nb_pixels))
            height = int(nb_pixels/width)
            if width*height < nb_pixels:
                height += 1

            # Pad our content to match the expected size
            exp_size = width*height*3
            if len(content) < exp_size:
                content += b'\x00'*(exp_size - len(content))

            # Allright, now we need to create the image
            img = Image.frombytes('RGB', (width, height), content)
            img.save(output)


    except IOError as err:
        print('[!] Cannot access input file `%s`' % in_file)
        return False

def decode_image(in_file, dest_dir, use_text_chunk=False):
    """Decode a PNG image into a file
    """
    # First, we need to read the content of our file
    try:

        # First, try to load our PNG and detect a 3rd tEXT chunk.
        img_png = png.Reader(in_file)
        chunks = list(img_png.chunks())

        img_data = None
        for chunk in chunks:
            if chunk[0] == b'tEXT':
                # Retrieve chunk value and check header and magic
                text_chunk = chunk[1]

                # Extract header and check magic
                magic, docsize, namesize = unpack('<IIH', text_chunk[:10])
                if magic != FLEA_MAGIC:
                    print('[!] Image has not been encoded with flea, exiting.')
                    return
                else:
                    img_data = text_chunk
                    break

        if img_data is None:
            # Load image file into PIL
            img = Image.open(in_file)

            # Access its buffer
            img_data = img.tobytes()

        magic, docsize, namesize = unpack('<IIH', img_data[:10])
        if magic != FLEA_MAGIC:
            print('oops')
            print('[!] Image has not been encoded with flea, exiting.')
            return

        # Extract name
        docname = img_data[10:10+namesize].decode('utf-8')

        # Extract document content
        content = img_data[10+namesize:10+namesize+docsize]

        # Save document
        docpath = os.path.join(dest_dir, docname)
        open(docpath, 'wb').write(content)
        print('Wrote %d bytes in `%s`.' % (docsize, docpath))

    except IOError as err:
        print('[!] Cannot access input file `%s`' % in_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--decode', '-d', action='store_true', default=False, dest='decode', help='Decode file and store file into the specified directory')
    parser.add_argument('--cover', '-c', dest='cover', help='Specify a PNG image to use as a cover')
    parser.add_argument('--dir', '-o', dest='outdir', help='Destination directory', default='')
    parser.add_argument('file', metavar='FILE')
    parser.add_argument('output', nargs='?', metavar='OUTPUT')
    args = parser.parse_args()

    if args.file is not None:
        if args.decode:
            decode_image(args.file, args.outdir)
        elif args.output is not None:
            encode_image(args.file, args.output, args.cover)
        else:
            print('[!] Please specify an output file.')
