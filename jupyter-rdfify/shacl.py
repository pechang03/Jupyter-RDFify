from pyshex.utils.schema_loader import SchemaLoader
from .rdf_module import RDFModule
from pyshacl import validate
import rdflib

class SHACLModule(RDFModule):
    def __init__(self, name, parser, logger, description, displayname):
        super().__init__(name, parser, logger, description, displayname)
        self.parser.add_argument(
            "action", choices=["parse", "validate", "prefix"], help="Action to perform")
        self.parser.add_argument(
            "--label", "-l", help="Shape label for referencing")
        self.parser.add_argument(
            "--graph", "-g", help="Graph label for validation")
        
        self.g_to_parse = rdflib.Graph()
        self.data_graph_format = "turtle"
        self.shacl_graph_format = "turtle"
        self.graph_fotmat = "ttl"
        self.graph_encoding = "utf-8"
        self.inference = "rdfs"
        self.debug = True
        self.serialize_report_graph = "turtle"
        self.prefix = ""

    def print_result(self, result):
        self.log(f"Evaluating shape '{result.start}' on node '{result.focus}'")
        if result.result:
            self.logger.print("PASSED!")
        else:
            self.logger.print(f"FAILED! Reason:\n{result.reason}\n")

    def handle(self, params, store):
        if params.action == "prefix":
            self.prefix = params.cell + "\n"
            self.log("Prefixes have been stored!")
            
        elif params.action == "parse":
            if params.cell is not None:
                try:
                    input_graph = params.graph
                    g_to_parse.parse(data=input_graph, format=self.graph_fotmat, encoding=self.graph_encoding)                    
                    self.log("Shape successfully parsed!")
                except Exception as e:
                    self.log(f"Error during shape parse:\n{str(e)}")
            else:
                self.log("No cell content to parse.")
        elif params.action == "validate":
            if params.label is not None and params.graph is not None:
                if params.label in store["shapes_graph"]:
                    if params.graph in store["data_graph"]:
                        result = self.evaluate(
                            store["rdfgraphs"][params.graph],
                            store["rdfshapes"][params.label],
                            data_graph_format,
                            shacl_graph_format, 
                            inference,
                            debug,
                            serialize_report_graph,
                        )
                        for r in result:
                            self.print_result(r)
                    else:
                        self.log(
                            f"Found no shapes graph with label '{params.graph}'.")
                else:
                    self.log(f"Found no shapes graph with label '{params.label}'.")
            else:
                self.log("A shapes graph and a data graph are required for the validation.")
