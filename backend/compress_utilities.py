import os
import tempfile
from huffman_tree import HuffmanTree
import numpy as np

MARKER_VALUE = 255
MARKER_OCCURANCE = 15
MARKER_SEQUENCE = np.array([MARKER_VALUE] * MARKER_OCCURANCE, dtype=np.uint8)
COMPRESSED_FILE_EXTENSION = ".huff"

class HuffFile:
    def __init__(self):
        pass

    def _validate_file(self, filename):
        if not filename:
            raise ValueError("Error! File not declared properly.")
        if not os.path.exists(filename):
            raise ValueError("Error! File does not exist.")
        if not os.access(filename, os.R_OK):
            raise ValueError("Error! File is not readable.")
        if os.path.getsize(filename) == 0:
            raise ValueError("Error! File is empty.")

    def _is_text_file(self, filename):
        try:
            with open(filename, "r") as file:
                file.read(1024)
        except UnicodeDecodeError:
            return False
        return True

    def _find_marker_sequence(self, data, marker_sequence):
        marker_length = len(marker_sequence)
        return [i for i in range(len(data) - marker_length + 1)
                if np.array_equal(data[i:i + marker_length], marker_sequence)]

    def compress_file(self, filename):
        try:
            self._validate_file(filename)
            if not self._is_text_file(filename):
                raise ValueError("Error! File is not a plain text file.")
        except ValueError as e:
            raise CompressionError(str(e))

        with open(filename, "r") as file:
            input_data = file.read()

        ht = HuffmanTree()
        bit_string, serial_code = ht.compress(input_data)

        code_bit_array = np.array(list(map(int, bit_string)))
        pack_code_data = np.packbits(code_bit_array)

        bit_length = np.array([len(bit_string)], dtype=np.uint64)
        bit_len_bytes = np.frombuffer(bit_length.tobytes(), dtype=np.uint8)

        serial_code_bytes = serial_code.encode('utf-8')
        serial_data_bin = ''.join(format(byte, '08b') for byte in serial_code_bytes)
        serial_data_bit_array = np.array(list(map(int, serial_data_bin)))
        pack_serial_data = np.packbits(serial_data_bit_array)

        compressed_data = np.concatenate([
            pack_code_data, MARKER_SEQUENCE,
            bit_len_bytes, MARKER_SEQUENCE,
            pack_serial_data, MARKER_SEQUENCE
        ])

        curr_dir = os.path.dirname(filename)
        temp_dir = tempfile.TemporaryDirectory(dir=curr_dir)
        new_dir = os.path.basename(temp_dir.name)
        temp_dir.cleanup()
        new_dir = os.path.join(curr_dir, new_dir)
        os.mkdir(new_dir)

        compressed_path = os.path.join(new_dir, os.path.basename(filename) + COMPRESSED_FILE_EXTENSION)
        compressed_data.tofile(compressed_path)

        return new_dir

    def decompress_file(self, filename):
        try:
            self._validate_file(filename)
            original_filename, file_extension = os.path.splitext(filename)
            if file_extension != COMPRESSED_FILE_EXTENSION:
                raise ValueError("Error! File is not of type " + COMPRESSED_FILE_EXTENSION)
        except ValueError as e:
            raise CompressionError(str(e))

        read_data = np.fromfile(filename, dtype=np.uint8)
        marker_location = self._find_marker_sequence(read_data, MARKER_SEQUENCE)

        packed_data = read_data[:marker_location[0]]
        length_data = read_data[marker_location[0] + MARKER_OCCURANCE:marker_location[1]]
        serial_data = read_data[marker_location[1] + MARKER_OCCURANCE:marker_location[2]]

        unpacked_data = np.unpackbits(packed_data)
        original_length = np.frombuffer(length_data, dtype=np.uint64)[0]
        unpacked_data_str = ''.join(map(str, unpacked_data[:original_length]))

        unpacked_serial_data = np.unpackbits(serial_data)
        unpacked_serial_data_str = ''.join(map(str, unpacked_serial_data))
        unpacked_serial_data_chunks = [unpacked_serial_data_str[i:i+8] for i in range(0, len(unpacked_serial_data_str), 8)]
        unpacked_serial_data_bytes = bytes(int(chunk, 2) for chunk in unpacked_serial_data_chunks)
        serial_data_str = unpacked_serial_data_bytes.decode('utf-8')

        ht = HuffmanTree()
        decompressed_data = ht.decompress(unpacked_data_str, serial_data_str)

        output_path = original_filename
        with open(output_path, 'w') as f:
            f.write(decompressed_data)

        return output_path

class CompressionError(Exception):
    pass
