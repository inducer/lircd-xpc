#!/usr/bin/env python
# -*- coding: latin-1 -*-

from distutils.core import setup,Extension

setup(name="lircd-xpc",
      version="0.90",
      description="replacement lircd for XPC-RC01 remotes",
      author=u"Andreas Kloeckner",
      author_email="inform@tiker.net",
      license = "BSD-Style",
      url="http://news.tiker.net/software/lircd-xpc",
      scripts=["lircd-xpc"],
     )
