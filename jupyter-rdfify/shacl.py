from pyshex.utils.schema_loader import SchemaLoader
from .rdf_module import RDFModule
from .graph import draw_graph, parse_graph
from pyshacl import validate
from util import strip_comments

class SHACLModule(RDFModule):
    def __init__(self, name, parser, logger, description, displayname):
        super().__init__(name, parser, logger, description, displayname)
        self.parser.add_argument(
            "action", choices=["parse", "draw", "validate", "prefix"], help="Action to perform")
        self.parser.add_argument(
            "--label", "-l", help="Shape label for referencing")
        self.parser.add_argument(
            "--graph", "-g", help="Graph label for validation")
        
        self.data_graph_format = "turtle"
        self.shacl_graph_format = "turtle"
        self.graph_fotmat = "ttl"
        self.graph_encoding = "utf-8"
        self.inference = "rdfs"
        self.debug = True
        self.serialize_report_graph = "turtle"
        self.prefix = ""

    def check_label(self, label, store):
        if label is not None:
            if label in store["rdfgraphs"]:
                return True
            else:
                self.log(f"Graph labelled '{label}' not found.")
        else:
            self.log("Please specify the label of a graph with parameter --label or -l.")
            
    def print_result(self, result):
        self.log(f"Evaluating the shape!")
        if result.result:
            self.logger.print("Test PASSED!")
        else:
            self.logger.print(f"Test FAILED! Reason:\n{result.reason}\n")
            
    def handle(self, params, store):
        if params.action is not None:
            if params.action == "prefix":
                self.prefix = params.cell + "\n"
                self.log("Prefixes have been stored!")            

            elif params.action == "parse":
                try:
                    self.prefix = params.cell + "\n"
                    code = strip_comments(params.cell)
                    parse_graph(self.prefix + code, self.logger, self.name)                    
                except Exception as e:
                    self.log(f"Parse failed:\n{str(e)}")                    
                    return
                    
            elif params.action == "draw":
                if self.check_label(params.label, store):
                    draw_graph(store["rdfgraphs"][params.label], self.logger)
                    
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
                            self.log(f"Found no data graph! '{params.graph}'.")
                    else:
                        self.log(f"Found no shapes graph! '{params.shape}'.")
                else:
                    self.log("A shapes graph and a data graph are required for the validation!")
