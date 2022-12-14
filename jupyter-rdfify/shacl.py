from pyshex.utils.schema_loader import SchemaLoader
from .rdf_module import RDFModule
from .graph import draw_graph, parse_graph
import pyshacl
from .util import strip_comments

class SHACLModule(RDFModule):
    def __init__(self, name, parser, logger, description, displayname):
        super().__init__(name, parser, logger, description, displayname)
        self.parser.add_argument(
            "action", choices=["parse", "draw", "validate", "prefix"], help="Action to perform")
        self.parser.add_argument(
            "--label", "-l", help="Shape label for referencing")
        self.parser.add_argument(
            "--graph", "-g", help="Graph label for validation")
        
        self.prefix = ""

    def check_label(self, label, store):
        if label is not None:
            if label in store["rdfgraphs"]:
                return True
            else:
                self.log(f"Graph labelled '{label}' not found.")
        else:
            self.log("Please specify the label of a graph with parameter --label or -l.")
            
    def print_validation_result(self, conforms):
        self.log(f"Evaluating the shape!")
        if conforms==True:
            self.logger.print("The data graph conforms the shapes graph!")
        else:
            self.logger.print(f"Conformance FAILED!")
    
    def print_parse_result(self, success):
        self.log(f"Parsing the graph!")
        if success==True:
            self.logger.print("Graph successfully parsed!")
        else:
            self.logger.print(f"Parse FAILED! Reason!")
            
    def handle(self, params, store):
        if params.action is not None:
            if params.action == "prefix":
                self.prefix = params.cell + "\n"
                self.log("Prefixes stored!")            

            elif params.action == "parse":
                success = False
                try:
                    self.prefix = params.cell + "\n"
                    code = strip_comments(params.cell)
                    parse_graph(self.prefix + code, self.logger)    
                    success = True 
                    self.print_parse_result(success)
                except Exception as e:
                    self.log(f"Parse failed:\n{str(e)}")                    
                    return 
            elif params.action == "draw":
                if self.check_label(params.label, store):
                    draw_graph(store["rdfgraphs"][params.label], self.logger)
                    
            elif params.action == "validate":
                if params.label is not None and params.graph is not None:
                    if params.label in store["rdfgraphs"]:
                        if params.graph in store["rdfgraphs"]:
                            try:
                                results = pyshacl.validate(
                                    data_graph = store["rdfgraphs"][params.graph],
                                    shacl_graph = store["rdfgraphs"][params.label],
                                    data_graph_format = "turtle",
                                    shacl_graph_format = "turtle", 
                                    inference = "both",
                                    debug = True,
                                    serialize_report_graph = "turtle",
                                )
                                conforms, report_graph, report_text = results
                                self.print_validation_result(conforms) 
                                            
                            except Exception as e:
                                print("Opps!", str(e), flush=True)
                        else:
                            self.log(f"Found no data graph! '{params.graph}'.")
                    else:
                        self.log(f"Found no shapes graph! '{params.label}'.")
                else:
                    self.log("A shapes graph and a data graph are required for the validation!")
