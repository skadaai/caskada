from brainyflow import Node, Flow, ParallelFlow

class MapReduceFlow(ParallelFlow):
    pass

class Trigger(Node):
    def __init__(self, options: dict = {}, **kwargs):
        super().__init__(**kwargs)
        self.input_key = options.get("input_key", "items")
        self.output_key = options.get("output_key", "output")

    async def prep(self, memory):
        assert hasattr(memory, self.input_key), f"'{self.input_key}' must be set in memory"
        return getattr(memory, self.input_key)
    
    async def post(self, memory, items, exec_res):
        setattr(memory, self.output_key, {} if isinstance(items, dict) else [None] * len(items))
        for index, input in (enumerate(items) if isinstance(items, (list, tuple)) else items.items()):
            self.trigger("default", {"index": index, "item": input})

class Reduce(Node):
    def __init__(self, options: dict = {}, **kwargs):
        super().__init__(**kwargs)
        self.output_key = options.get("output_key", "output")

    async def prep(self, memory):
        assert hasattr(memory, "index"), "index of processed item must be set in memory"
        assert hasattr(memory, "item"), "processed item must be set in memory"
        return memory.index, memory.item
    
    async def post(self, memory, prep_res, exec_res):
        memory[self.output_key][prep_res[0]] = prep_res[1]

def mapreduce(iterate: Node | Flow, options: dict = {}):
    trigger = Trigger(options)
    reduce = Reduce(options)

    trigger >> iterate >> reduce
    return MapReduceFlow(start=trigger)
