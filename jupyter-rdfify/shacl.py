from pyshex.utils.schema_loader import SchemaLoader
from .rdf_module import RDFModule
from pyshacl import validate

class SHACLModule(RDFModule):
    def __init__(self, name, parser, logger, description, displayname):
        super().__init__(name, parser, logger, description, displayname)
        self.parser.add_argument(
            "action", choices=["parse", "validate", "prefix"], help="Action to perform")
        self.parser.add_argument(
            "--label", "-l", help="Shape label for referencing")
        self.parser.add_argument(
            "--graph", "-g", help="Graph label for validation")
        
        self.loader = SchemaLoader()
        self.data_graph_format = "turtle"
        self.shacl_graph_format = "turtle"
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
            self.log("Stored Prefix.")
        elif params.action == "parse":
            if params.cell is not None:
                try:
                    schema = self.loader.loads(self.prefix + params.cell)
                    if params.label is not None and schema is not None:
                        store["shapes_graph"][params.label] = schema
                    self.log("Shape successfully parsed.")
                except Exception as e:
                    self.log(f"Error during shape parse:\n{str(e)}")
            else:
                self.log("No cell content to parse.")
        elif params.action == "validate":
            if params.label is not None and params.graph is not None:
                if params.label in store["shapes_graph"]:
                    if params.graph in store["data_graph"]:
                        result = self.evaluate(
                            store["data_graph"][params.graph],
                            store["shapes_graph"][params.label],
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
