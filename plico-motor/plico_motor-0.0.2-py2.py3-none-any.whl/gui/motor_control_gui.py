import sys

import plico_motor
from guietta import Gui, _


class Runner(object):

    def __init__(self):
        pass

    def _setUp(self, argv):

        host, port = argv
        self._motor = plico_motor.motor(host, int(port))
        print(dir(self._motor))

        def moveby(gui):
            nsteps = int(gui.nstepsby)
            self._motor.move_by(nsteps)

        def moveto(gui):
            nsteps = int(gui.nstepsto)
            self._motor.move_to(nsteps)

        def getstatus(gui):
            try:
                gui.pos = self._motor.position()
                gui.status = self._motor.status().as_dict()
            except Exception as e:
                gui.pos = str(e)

        self.gui = Gui(
             [  'Pos:'     , 'pos'       , _       ],
             [ ['Move to'] , '__nstepsto__', 'steps' ],
             [ ['Move by'] , '__nstepsby__', 'steps' ],
             [ 'Status:'   , 'status'    , _       ]
        )
        self.gui.Moveby = moveby
        self.gui.Moveto = moveto
        self.gui.timer_start(getstatus, 0.1)

    def run(self, argv):
        self._setUp(argv)
        self.gui.run()

    def terminate(self, signal, frame):
        pass


if __name__ == '__main__':
    runner = Runner()
    sys.exit(runner.run(sys.argv[1:]))

