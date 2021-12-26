class Pipeline:
    def __init__(self, tasks):
        self.entrypoint = Pipeline.__create_taskflow(tasks)

    @staticmethod
    def __create_taskflow(tasks):
        for i in range(len(tasks) - 1):
            tasks[i].set_next(tasks[i + 1])

        return tasks[0]

    def run(self, configs):
        self.entrypoint.run(configs)
