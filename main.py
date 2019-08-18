#! /usr/bin/env python3

import os, sys

from smd.smd_app import SmdApp

if __name__ == "__main__":
    app = SmdApp()
    sys.exit(app.main())
