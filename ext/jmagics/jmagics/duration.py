import ast
import time

from IPython import get_ipython
from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magics.execution import _format_time

import matplotlib.pyplot as plt


@magics_class
class DurationMagics(Magics):
    labels: list
    durations: list

    def __init__(self, shell):
        super().__init__(shell)
        self.reset_durations()

    @line_magic
    def reset_durations(self, _=None):
        self.labels = []
        self.durations = []

    def _split_cell(self, cell):
        code = None
        exp = None

        cell_tmp = self.shell.transform_cell(cell)
        cell_ast = self.shell.compile.ast_parse(cell_tmp)
        cell_body = self.shell.transform_ast(cell_ast).body

        if len(cell_body)>=1:
            if isinstance(cell_body[-1], ast.Expr):
                exp_val = ast.Expression(cell_body.pop().value)
                exp = self.shell.compile(exp_val, '<timelog>', 'eval')

            if len(cell_body)>=1:
                code_val = ast.Module(cell_body)
                code = self.shell.compile(code_val, '<timelog>', 'exec')

        return code, exp

    @cell_magic
    def duration(self, line, cell):
        self.labels.append(line.strip())
        self.durations.append(-1)

        code, exp = self._split_cell(cell)
        out = None

        try:
            wtime = time.time
            user_ns = self.shell.user_ns
            start_time = wtime()
            if code:
                exec(code, user_ns)
            if exp:
                out = eval(exp, user_ns)
            end_time = wtime()

            duration = end_time - start_time
            print("Duration: ", _format_time(duration))
            self.durations[-1] = duration
        except:
            self.shell.showtraceback()
            return

        return out

    @line_magic
    def plot_durations(self, mode:str):
        mode = mode.upper()

        labels = self.labels[::-1]
        durations = self.durations[::-1]

        plt.figure(figsize=(14, 6))

        if mode == "LOG":
            plt.xscale('log')
            plt.xlabel('Duration (Log)')
        else:
            plt.xlabel('Duration')

        plt.barh(labels, durations)

        for i, value in enumerate(durations):
            plt.text(value * 1.01, i, _format_time(value), va='center')

        plt.show()

    def get_duration(self, label):
        index = self.labels.index(label)
        return self.durations[index]


# Register the magic with IPython
ip = get_ipython()
duration_magics = DurationMagics(shell=ip)
ip.register_magics(duration_magics)
