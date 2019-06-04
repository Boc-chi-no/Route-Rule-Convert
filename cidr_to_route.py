import sys,getopt
import socket
import struct

def cidr_to_netmask(cidr):
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return (network, netmask)
	
def main(argv):
	inputfile = ''
	outputfile = ''
	cmroute = ""
	network = ""
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print ('cidr_to_route.py -i <inputfile> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('cidr_to_route.py -i <inputfile> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	file = open(inputfile)
	for line in file:
		try:
			network=cidr_to_netmask(line)
			cmroute += "add %s mask %s default METRIC default IF default\n" % (network)
		except Exception:
			pass
	fo = open(outputfile, "w+")
	fo.write(cmroute)
	fo.close()
	
if __name__ == "__main__":
	main(sys.argv[1:])
	
