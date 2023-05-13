from itertools import combinations

SEPARATOR = 16777216
SUM_BYTES = 32640

def error_out(message: str):
	print("\033[1;31mError occured\033[0m")
	print(message)
	exit(1)


def random_number(seed: int, m=256):
	return (((seed << 5) + seed) + 1) % m


def generate_shuffled_bytelist(seed: int) -> list[int]:
	bytelist = list(range(256))
	if not seed: return bytelist
	for i in reversed((1, 254)):
		j = random_number(seed, i)
		tmp = bytelist[j]
		byteelist[j] = bytelist[i]
		bytelist[i] = tmp
	return bytelist


def generate_triplet_dictionary(bytelist: list[int], outfile="triplets.dfd") -> None:
	if len(bytelist) != 256: error_out("Length of byte list must be exactly 256")
	if sum(bytelist) != SUM_BYTES: error_out(f"Sum of byte list must exactly be {SUM_BYTES}")
	if not all([i in bytelist for i in range(256)]): error_out("The bytelist must include all 256 bytes (0-255)")
	triplets = combinations(bytearray(bytelist), 3)
	separator = SEPARATOR.to_bytes(4, byteorder="little", signed=False)
	with open(outfile, "wb") as fbw:
		for triplet in triplets:
			fbw.write(triplet)
			fbw.write(separator)




if __name__ == "__main__":
	from sys import executable, argv
	execname = executable.split("/")[-1]
	scriptname = argv[0]
	argv = argv[1:]


	params = {
		"inflate": ["INFLATE"],
		"deflate": ["DEFLATE"],
		"generate": ["GENERATE"],
		"seed": ["--seed", "-s"],
		"outfile": ["--outfile", "-o"],
		"infile": ["--infile", "-i"],
		"triplets": ["--triplets", "-t"],
	}

	if "--help" in argv or "-h" in argv:
		print("\033[1;36mDaytaflate by Chubak Bidpaa\033[0m")
		print("\033[1m[Long Param/Short Param] | Purpose | Default Value\033[0m")
		print("\033[1;33mIf you are either compressing or decompressing, you need a triplet database file\033[0m")
		print("(which you can generate, but keep it for decompression)")
		print("You may pass a seed of 0, that will not shuffle the bytearray, you will get lexicographical byteorder (0-255) for triplets")
		print("[INFLATE] | Set mode to inflate (compress) | OFF")
		print("[DEFLATE] | Set mode to deflate (decompress) | OFF")
		print("[GENERATE] | Set mode to generate | ON")
		print("[--seed|-s] | Seed for triplet generation | 42498279")
		print("[--outfile/-o] | Output compressed/decompressed file | None")
		print("[--infile/-i] | Input compressed/decompressed file | daytaflated.dfa")
		print("[--triplets/-t] | Input/output triplets | triplets.dfd")
		print(f"Example: {execname} {scriptname} INFLATE -i myfile.bin --output daytaflatedfile.dfa -t triplets.dfd")
		exit(1)

	args = {	
		"inflate": None,
		"deflate": None,
		"generate": "GENERATE",
		"outfile": None,
		"infile": "daytaflated.dfa",
		"triplets":	"triplets.dfd",
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

	if any([a and b for a, b in combinations(list(args.values()[:3]), 2)]):
		error_out("You may only sed one of the following: INFLATE, DEFLATE, GENERATE")

	if args['generate'] == "GENERATE":
		bytelist = generate_shuffled_bytelist(int(args['seed']))
		generate_triplet_dictionary(bytelist, args['triplets'])