import sys,getopt
import socket
import struct

help = 'cidr_to_route.py -i <inputfile> -o <outputfile> -c <cmroute|openvpn>'

def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return (network, netmask)
	
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
	for line in file:
		try:
			network=cidr_to_netmask(line)
			if config == "openvpn" :
				out_route += "route %s %s vpn_gateway\n" % (network)
			elif config == "cmroute" :
				cmroute += "add %s mask %s default METRIC default IF default\n" % (network)
		except Exception:
			pass
	fo = open(outputfile, "w+")
	fo.write(out_route)
	fo.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])
	
