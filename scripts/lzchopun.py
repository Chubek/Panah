from os import open as sysc_open, read as sysc_read, write as sysc_write, close as sysc_close, fstat as sysc_fstat, O_CREAT, O_WRONLY, O_RDONLY, O_RDWR
from stat import S_IRUSR, S_IWUSR



if __name__ == "__main__":
	from sys import executable, argv
	execname = executable.split("/")[-1]
	scriptname = argv[0]
	argv = argv[1:]


	params = {
		"inflate": ["INFLATE"],

	}

	if "--help" in argv or "-h" in argv:
		
		print(f"Example: {execname} {scriptname} INFLATE -i myfile.bin --output daytaflatedfile.dfa -t triplets.dfd")
		exit(1)

	args = {	
		"inflate": None,

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

