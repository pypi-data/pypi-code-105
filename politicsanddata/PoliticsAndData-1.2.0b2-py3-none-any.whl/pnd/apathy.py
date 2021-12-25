"""
Contains :py:class:`Apathy`.

- Run & Combine everything
"""

import multiprocessing
import json
from .specific import Alliances, Cities, Nations, Trades, Wars
from.boredom import Boredom


class Apathy:
    """Made to make running and combining different categories easy."""

    def __init__(self, types=(Alliances, Cities, Nations, Trades, Wars), fs="filespace"):
        self.filespace = fs
        self.types = types
        self.create()

    def create(self):
        self.processes = []
        self.things = []
        for T in self.types:
            thing = T(fs=self.filespace)
            self.things.append(thing)
            self.processes.append(
                multiprocessing.Process(
                    target=thing.run,
                    daemon=True,
                    name=T.__name__)
            )

    def run(self):
        """..py:function:: run(self: :py:class:`Apathy`) -> None
        
        - Runs :py:meth:`Apathy.collect` and :py:meth:`Apathy.combine`:.


        """
        self.collect()
        self.combine()

    def collect(self):
        """..py:function:: collect(self: :py:class:`Apathy`) -> None
        
        - Runs all collection classes.

        """
        try:
            for process in self.processes:
                process.start()
            for process in self.processes:
                process.join()
        except KeyboardInterrupt:
            for process in self.processes:
                process.terminate()
            raise

    def combine(self):
        """..py:function:: combine(self: :py:class:`Apathy`) -> None
        
        - Combines all collected data into a single ``final.json``.


        """
        data = []

        for thing in self.things:
            with open(thing.file) as f:
                data.append(json.load(f)["timeline"])

        days = set(data[1].keys())
        for dat in data[1::]:
            keys = set(dat.keys())
            days = days and keys

        final = {}
        for day in sorted([float(d) for d in days]):
            val = []
            str_ver = Boredom.date_conv(None, day)
            try:
                for dat in data:
                    val += list(dat[str(day)].items())
                final[day] = dict(val)
            except KeyError:
                print(f"{str_ver} skipped due to missing data.")

        with open(f"{self.filespace}/final.json", "w") as f:
            json.dump(final, f)
