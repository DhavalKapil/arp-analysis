import json
import matplotlib.pyplot as plt

with open('log.json') as data_file:
	data = json.load(data_file)

# Plot a graph 
def saveGraph(x, y, filename):
	plt.plot(x, y, marker='o')
	plt.savefig(filename)
	plt.show()
	
# separating requests and replies
def separateRequestsAndReplies():
	requests = []
	replies = []
	for i, arpPacket in enumerate(data):
		if arpPacket["packet"]["arp_header"]["type"] == "request":
			requests.append(arpPacket)
		else:
			replies.append(arpPacket)
	return (requests, replies)

# Calculating time difference between a request and a reply
# Always equal to zero?
def findTimeDifferenceInRequestAndReply():
	diff = []
	k = 0
	for i in xrange(0, len(requests)):
		for j in xrange(k, len(replies)):
			request_arp_header = requests[i]["packet"]["arp_header"]
			reply_arp_header = replies[j]["packet"]["arp_header"]
			if request_arp_header["dest_ip"] == reply_arp_header["source_ip"] and request_arp_header["source_mac"] == reply_arp_header["dest_mac"]:
				# print reply_arp_header["source_ip"], reply_arp_header["source_mac"],request_arp_header["source_ip"], request_arp_header["source_mac"]
				# print replies[j]["timestamp"] - requests[i]["timestamp"]
				diff.append(requests[i], replies[j], replies[j]["timestamp"] - requests[i]["timestamp"])
				k = j + 1
				break
	return diff

# Number of packets received or sent in a minute
# params - packetList
def packetsPerMinute(packetList, filename):
	minutes = []
	packetCount = []
	minuteStart = data[0]["timestamp"]
	j = 0
	minute = 1
	for i in xrange(1, len(packetList)):
		if ((packetList[i]["timestamp"] - minuteStart)) >= 60:
			# print "Minute Number ", minute, (i-j)
			minutes.append(minute)
			packetCount.append(i-j)
			minute+=1
			j = i
			minuteStart = packetList[i]["timestamp"]

	saveGraph(minutes, packetCount, filename)
	#return (minutes, packetCount)

# Return list of IPs for which request is received, along with no. of requests
# Excluding RARP requests
# ipType can be source or destination
def countIpRequests(requests, ipType):
	listOfIPs = {}
	for i in xrange(0, len(requests)):
		arp_header = requests[i]["packet"]["arp_header"]
		if arp_header["source_ip"] != "0.0.0.0":
			if listOfIPs.has_key(arp_header[ipType]):
				listOfIPs[arp_header[ipType]]+=1
			else:
				listOfIPs[arp_header[ipType]] = 1
	return listOfIPs

# Number of requests per IP per Minute
def countIpRequestsPerMinute(listOfIPs, requests, ipType):
	listOfNumberOfRequestsPerMinute = []
	for ip in listOfIPs.keys():

		minutes = []
		packetCount = []
		minuteStart = requests[0]["timestamp"]
		k = 0
		for i in xrange(0, len(requests)):
			if ip == requests[i]["packet"]["arp_header"][ipType]:
				k = i
				break

		minute = 1
		for i in xrange(0, k):
			if (requests[i]["timestamp"] - minuteStart)>=60:
				minutes.append(minute)
				packetCount.append(0)
				minuteStart = requests[i]["timestamp"]
				minute+=1

		count = 0		
		for i in xrange(k, len(requests)):
			if ip == requests[i]["packet"]["arp_header"][ipType]:
					count+=1
			if (requests[i]["timestamp"] - minuteStart) >= 60:
				#print "Minute Number ", minute, (i-j)
				minutes.append(minute)
				packetCount.append(count)
				count = 0
				minute+=1
				minuteStart = requests[i]["timestamp"]

		listOfNumberOfRequestsPerMinute.append((ip, minutes, packetCount))

	return listOfNumberOfRequestsPerMinute

# Requests and Replies
(requests, replies) = separateRequestsAndReplies()

# Number of packets received or sent in a minute
packetsPerMinute(data, 'PacketsPerMinute.png')

# Number of requests received in a minute
packetsPerMinute(requests, 'RequestsPerMinute.png')


# Number of replies sent in a minute
packetsPerMinute(replies, 'RepliesPerMinute.png')

# Number of times MAC Address for each IP is requested 
# (ip, count)
listOfRequestedIPs = countIpRequests(requests, "dest_ip")

# Number of times the host with an IP makes requests for other IPs 
# (ip, count)
listOfRequestingIPs = countIpRequests(requests, "source_ip")

# Number of times MAC Address for each IP is requested per minute
# (ip, list of minutes, list of count of requests in each minute)
listOfNumberOfRequestsPerMinute = countIpRequestsPerMinute(listOfRequestedIPs, requests, "dest_ip")

# Number of times the host with an IP makes requests for other IPs per minute
# (ip, list of minutes, list of count of requests in each minute)
listOfNumberOfRequestsMadePerMinute  = countIpRequestsPerMinute(listOfRequestingIPs, requests, "source_ip")

