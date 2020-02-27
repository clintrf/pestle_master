"""Entry point for launching the Pestle on-device software.

If launching on device, simple run `python3 launch_pestle.py`. If running
on a machine without the appropriate hardware, run in simulation mode:
`python3 launch_pestle.py --simulate`.
"""
from absl import app
from absl import flags
from absl import logging


FLAGS = flags.FLAGS

flags.DEFINE_bool(
    "simulate",
    False,
    "If set to true, this will simulate the Pestle hardware.",
)


def main(argv):
    del argv  # unused

    logging.info("Starting Pestle")


if __name__ == "__main__":
    app.run(main)
