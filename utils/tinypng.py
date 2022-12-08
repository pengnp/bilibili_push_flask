import os
import tinify


# 压缩的核心
def compress_core(input_file, output_file):
	tinify.key = "dc4zqdhqXZsKMfcrXNzH0sCpvcDmVfkR"  # API KEY
	source = tinify.from_file(input_file)
	source.to_file(output_file)
	os.remove(input_file)


