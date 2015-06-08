import binascii

#returns -1 if str1 is less, 1 if str1 is greater, and 0 if equal
def string_cmp(str1, str2):
	pos = 0
	while (pos < len(str1) and pos < len(str2)):
		cmp = character_cmp(str1[pos], str2[pos])
		if (cmp != 0):
			return cmp
		pos = pos + 1
	#the shorter string comes first as it is a substring of the second
	if (len(str1) < len(str2)):
		return -1
	elif (len(str1) > len(str2)):
		return 1
	else:
		return 0

def character_cmp(chr1, chr2):
	values = {
		'0': 0,
		'1': 1,
		'2': 2,
		'3': 3,
		'4': 4,
		'5': 5,
		'6': 6,
		'7': 7,
		'8': 8,
		'9': 9,
		'a': 10,
		'b': 11,
		'c': 12,
		'd': 13,
		'e': 14,
		'f': 15}
	if (values[chr1] < values[chr2]):
		return -1
	elif (values[chr1] > values[chr2]):
		return 1
	else:
		return 0

#returns -1 if barr1 is less, 1 if barr1 is greater, and 0 if equal
def bytearr_cmp(barr1, barr2):
	pos = 0
	while (pos < len(barr1) and pos < len(barr2)):
		if (barr1[pos] < barr2[pos]):
			return -1;
		elif (barr1[pos] > barr2[pos]):
			return 1;
		pos = pos + 1
	#the shorter array will be ordered first
	if (len(barr1) < len(barr2)):
		return -1
	elif (len(barr1) > len(barr2)):
		return 1
	else:
		return 0

#tuples: (prev_tx_hash, prev_tx_output_index)
def input_cmp(input_tuple1, input_tuple2):
	#test prev_tx_hash first
	prev_tx_hash_cmp = string_cmp(input_tuple1[0], input_tuple2[0])
	if (prev_tx_hash_cmp != 0):
		return prev_tx_hash_cmp
	#tie-breaker: prev_tx_output_index
	if (input_tuple1[1] < input_tuple2[1]):
		return -1
	elif (input_tuple1[1] > input_tuple2[1]):
		return 1
	else:
		raise ValueError('Matching previous transaction hash and previous transaction output index for two disinct inputs. Invalid!')


def sort_inputs(input_tuples):
	return sorted(input_tuples, cmp=input_cmp)

def print_inputs(ordered_input_tuples):
	index = 0
	for prev_tx_hash, prev_tx_output_index in ordered_input_tuples:
		print("%d: %s[%d]" % (index, prev_tx_hash, prev_tx_output_index))
		index = index + 1

#tuples: # (amount, locking_script_byte_arr_little_endian)
def output_cmp(output_tuple1, output_tuple2):
	#test amount first
	if (output_tuple1[0] < output_tuple2[0]):
		return -1
	elif (output_tuple1[0] > output_tuple2[0]):
		return 1
	#tie-breaker: locking_script_byte_arr_little_endian
	return bytearray_cmp(output_tuple1[1], output_tuple2[1])

def sort_outputs(output_tuples):
	return sorted(output_tuples, cmp=output_cmp)

def print_outputs(ordered_output_tuples):
	index = 0
	for amount, locking_script_byte_array_litte_endian in ordered_output_tuples:
		locking_script_hex = binascii.hexlify(bytearray(locking_script_byte_array_litte_endian))
		print("%d:\t%d\t%s" % (index, amount, locking_script_hex))
		index = index + 1

