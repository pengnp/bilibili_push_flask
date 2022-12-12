import tinify


# 压缩的核心
def compress_core(input_file, output_file):
	print(f"f{input_file}开始压缩")
	tinify.key = "dc4zqdhqXZsKMfcrXNzH0sCpvcDmVfkR"  # API KEY
	source = tinify.from_file(input_file)
	source.to_file(output_file)
	print(f"{input_file}压缩完成")


