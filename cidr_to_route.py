import sys,getopt
import socket
import struct

help = 'cidr_to_route.py -i <inputfile> -o <outputfile> -c <filter|cmroute|openvpn>'

def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return (network, netmask)

def cidr_filter(file):
	network_bin_list = []
	cidr=[]
	network_tmp_bin=[]
	for line in file:
		try:
			mask = line.split('/')[1]
			mask = int(mask)
			network = line.split('/')[0]

			network_bin = ""
			for j in range(0, 4):
				item = network.split('.')[j]
				item1 = int(item)
				item1 = bin(item1)
				item1 = str(item1)
				num2 = 10 - len(item1)
				for k in range(0, num2):
					network_bin = network_bin + '0'
				network_bin = network_bin + item1[2:]
			network_bin = network_bin[0:mask]
			tag = True
			if len(network_bin_list) == 0:
				network_bin_list.append(network_bin)
				cidr.append(line)
			else:
				network_tmp_bin=network_bin_list.copy()
				network_tmp=cidr.copy()
				for index in network_tmp_bin:
					if len(network_bin) >= len(index) and network_bin[0:len(index)] == index:
						tag = False
						break
					if len(network_bin) < len(index) and network_bin == index[0:len(network_bin)]:
						cidr_bin=network_tmp_bin.index(index)
						network_bin_list.remove(index)
						index1=network_tmp[cidr_bin]
						cidr.remove(index1)
				if tag:
					network_bin_list.append(network_bin)
					cidr.append(line)
		except Exception:
			pass
	return cidr
	
def main(argv):
	inputfile = ''
	outputfile = ''
	config = ""
	out_route = ""
	network = ""
	try:
		opts, args = getopt.getopt(argv,"hi:o:c:",["ifile=","ofile=","config="])
	except getopt.GetoptError:
		print (help)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print (help)
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		elif opt in ("-c", "--config"):
			config = arg
	if inputfile == "" or outputfile == "" or config == "":
		print (help)
		sys.exit(2)
	file = open(inputfile)
	cidr = cidr_filter(file)
	for line in cidr:
		try:
			network=cidr_to_netmask(line)
			if config == "openvpn" :
				out_route += "route %s %s vpn_gateway\n" % (network)
			elif config == "cmroute" :
				out_route += "add %s mask %s default METRIC default IF default\n" % (network)
			elif config == "filter" :
				out_route += line
		except Exception:
			pass
	fo = open(outputfile, "w+")
	fo.write(out_route)
	fo.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])
	
