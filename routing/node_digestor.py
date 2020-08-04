import uart 
import map_processor
import time
from ast import literal_eval as make_tuple

class Node_digestor:

	def get_path_node(start_row, start_column, dest_room):
		# start_row = 1
		# start_column = 2
		list_of_nodes = []
		list_of_nodes = map_processor.get_directions(start_row, start_column, dest_room)
		if list_of_nodes == -1:
			print("Invalid path request.")
			return -1

		with uart.Uart(115200) as Communicator:
			for i in list_of_nodes:
				tuple_node = (make_tuple(str(i)))
				Communicator.send(str(tuple_node[0]))
				time.sleep(0.1)
				Communicator.send(str(tuple_node[1]))
				time.sleep(0.1)
				Communicator.send("x")
				time.sleep(0.1)

				# wait for the Nano to respond with one byte character confirming that the node was processed
				Communicator.read()

if __name__ == "__main__":
	# DEBUG MODE
	print("Sending path for Room 223 from location (0,0)")
	Node_digestor.get_path_node(0, 0, "223")