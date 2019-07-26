#!/usr/bin/env python3

import sys
import struct
from typing import NamedTuple
import argparse
import zlib
import os
import logging

"""
The Retron5 data format is:

typedef struct
{
   uint32_t magic;
   uint16_t fmtVer;
   uint16_t flags;
   uint32_t origSize;
   uint32_t packed_size;
   uint32_t data_offset;
   uint32_t crc32;
   uint8_t data[0];
} t_retronDataHdr;
"""

class RetronDataHeader(NamedTuple):
    magic: int
    format_version: int
    flags: int
    original_size: int
    packed_size: int
    data_offset: int
    crc32: int

class Retron5SaveFiles:

    MAGIC = 0x354E5452 # "RTN5", except backwards
    FORMAT_VERSION = 1
    FLAG_ZLIB_PACKED = 0x01
    RETRON_DATA_HEADER_FORMAT = "I H H I I I I" # The format of this string is described here: https://docs.python.org/3/library/struct.html#struct-format-strings
    RETRON_DATA_HEADER_SIZE = struct.calcsize(RETRON_DATA_HEADER_FORMAT)

    @staticmethod
    def extract_from_retron_save_file(input_filename, output_filename):

        # Read file

        with open(input_filename, 'rb') as input_file:
            retron_data_header_bytes = input_file.read(Retron5SaveFiles.RETRON_DATA_HEADER_SIZE)
            save_data_bytes = input_file.read()
        input_file.closed

        retron_data_header = RetronDataHeader._make(struct.unpack_from(Retron5SaveFiles.RETRON_DATA_HEADER_FORMAT, retron_data_header_bytes))

        logging.debug("Read file and found magic 0x%x version 0x%x flags 0x%x original_size %d packed_size %d data offset %d bytes crc32 0x%x. Header is %d bytes" % (retron_data_header.magic, retron_data_header.format_version, retron_data_header.flags, retron_data_header.original_size, retron_data_header.packed_size, retron_data_header.data_offset, retron_data_header.crc32, Retron5SaveFiles.RETRON_DATA_HEADER_SIZE))

        # Check file format

        if retron_data_header.magic != Retron5SaveFiles.MAGIC:
            logging.error("Incorrect file format: magic did not match. Got magic 0x%x instead of 0x%x" % (retron_data_header.magic, Retron5SaveFiles.MAGIC))
            sys.exit(1)

        if retron_data_header.format_version > Retron5SaveFiles.FORMAT_VERSION:
            logging.error("Incorrect file format: format version did not match. Got version 0x%x instead of 0x%x" % (retron_data_header.format_version, Retron5SaveFiles.FORMAT_VERSION))
            sys.exit(1)

        if retron_data_header.data_offset != Retron5SaveFiles.RETRON_DATA_HEADER_SIZE:
            logging.error("Incorrect file format: expected header size: %d bytes, but file specifies %d instead" % (Retron5SaveFiles.RETRON_DATA_HEADER_SIZE, retron_data_header.data_offset))
            sys.exit(1)

        if retron_data_header.packed_size != len(save_data_bytes):
            logging.error("Error reading file: expected %d bytes of save data but found %d instead" % (retron_data_header.packed_size, len(save_data_bytes)))
            sys.exit(1)

        # Pull the save data from the file

        save_data = save_data_bytes

        if (retron_data_header.flags & Retron5SaveFiles.FLAG_ZLIB_PACKED) != 0:

            save_data = zlib.decompress(save_data_bytes)

            logging.debug("Decompressed %d bytes into %d bytes; expected to find %d bytes" % (len(save_data_bytes), len(save_data), retron_data_header.original_size))
        else:
            logging.debug("Data not compressed - skipping decompression step")

        if len(save_data) != retron_data_header.original_size:
            logging.error("Corrupted save data: expected to find %d bytes but actually found %d" % (retron_data_header.original_size, len(save_data)))
            sys.exit(1)

        save_data_crc32 = zlib.crc32(save_data)

        logging.debug("Found crc32 0x%x; expected 0x%x" % (save_data_crc32, retron_data_header.crc32))

        if save_data_crc32 != retron_data_header.crc32:
            logging.error("Corrupted save data: CRC did not match. Expected 0x%x but got 0x%x", (retron_data_header.crc32, save_data_crc32))
            sys.exit(1)

        # Write out the save data

        with open(output_filename, 'wb') as output_file:
            bytes_written = output_file.write(save_data)
        output_file.closed

        logging.debug("Wrote out %d bytes" % (bytes_written))
        logging.info("Extracted %s => %s" % (input_filename, output_filename))

    @staticmethod
    def pack_to_retron_save_file(input_filename, output_filename):

        # Read in the data

        with open(input_filename, 'rb') as input_file:
            save_data_bytes = input_file.read()
        input_file.closed

        # Compress it

        save_data_uncompressed_size = len(save_data_bytes)
        save_data_crc32 = zlib.crc32(save_data_bytes)
        save_data_bytes_compressed = zlib.compress(save_data_bytes)
        save_data_compressed_size = len(save_data_bytes_compressed)

        logging.debug("Read in %d bytes. Calculated CRC32: 0x%x. Compressed to %d bytes." % (save_data_uncompressed_size, save_data_crc32, save_data_compressed_size))

        # Create the header

        retron_data_header = RetronDataHeader(
            magic = Retron5SaveFiles.MAGIC,
            format_version = Retron5SaveFiles.FORMAT_VERSION,
            flags = Retron5SaveFiles.FLAG_ZLIB_PACKED,
            original_size = save_data_uncompressed_size,
            packed_size = save_data_compressed_size,
            data_offset = Retron5SaveFiles.RETRON_DATA_HEADER_SIZE,
            crc32 = save_data_crc32)

        # Write out the header + compressed data

        retron_data_header_packed = struct.pack(Retron5SaveFiles.RETRON_DATA_HEADER_FORMAT,
            retron_data_header.magic,
            retron_data_header.format_version,
            retron_data_header.flags,
            retron_data_header.original_size,
            retron_data_header.packed_size,
            retron_data_header.data_offset,
            retron_data_header.crc32)

        with open(output_filename, 'wb') as output_file:
            header_bytes_written = output_file.write(retron_data_header_packed)
            save_data_bytes_written = output_file.write(save_data_bytes_compressed)
        output_file.closed

        logging.debug("Wrote out %d bytes for the header, and %d bytes for the compressed save data" % (header_bytes_written, save_data_bytes_written))
        logging.info("Packed %s => %s" % (input_filename, output_filename))

# Command line arguments

parser = argparse.ArgumentParser(description="Read and write Retron5 save files")

parser.add_argument("-d", "--debug", action="store_true", dest="debug", default=False, help="Display debug information")
parser.add_argument("-t", "--to-retron", action="store_true", dest="to_retron", default=False, help="Convert to Retron5 format. Otherwise, convert from Retron5 format")
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument("-i", "--input-file", dest="input_filename", type=str, help="File to read in", required=True)
requiredArguments.add_argument("-o", "--output-dir", dest="output_directory", type=str, help="Directory to place the outputted file", required=True)

args = parser.parse_args()

base_filename = os.path.splitext(os.path.basename(args.input_filename))[0] # Pull out just the file name: "/path/to/filename.ext" => "filename"

output_filename = os.path.join(args.output_directory, base_filename)

log_level = logging.INFO
if args.debug:
    log_level = logging.DEBUG

logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

if args.to_retron:
    output_filename += ".sav" 
    Retron5SaveFiles.pack_to_retron_save_file(args.input_filename, output_filename)
else:
    output_filename += ".srm" # FIXME: Need to change this per platform?
    Retron5SaveFiles.extract_from_retron_save_file(args.input_filename, output_filename)

sys.exit(0)