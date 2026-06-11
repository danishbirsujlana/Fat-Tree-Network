"""
 Copyright (c) 2025 Computer Networks Group @ UPB

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

# Class for an edge in the graph
class Edge:
	def __init__(self):
		self.lnode = None
		self.rnode = None
	
	def remove(self):
		self.lnode.edges.remove(self)
		self.rnode.edges.remove(self)
		self.lnode = None
		self.rnode = None

# Class for a node in the graph
class Node:
	def __init__(self, id, type):
		self.edges = []
		self.id = id # identifeid by ip
		self.type = type # identifeid by node name

	# Add an edge connected to another node
	def add_edge(self, node):
		edge = Edge()
		edge.lnode = self
		edge.rnode = node
		self.edges.append(edge)
		node.edges.append(edge)
		return edge

	# Remove an edge from the node
	def remove_edge(self, edge):
		self.edges.remove(edge)

	# Decide if another node is a neighbor
	def is_neighbor(self, node):
		for edge in self.edges:
			if edge.lnode == node or edge.rnode == node:
				return True
		return False


class Fattree:

	def __init__(self, num_ports):
		self.servers = []
		self.switches = []
		self.generate(num_ports)

	def generate(self, num_ports):

		# TODO: code for generating the fat-tree topology;
		k = num_ports;
		pods = k;
		pod_switches_per_layer = k // 2;
		hosts_per_edge_switch = k // 2;
		core_switch_group_size = k // 2;

		core_switches = [];
		agregation_switches = [];
		edge_switches = [];

		# Creating core switches
		core_switch_index = 0;
		for i in range(1, (core_switch_group_size + 1)):
			for j in range(1, (core_switch_group_size + 1)):
				node = Node(f"10.{k}.{i}.{j}", f"c_{core_switch_index}");
				core_switches.append(node);
				self.switches.append(node);
				core_switch_index += 1;
		
		# Creating Pods
		host_index = 0;
		for p in range(pods):
			pod_aggs = []; # Aggregation Switches for pod p
			pod_edges = []; # Edge (TOR) Switches for pod p

			# Edge switches for pod p
			for edge in range(pod_switches_per_layer):
				edge_node = Node(f"10.{p}.{edge}.1", f"e_{p}_{edge}");
				pod_edges.append(edge_node);
				edge_switches.append(edge_node);
				self.switches.append(edge_node);

			# Aggregation switches for pod p
			for agg in range(pod_switches_per_layer):
				aggregation_node = Node(f"10.{p}.{pod_switches_per_layer + agg}.1", f"a_{p}_{agg}");
				pod_aggs.append(aggregation_node);
				agregation_switches.append(aggregation_node);
				self.switches.append(aggregation_node);

			# Connect Host servers to Edge Nodes in pod p
			for edge in range(pod_switches_per_layer):
				for h in range(hosts_per_edge_switch):
					host = Node(f"10.{p}.{edge}.{h + 2}", f"h_{host_index}");
					self.servers.append(host);
					host.add_edge(pod_edges[edge]);
					host_index += 1;

			for agg_nodes in pod_aggs:
				for edge_node in pod_edges:
					agg_nodes.add_edge(edge_node);

		for p in range(pods): # for each pod p
			for agg in range(pod_switches_per_layer): # for each agg switch in p
				aggregation_node_id = f"10.{p}.{pod_switches_per_layer + agg}.1";
				aggregation_node = next((agg for agg in agregation_switches if agg.id == aggregation_node_id), None) # Finding aggregation switch by id
				for c in range(core_switch_group_size):
					core_index = agg * core_switch_group_size + c; # Calculating core switch from it's index
					aggregation_node.add_edge(core_switches[core_index]);

# net_topo = Fattree(4)
# for switch in net_topo.switches:
# 	print(switch.id, switch.type)
# print("--------------------------------")
# for server in net_topo.servers:
# 	print(server.id, server.type)