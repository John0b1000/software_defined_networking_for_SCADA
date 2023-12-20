# @file: request_test.py
#
# @brief: Uses northbound interface (REST API) to communicate with SEL-5056.
#

# imports
import json
import requests
import sys

class configurationNode:
    """ Class for storing node-related information. """

    def __init__(self, name, uid, ip_addr, ethernet_id, mac_addr):
        self.common_name       = name
        self.unique_identifier = uid
        self.ip_addr           = None
        self.ethernet_id       = None
        self.mac_addr          = None

    def __repr__(self):
        return f"Node: {self.common_name}; UID: {self.unique_identifier}; IP Address: {self.ip_addr}; Ethernet Address: {self.ethernet_id}; MAC Address: {self.mac_addr})"

    def __str__(self):
        return f"Node: {self.common_name}; UID: {self.unique_identifier}; IP Address: {self.ip_addr}; Ethernet Address: {self.ethernet_id}; MAC Address: {self.mac_addr})"
    
class logicalConnection:
    """ Class for storing logical-connection-related information. """

    def __init__(self, uid, cst, source, dst):
        self.unique_identifier = uid
        self.cst_type          = cst
        self.source_uid        = source
        self.dst_uid           = dst
        self.nodes             = None

    def __repr__(self):
        return f"Logical Connection: {self.unique_identifier}; CST: {self.cst_type}; Source Node: {self.nodes[self.source_uid].common_name}; Destination Node: {self.nodes[self.dst_uid].common_name}"

    def __str__(self):
        return f"Logical Connection: {self.unique_identifier:40s} CST: {self.cst_type:40s} Source Node: {self.nodes[self.source_uid].common_name:15s} Destination Node: {self.nodes[self.dst_uid].common_name:15s}"

def get_token(disp=False):
    """ Get a login token for Permission Level 3 User.

    @param disp (bool)    display Boolean
    
    @return token
    """

    # print a divider
    #
    print(f"\n{'Begin - Login Token Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/identity/connect/token"
    endpoint = api_url + uri

    # define HTTP message content
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"grant_type":"password", "username":"admin", "password":"Powerlab.1",\
            "acr_values":"role:PermissionLevel3", "client_secret":"Rest Interface",\
            "scope":"Rest", "client_id":"password-client", "state":0}
    
    # make HTTP request
    response = requests.post(endpoint, data=body, headers=headers, verify=False)

    # display response
    if disp:
        print(response)
        print(response.json())
    print(f"\n{'End - Login Token Request'.center(80, '=')}")

    # extract and return token
    token = response.json()
    token = token["access_token"]
    return token

