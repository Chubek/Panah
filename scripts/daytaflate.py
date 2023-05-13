from os import open as sysc_open, read as sysc_read, write as sysc_write, close as sysc_close, fstat as sysc_fstat, O_CREAT, O_WRONLY, O_RDONLY, O_RDWR
from stat import S_IRUSR, S_IWUSR

SEPARATOR = 16777216
SUM_BYTES = 32640
TRIPFILE_SIZE = 8290560
SYMTABLE_LEN = 2731136
BIOCOEFF_255K3 = 2731135

def error_out(message: str):
	print("\033[1;31mError occured\033[0m")
	print(message)
	exit(1)


def random_number(seed: int, m=256):
	return (((seed << 5) + seed) + 1) % m


def sysc_write_byte_three_combinations_to_disk(outfile="3combinations.dfd"):
	from itertools import combinations
	fd = sysc_open(outfile, O_CREAT | O_WRONLY, S_IWUSR | S_IRUSR)
	print(fd)
	for triplet in combinations(range(256), 3):	sysc_write(fd, bytearray(triplet))
	sysc_close(fd)



def sysc_read_byte_three_combinations_from_disk(infile="3combinations.dfd"):
	from os.path import exists
	if not exists(infile): sysc_write_byte_three_combinations_to_disk()
	fd = sysc_open(infile, O_RDONLY, S_IRUSR)
	combinations = sysc_read(fd, BIOCOEFF_255K3)
	sysc_close(fd)
	return combinations


def generate_shuffled_bytelist(seed: int) -> list[int]:
	bytelist = list(range(256))
	if not seed: return bytelist
	for i in reversed((1, 254)):
		j = random_number(seed, i)
		tmp = bytelist[j]
		bytelist[j] = bytelist[i]
		bytelist[i] = tmp
	return bytelist


def generate_triplet_dictionary(bytelist: list[int], outfile="triplets.dfd", combinations="3combinations.dfd") -> None:
	if len(bytelist) != 256: error_out("Length of byte list must be exactly 256")
	if sum(bytelist) != SUM_BYTES: error_out(f"Sum of byte list must exactly be {SUM_BYTES}")
	if not all([i in bytelist for i in range(256)]): error_out("The bytelist must include all 256 bytes (0-255)")
	combinations = sysc_read_byte_three_combinations_from_disk(combinations)
	fd = sysc_open(outfile, O_CREAT | O_WRONLY, S_IWUSR | S_IRUSR)		
	for i in combinations: sysc_write(fd, bytes(bytelist[i]))
	sysc_close(fd)


def load_triplet_file(tripfile="triplets.dfd") -> list[int]:
	from os import sysc_open, sysc_read, sysc_close
	fd = sysc_open(tripfile, O_RDONLY, S_IRUSR)
	sysc_readbytes = sysc_read(fd, TRIPFILE_SIZE)
	sysc_close(fd)
	return [int.from_bytes(bytearray([0, b1, b2, b3]), byteorder='little', signed=False) for b1, b2, b3 in zip(sysc_readbytes[::3], sysc_readbytes[1::3], sysc_readbytes[2::3])]



def sysc_read_input_and_update_stats(inputfile: str, triplets: list[int]) -> list[int]:
	fd = sysc_open(tripfile, 0)
	size = sysc_fstat(fd).st_size
	stats = [0] * SYMTABLE_LEN
	while size:
		b1, b2, b3 = sysc_read(fd, O_RDONLY, S_IRUSR)
		sysc_readtrip = int.from_bytes(bytearray([0, b1, b2, b3]), byteorder='little', signed=False)
		idx = triplets.index(sysc_readtrip)
		stats[idx] += 1
		size -= 1
	sysc_close(fd)
	stats[-1] = 1
	return stats