def main():
	#reference data: https://blockchain.info/rawtx/0a6a357e2f7796444e02638749d9611c008b253fb55f5dc88b739b230ed0c4c3
	tx_0a6a_input_tuples = [
		# (prev_tx_hash, prev_tx_output_index)
		("643e5f4e66373a57251fb173151e838ccd27d279aca882997e005016bb53d5aa", 0),
		("28e0fdd185542f2c6ea19030b0796051e7772b6026dd5ddccd7a2f93b73e6fc2", 0),
		("f0a130a84912d03c1d284974f563c5949ac13f8342b8112edff52971599e6a45", 0),
		("0e53ec5dfb2cb8a71fec32dc9a634a35b7e24799295ddd5278217822e0b31f57", 0),
		("381de9b9ae1a94d9c17f6a08ef9d341a5ce29e2e60c36a52d333ff6203e58d5d", 1),
		("f320832a9d2e2452af63154bc687493484a0e7745ebd3aaf9ca19eb80834ad60", 0),
		("de0411a1e97484a2804ff1dbde260ac19de841bebad1880c782941aca883b4e9", 1),
		("3b8b2f8efceb60ba78ca8bba206a137f14cb5ea4035e761ee204302d46b98de2", 0),
		("54ffff182965ed0957dba1239c27164ace5a73c9b62a660c74b7b7f15ff61e7a", 1),
		("bafd65e3c7f3f9fdfdc1ddb026131b278c3be1af90a4a6ffa78c4658f9ec0c85", 0),
		("a5e899dddb28776ea9ddac0a502316d53a4a3fca607c72f66c470e0412e34086", 0),
		("7a1de137cbafb5c70405455c49c5104ca3057a1f1243e6563bb9245c9c88c191", 0),
		("26aa6e6d8b9e49bb0630aac301db6757c02e3619feb4ee0eea81eb1672947024", 1),
		("402b2c02411720bf409eff60d05adad684f135838962823f3614cc657dd7bc0a", 1),
		("7d037ceb2ee0dc03e82f17be7935d238b35d1deabf953a892a4507bfbeeb3ba4", 1),
		("6c1d56f31b2de4bfc6aaea28396b333102b1f600da9c6d6149e96ca43f1102b1", 1),
		("b4112b8f900a7ca0c8b0e7c4dfad35c6be5f6be46b3458974988e1cdb2fa61b8", 0)]
	tx_0a6a_sorted_input_tuples = sort_inputs(tx_0a6a_input_tuples)
	print_inputs(tx_0a6a_sorted_input_tuples)

	tx_0a6a_output_tuples = [
		# (amount, locking_script_byte_arr_little_endian)
		(400057456, [0x76, 0xa9, 0x14, 0x4a, 0x5f, 0xba, 0x23, 0x72, 0x13, 0xa0, 0x62, 0xf6, 0xf5, 0x79, 0x78, 0xf7, 0x96, 0x39, 0x0b, 0xdc, 0xf8, 0xd0, 0x15, 0x88, 0xac]),
		(40000000000, [0x76, 0xa9, 0x14, 0x5b, 0xe3, 0x26, 0x12, 0x93, 0x0b, 0x83, 0x23, 0xad, 0xd2, 0x21, 0x2a, 0x4e, 0xc0, 0x3c, 0x15, 0x62, 0x08, 0x4f, 0x84, 0x88, 0xac])]
	tx_0a6a_sorted_output_tuples = sort_outputs(tx_0a6a_output_tuples)
	print_outputs(tx_0a6a_sorted_output_tuples)

	#reference data: https://blockchain.info/rawtx/28204cad1d7fc1d199e8ef4fa22f182de6258a3eaafe1bbe56ebdcacd3069a5f thanks @quantabytes!
	tx_2820_input_tuples = [
		# (prev_tx_hash, prev_tx_output_index)
		("35288d269cee1941eaebb2ea85e32b42cdb2b04284a56d8b14dcc3f5c65d6055", 0),
		("35288d269cee1941eaebb2ea85e32b42cdb2b04284a56d8b14dcc3f5c65d6055", 1)] #duplicate prev_tx_hash

	tx_2820_sorted_input_tuples = sort_inputs(tx_2820_input_tuples)
	print_inputs(tx_2820_sorted_input_tuples)

	tx_2820_output_tuples = [
		# (amount, locking_script_byte_arr_little_endian)
		(100000000, [0x41, 0x04, 0x6a, 0x07, 0x65, 0xb5, 0x86, 0x56, 0x41, 0xce, 0x08, 0xdd, 0x39, 0x69, 0x0a, 0xad, 0xe2, 0x6d, 0xfb, 0xf5, 0x51, 0x14, 0x30, 0xca, 0x42, 0x8a, 0x30, 0x89, 0x26, 0x13, 0x61, 0xce, 0xf1, 0x70, 0xe3, 0x92, 0x9a, 0x68, 0xae, 0xe3, 0xd8, 0xd4, 0x84, 0x8b, 0x0c, 0x51, 0x11, 0xb0, 0xa3, 0x7b, 0x82, 0xb8, 0x6a, 0xd5, 0x59, 0xfd, 0x2a, 0x74, 0x5b, 0x44, 0xd8, 0xe8, 0xd9, 0xdf, 0xdc, 0x0c, 0xac]),
		(2400000000, [0x41, 0x04, 0x4a, 0x65, 0x6f, 0x06, 0x58, 0x71, 0xa3, 0x53, 0xf2, 0x16, 0xca, 0x26, 0xce, 0xf8, 0xdd, 0xe2, 0xf0, 0x3e, 0x8c, 0x16, 0x20, 0x2d, 0x2e, 0x8a, 0xd7, 0x69, 0xf0, 0x20, 0x32, 0xcb, 0x86, 0xa5, 0xeb, 0x5e, 0x56, 0x84, 0x2e, 0x92, 0xe1, 0x91, 0x41, 0xd6, 0x0a, 0x01, 0x92, 0x8f, 0x8d, 0xd2, 0xc8, 0x75, 0xa3, 0x90, 0xf6, 0x7c, 0x1f, 0x6c, 0x94, 0xcf, 0xc6, 0x17, 0xc0, 0xea, 0x45, 0xaf, 0xac])]
	tx_2820_sorted_output_tuples = sort_outputs(tx_2820_output_tuples)
	print_outputs(tx_2820_output_tuples)

if __name__ == "__main__":
    main()