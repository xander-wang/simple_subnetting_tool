#
# A simple subnetting demo.
# For the curriculum design of computer network.
# 1st edition created by Xander Wang on 4th December, 2017.
# This is the 2nd edition created on 21st December, 2017, some functions deprecated.
# This demo includes:
#
# # validity check
# # Address type check
# # subnetting
#
# IPv4 only.
# Demo only.
#

from prettytable import PrettyTable

# receive ip string from user:
ip = raw_input('IP address: ')

# check its validity, output the type:

# var stores ip type, shown as corresponding mask(CIDR)
# except for type D,E
ip_type = 0

# first, convert in this form:
# 192.168.1.1 -> ['11000000', '10101000', '00000001', '00000001']
ip_decimal_list = ip.split('.')
ip_binary_list = []
for group in ip_decimal_list:
    ip_binary_group_with_zb = (bin(int(group)))
    ip_binary_group_without_zb = ip_binary_group_with_zb.replace('0b', '')
    if len(ip_binary_group_without_zb) <= 8:
        ip_binary_group_without_zb = ip_binary_group_without_zb.zfill(8)
        ip_binary_list.append(ip_binary_group_without_zb)
    else:
        print ('Invalid IP address.')
        exit()

# then, type checking, based on ip_binary_list:
for group in ip_binary_list:
    if group[0] == '0':
        ip_type = 8
        print ('Type A address.')
        break
    if group[0] == '1' and group[1] == '0':
        ip_type = 16
        print ('Type B address.')
        break
    if group[0] == '1' and group[1] == '1' and group[2] == '0':
        ip_type = 24
        print ('Type C address.')
        break
    if group[0] == '1' and group[1] == '1' and group[2] == '1' and group[3] == '0':
        ip_type = 40
        print ('Type D address.')
        exit()
    if group[0] == '1' and group[1] == '1' and group[2] == '1' and group[3] == '1':
        ip_type = 41
        print ('Type E address.')
        exit()
    else:
        print ('Wrong address.')
        exit()
    break

# receive mask string from user:
mask = raw_input('Subnet mask: ')

# check its validity:
# same as above:
mask_decimal_list = mask.split('.')
mask_binary_list = []
mask_binary_list_without_dot = ''
for group in mask_decimal_list:
    mask_binary_group_with_zb = (bin(int(group)))
    mask_binary_group_without_zb = mask_binary_group_with_zb.replace('0b', '')
    if len(mask_binary_group_without_zb) <= 8:
        mask_binary_group_without_zb = mask_binary_group_without_zb.zfill(8)
        mask_binary_list.append(mask_binary_group_without_zb)
    else:
        print ('Invalid mask.')
        exit()

# check whether group contains digit '01', yes for invalid scenario:
# first, mix the groups:
for group1 in mask_binary_list:
    mask_binary_list_without_dot = mask_binary_list_without_dot + group1

if ('01' in mask_binary_list_without_dot) is True:
    print ('Invalid mask.')
    exit()

# check ip-mask compatibility:
if ip_type == 8:
    if mask_binary_list[0] != '11111111':
        print ('Invalid mask.')
        exit()
if ip_type == 16:
    if mask_binary_list[0] != '11111111' or mask_binary_list[1] != '11111111':
        print ('Invalid mask.')
        exit()
if ip_type == 24:
    if mask_binary_list[0] != '11111111' or mask_binary_list[1] != '11111111' or mask_binary_list[2] != '11111111':
        print ('Invalid mask.')
        exit()

# show number of subnet:
# first, convert mask to CIDR format:

# var stores the CIDR suffix:
CIDR_suffix = 0

for digit in mask_binary_list_without_dot:
    if digit == '1':
        CIDR_suffix = CIDR_suffix + 1
num_of_subnet = 2 ** (CIDR_suffix - ip_type)
print ('Number of subnet: ' + str(num_of_subnet))

# show valid subnet information, shown like:
# No.   network address   num of host        host range                  broadcasting add
# 1       192.168.1.0        254        192.168.1.1-192.168.1.254          192.168.1.255

num_of_host = 2 ** (32 - CIDR_suffix) - 2
num_of_host_within_subnet = num_of_host / num_of_subnet

# get the network address:
ip_binary_list_without_dot = ''
network_binary_list_without_dot = ''
network_binary_list = []
checker = 0
temp_group = ''
# first, mix groups in ip_binary_list:
for group2 in ip_binary_list:
    ip_binary_list_without_dot = ip_binary_list_without_dot + group2

# get network address:
for digit1 in range(0, 32, 1):
    network_binary_list_without_dot = network_binary_list_without_dot + str(
        (int(ip_binary_list_without_dot[digit1]) and int(mask_binary_list_without_dot[digit1])))


# put digits back to groups for network_binary_list_without_dot:
for digit2 in network_binary_list_without_dot:
    temp_group = temp_group + digit2
    checker = checker + 1
    if checker % 8 == 0:
        network_binary_list.append(temp_group)
        temp_group = ''

# generate list stores subnet digits:
subnet_digits_list = []
for num in range(0, num_of_subnet, 1):
    subnet_digits_list.append(bin(num).replace('0b', '').zfill(CIDR_suffix - ip_type))

# generate all network addresses(mix subnet digits with network_binary_list_without_dot):
network_addresses = []

for num1 in range(0, num_of_subnet, 1):
    # create alias for further operations:
    alias = list(network_binary_list_without_dot)

    # first, delete subnet digits for variation:
    del alias[ip_type + 1:CIDR_suffix + 1]

    # and, insert the varied subnet digits:
    alias.insert(ip_type, subnet_digits_list[num1])

    # add items to network_addresses:
    network_addresses.append(''.join(alias))


# convert the network_binary_list to decimal:
checker1 = 0
loop_round = 0

# the list is a list-within-a-list:
network_decimal_list_sub_list_group = ''
network_decimal_list_sub_list = []
network_decimal_list = []

# loops to reformat(convert) the lists:
for rounds in range(0, num_of_subnet, 1):
    for rounds1 in range(1, 33, 1):
        network_decimal_list_sub_list_group = network_decimal_list_sub_list_group + network_addresses[rounds][
            rounds1 - 1]
        if rounds1 % 8 == 0:
            network_decimal_list_sub_list.append(str(int(network_decimal_list_sub_list_group, 2)))
            network_decimal_list_sub_list_group = ''
    network_decimal_list.append(network_decimal_list_sub_list)
    network_decimal_list_sub_list = []


# final output:
print "Subnetting Table:    "
output = PrettyTable(["No.", "Network Address", "Host", "IP Range", "Broadcast Address"])
output.align["No."] = '1'
output.padding_width = 3
for index in range(0, num_of_subnet, 1):
    output.add_row([index+1, '.'.join(network_decimal_list[index]), num_of_host, '.'.join(network_decimal_list[index]) + '-' + str(int(network_decimal_list[index][3])+num_of_host), '***.' + str(int(network_decimal_list[index][3])+num_of_host+1)])
print output

# Bye.
print "Bye."