def scale_stats(stats: list[int]) -> list[int]:
	max_stat = 0
	for stat in stats:
		if stat > max_stat: max_stat = stat
	scale = max_stat // SYMTABLE_LEN
	scale += 1
	scaled_stats = [0] * (SYMTABLE_LEN + 1)
	for i, stat in enumerate(stats):
		scaled_stats[i] = stat // scale
		if not scaled_stats[i]:
			scaled_stats[i] = 1
	scaled_stats[-1] = scale
	return scaled_stats


def get_cumulative_stats(scaled_stats: list[int]) -> list[int]:
	cumulative_stats = [0] * SYMTABLE_LEN
	for i in range(SYMTABLE_LEN):
		cumulative_stats[i + 1] = cumulative_stats[i] + scaled_stats[i]
	cumulative_stats[-1] = SYMTABLE_LEN
	return cumulative_stats


def get_interval(symbol: int, totals: list[int], triplets: list[int]) -> tuple[int, int]:
	return totals[0]


if __name__ == "__main__":
	from sys import executable, argv
	execname = executable.split("/")[-1]
	scriptname = argv[0]
	argv = argv[1:]


	params = {
		"inflate": ["INFLATE"],
		"deflate": ["DEFLATE"],
		"combinegen": ["COMBINE-GEN"],
		"tripletgen": ["TRIPLET-GEN"],
		"seed": ["--seed", "-s"],
		"outfile": ["--outfile", "-o"],
		"infile": ["--infile", "-i"],
		"triplets": ["--triplets", "-t"],
		"3combine": ["--3combine", "-3"]
	}

	if "--help" in argv or "-h" in argv:
		print("\033[1;32mDaytaflate by Chubak Bidpaa\033[0m")
		print("\033[1;33mIf you are either compressing (inflating) or decompressing (deflating), you need a triplet database file (identical across compression/decompression)")
		print("(which you can generate, but keep it for decompression)")
		print("You may pass a seed of 0, that will not shuffle the bytearray, you will get lexicographical byteorder (0-255) for triplets")
		print("Before you attempt to generate a triplet, you first need to generate a 3-combinations file")
		print("A 3-combinations file will save all the 3-combinations of 0-255 to the specified file")
		print("You can pass a custom 3-combinations file as well, but it should just be the 3-combinations of 0-255 in lexographical order\033[0m")
		print("Note: if the combinations file does not exist, it will be created under default name\033[0m")
		print("\033[1m[Long Param/Short Param] | Purpose | Default Value")
		print("[INFLATE] | Set mode to inflate (compress) | OFF")
		print("[DEFLATE] | Set mode to deflate (decompress) | OFF")
		print("[COMBINE-GEN] | Set mode to 3-combine generate | OFF")
		print("[TRIPLET-GEN] | Set mode to triplet generate | ON")
		print("[--seed/-s] | Seed for triplet generation | 42498279")
		print("[--outfile/-o] | Output compressed/decompressed file | None")
		print("[--infile/-i] | Input compressed/decompressed file | daytaflated.dfa")
		print("[--triplets/-t] | Input/output triplets | triplets.dfd")
		print("[--3combine/-3] | Input/output 3-combinations | 3combinations.dfd")
		print(f"Example: {execname} {scriptname} INFLATE -i myfile.bin --output daytaflatedfile.dfa -t triplets.dfd")
		exit(1)

	args = {	
		"inflate": None,
		"deflate": None,
		"combinegen": None,
		"tripletgen": "TRIPLET-GEN",
		"outfile": None,
		"infile": "daytaflated.dfa",
		"triplets":	"triplets.dfd",
		"3combine": "3combinations.dfd",
		"seed": 42498279,	
	}

	all_params = sum(params.values(), [])
	skip = False
	for arg in argv:
		if skip:
			args[skip] = arg
			skip = False
			continue
		if arg in all_params:
			for k, v in params.items():
				if arg in v:
					skip = k
		else:
			error_out(f"Illegal parameter: {arg}")

	if args['tripletgen'] == "TRIPLET-GEN":
		bytelist = generate_shuffled_bytelist(int(args['seed']))
		generate_triplet_dictionary(bytelist, args['triplets'], args['3combine'])