#!/usr/bin/env python

import lz4.block
import sys
import struct

def print_usage_and_exit(): 
    print(f"usage: \n\t{sys.argv[0]} c decompressed_file.dll outupt.dll")
    print(f"\t{sys.argv[0]} d compressed_file.dll output.dll")
    exit()

def decompress_file(inp, out):
    # file is DLL compressed
    filebytes = open(inp, "rb").read()
    if filebytes[:4] != b"XALZ":
        sys.exit("The input file is not LZ4 compressed")

    header_index = filebytes[4:8]
    payload = filebytes[8:]

    print("Index %s" % header_index)
    print("Compressed size %s bytes" % len(payload))

    decompressed = lz4.block.decompress(payload)

    with open(out, "wb") as o:
        o.write(decompressed)
        o.close()

    print("file created %s" % out)

def compress_file(inp, out):
    # file is clean DLL
    filebytes = open(inp, 'rb').read()
    if filebytes[:2] != b"MZ":
        sys.exit("Input file is not DLL file")

    compress = lz4.block.compress(filebytes)

    with open(out, "wb") as o:
        o.write(b"\x58\x41\x4C\x5A\x00\x00\x00\x00")
        o.write(compress)
        o.close()

    print("file compressed ans created: %s" % out)

def main():
    if len(sys.argv) < 4:
        print_usage_and_exit()
    choice = sys.argv[1]
    inp_file = sys.argv[2]
    out_file = sys.argv[3]

    if choice.lower() == "d":
        decompress_file(inp_file, out_file)

    elif choice.lower() == "c":
        compress_file(inp_file, out_file)

main()
