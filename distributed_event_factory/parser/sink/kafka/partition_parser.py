from distributed_event_factory.parser.parser import Parser

class PartitionParser(Parser):

    def __init__(self):
        self.dependencies = dict()

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        return self.dependencies[config["type"]].parse(config)