def logout(token, disp=False):
    """ Revoke token and logout.

    @param token (str)     token to be revoked
    @param disp  (bool)    display Boolean
    
    @return token
    """

    # print a divider
    #
    print(f"\n{'Begin - Logout Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/identity/connect/revocation"
    endpoint = api_url + uri

    # define HTTP message content
    headers = {"Content-Type":"application/x-www-form-urlencoded"}
    body = {"token":{token}, "token_type_hint":"access_token", "client_id":"password-client", "client_secret":"Rest Interface"}
    
    # make HTTP request
    response = requests.post(endpoint, data=body, headers=headers, verify=False)

    # display response
    if disp:
        print(response)
    print(f"\n{'End - Logout Request'.center(80, '=')}")


def view_metadata(disp=False):
    """ View OData endpoints and properties via REST metadata.

    @param disp (bool)    display Boolean
    
    @return None
    """

    # print a divider
    #
    print(f"\n{'Begin - OData Endpoints Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/configuration/settings.json"
    endpoint = api_url + uri
    
    # make HTTP request
    response = requests.get(endpoint, verify=False)

    # display response
    if disp:
        print(response)
        print(response.json())
    print(f"\n{'End - OData Endpoints Request'.center(80, '=')}")

def read_logical_connections(disp=False):
    """ View all logical connections.

    @param disp (bool)    display Boolean     

    @return None
    """
    
    # print a divider
    #
    print(f"\n{'Begin - Logical Connections Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/api/default/config/logicalConnections"
    endpoint = api_url + uri

    # get Permission Level 3 Token
    token = get_token(disp=True)

    # define HTTP message content
    headers = {"Authorization":f"Bearer {token}"}
    
    # make HTTP request (authenticated)
    response = requests.get(endpoint, headers=headers, verify=False)

    # display response
    parsed_response = response.json()
    content = parsed_response['value']
    if disp:
        print(response)
        print(content)

    # parse all logical connections and store relevant information
    # in a list
    my_logical_connections = []
    for entry in content:

        # get the unique identifier for the entry
        id = entry['id']

        # get the CST type
        cst_type = entry['communicationServiceTypeId']

        # get the source and destination node identifiers
        source_uid = entry['sourceEndPoints'][0]
        dst_uid    = entry['destinationEndPoints'][0]

        # add a new logical connection to the list
        my_logical_connections.append(logicalConnection(id, cst_type, source_uid, dst_uid))

    # logout
    logout(token, disp=True)

    print(f"\n{'End - Logical Connections Request'.center(80, '=')}")

    # return logical connections
    return my_logical_connections

def read_configuration_nodes(disp):
    """ View all configuration nodes in the network.
       
    @param disp (bool)    display Boolean
    
    @return list of configuration nodes
    """
    
    # print a divider
    #
    print(f"\n{'Begin - Operational Nodes Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/api/default/config/nodes"
    endpoint = api_url + uri

    # get Permission Level 3 Token
    token = get_token(disp=True)

    # define HTTP message content
    headers = {"Authorization":f"Bearer {token}"}
    
    # make HTTP request (authenticated)
    response = requests.get(endpoint, headers=headers, verify=False)

    # display response
    parsed_response = response.json()
    content = parsed_response['value']
    if disp:
        print(response)
        print(content)

    # list of node objects
    my_nodes = []

    # parse all operational nodes and store relevant information
    # in a dictionary, indexed by human-readable name
    for entry in content:

        # get the unique identifier for the node
        id = entry['id']

        # get the display name
        display_name = entry['displayName']

        # get the attributes associated with this node
        #attributes = entry['attributes']

        # create vars for mac address, ethernet address, and ip address

        # extract relevant attributes
        '''
        for attribute in attributes:

            # ethernet-related information
            if attribute['@odata.type'] == '#Sel.Sel5056.TopologyManager.Attributes.Operational.EthernetAttr':
                mac_addr = attribute['macAddress']
                ethernet_id = attribute['id']
                
            # ip-related information
            elif attribute['@odata.type'] == '#Sel.Sel5056.TopologyManager.Attributes.Operational.Node.IpAttr':
                ip_addr = attribute['ipAddress']
        '''

        # add the node to the list
        my_nodes.append(configurationNode(display_name, id, None, None, None))

    # logout
    logout(token, disp=True)

    print(f"\n{'End - Operational Nodes Request'.center(80, '=')}")

    # return nodes
    return my_nodes

def delete_logical_connection(node, disp=False):
    """ Delete a logical connection between two configuration nodes.
       
    @param node (configurationNode) logical connection unique identifier
    @param disp (bool)              display Boolean
    
    @return None
    """

    # print a divider
    #
    print(f"\n{'Begin - Delete Logical Connections Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = f"/api/default/config/logicalConnections('{node.unique_identifier}')"
    endpoint = api_url + uri

    # get Permission Level 3 Token
    token = get_token(disp=True)

    # define HTTP message content
    headers = {"Authorization":f"Bearer {token}"}
    
    # make HTTP request (authenticated)
    response = requests.delete(endpoint, headers=headers, verify=False)

    # display response
    if disp:
        print(response)

    # logout
    logout(token, disp=True)

    print(f"\n{'End - Delete Logical Connections Request'.center(80, '=')}")

def create_logical_connection(cst_type, source_node, dst_node, disp=False):
    """ Create a logical connection between two configuration nodes.
       
    @param cst_type    (str)               communication service type
    @param source_node (configurationNode) source of logical connection
    @param dst_node    (configurationNode) dst of logical connection
    @param disp        (bool)              display Boolean
    
    @return None
    """

    # print a divider
    #
    print(f"\n{'Begin - Create Logical Connection Request'.center(80, '=')}")

    # define endpoint
    api_url = "https://localhost"
    uri = "/api/default/config/logicalConnections"
    endpoint = api_url + uri

    # get Permission Level 3 Token
    token = get_token(disp=True)

    # define HTTP message content
    src_list = [source_node.unique_identifier]
    dst_list = [dst_node.unique_identifier]
    headers = {"Content-Type":"application/json", "Authorization":f"Bearer {token}"}
    body = {"communicationServiceTypeId":"ICMP", "destinationEndPoints":[dst_node.unique_identifier], "sourceEndPoints":[source_node.unique_identifier]}
    
    # make HTTP request (need to convert body into json format - best practice: update elsewhere as well)
    response = requests.post(endpoint, data=json.dumps(body), headers=headers, verify=False)

    # display response
    if disp:
        print(response)
        print(response.json())

    # logout
    logout(token, disp=True)

    print(f"\n{'End - Create Logical Connection Request'.center(80, '=')}")

def main(argv):
    """ Main Program """

    if (len(argv) != 2):
        return -1

    # read in information about nodes and logical connections
    my_logical_connections = read_logical_connections(disp=True)
    my_nodes = read_configuration_nodes(disp=True)

    # make a sequence of requests
    if (argv[1] == 'v'):
        view_metadata(disp=True)
        nodes_dict = {}
        for node in my_nodes:
            nodes_dict[node.unique_identifier] = node
        for l in my_logical_connections:
            l.nodes = nodes_dict
        for l in my_logical_connections:
            print(l)

    # delete an ICMP logical connection: Nano_01 <-> Nano_00
    deleted = False
    if (argv[1] == 'd'):
        for l in my_logical_connections:
            if deleted: break
            if l.cst_type == "ICMP":
                for node in my_nodes:
                    if l.source_uid == node.unique_identifier and node.common_name == 'Nano_01':
                        delete_logical_connection(l, disp=True)
                        deleted = True
                        break
        
    # create an ICMP logical connection: Nano_01 <-> Nano_00
    if (argv[1] == 'c'):
        new_src_node = None
        new_dst_node = None
        for node in my_nodes:
            if node.common_name == "Nano_01":
                new_src_node = node
            elif node.common_name == "Nano_00":
                new_dst_node = node
        create_logical_connection("ICMP", new_src_node, new_dst_node, disp=True)

    # exit gracefully
    return 0

if __name__ == "__main__":
   main(sys.argv)
