import argparse
import io
import os

from charms.layer import basic
import charms.reactive
from charms.reactive.helpers import data_changed

from charmhelpers.core import hookenv
from charmtest import CharmTest


class HttpStub:

    port = None

    def configure(self, port=None):
        self.port = port


class Snap:

    name = "snap"

    def __init__(self):
        self.snaps = {}

    def __call__(self, proc_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("command")
        parser.add_argument("snap_name")
        args = parser.parse_args(proc_args["args"][1:])
        if args.command == "install":
            self.snaps[args.snap_name] = {}
        else:
            raise AssertionError("Command not implemented: " + args.command)
        return {}


class ResourceGet:

    name = "resource-get"

    def __call__(self, proc_args):
        return {"stdout": io.BytesIO(b"")}


class FooTest(CharmTest):

    def setUp(self):
        super().setUp()
        self.http = HttpStub()
        # self.charm_dir = os.getcwd()
        # os.environ["CHARM_DIR"] = self.charm_dir
        basic.init_config_states()
        hookenv.config()["snap_proxy"] = ""
        data_changed("snap.proxy", "")
        code_dir = os.getcwd()
        charm_dir = hookenv.charm_dir()
        tools_dir = "/var/lib/juju/tools/machine-0"
        os.makedirs(tools_dir)
        jujud_path = os.path.join(tools_dir, "jujud")
        with open(jujud_path, "w") as jujud:
            jujud.write("#!/bin/sh\necho 2.0.3\n")
        os.chmod(jujud_path, 0o755)

        for sub_path in ["reactive", "layer.yaml"]:
            source = os.path.join(code_dir, sub_path)
            target = os.path.join(charm_dir, sub_path)
            os.symlink(source, target)
        self.snap = Snap()
        self.fakes.processes.add(self.snap)
        self.resource_get = ResourceGet()
        self.fakes.processes.add(self.resource_get)

    def test_install_snap(self):
        os.environ["JUJU_HOOK_NAME"] = "install"
        charms.reactive.main()
        self.assertEqual(
            ["bjornt-prometheus-node-exporter"], list(self.snap.snaps.keys()))
