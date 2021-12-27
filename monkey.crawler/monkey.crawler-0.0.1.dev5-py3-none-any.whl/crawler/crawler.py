# -*- coding: utf-8 -*-

import logging

from monkey.crawler.op_codes import OpCode, OpCounter, Plotter
from monkey.crawler.processor import Processor


class Crawler:

    def __init__(self, source_name: str, processor: Processor, offset: int = 0, max_retry: int = 0):
        self.logger = logging.getLogger(self.__class__.__name__.lower())
        self.source_name = source_name
        self.offset = offset
        self.processor = processor
        self.retry_record_list = []
        self.retry_count = 0
        self.max_retry = max_retry

    def crawl(self):
        self._crawl(self._get_records())

    def _crawl(self, records):
        """Crawl the entire data source"""
        allow_retry = self.retry_count <= self.max_retry
        retry_accumulator = InMemoryAccumulator()
        if self.retry_count == 0:
            self._echo_start()
        print(f'\n-- PASS #{self.retry_count + 1} ({self.source_name}) --', end='', flush=True)
        counter = OpCounter()
        plotter = Plotter()
        with self.processor as processor:
            for record in records:
                plotter.print_line_head(counter.total())
                op_code = processor.process(record, allow_retry)
                counter.inc(op_code)
                plotter.plot(op_code)
                if op_code == OpCode.RETRY:
                    retry_accumulator.add(record)
            print('\n-- END --')
        self._report(counter)
        if len(retry_accumulator) > 0 and allow_retry:
            self._crawl(retry_accumulator)

    def _get_records(self):
        """Returns an iterator on records"""
        # TODO: Check retry accumulator to get records from accumulator instead of original source
        raise NotImplementedError()

    def _report(self, counter: OpCounter):
        self.logger.info(f'Crawling report: \n{counter}')

    def _echo_start(self):
        raise NotImplementedError()


class Accumulator:

    def __init__(self):
        pass

    def __iter__(self):
        raise NotImplementedError()


class InMemoryAccumulator:

    def __init__(self):
        super().__init__()
        self._list = []

    def __iter__(self):
        return self._list.__iter__()

    def add(self, elt):
        self._list.append(elt)

    def __len__(self):
        return len(self._list)
