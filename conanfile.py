#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class PetscConan(ConanFile):
    name = "petsc"
    version = "3.8.3"
    url="http://github.com/bilke/conan-petsc"
    description = "PETSc is suite of data structures and routines for the scalable (parallel) solution of scientific applications modeled by partial differential equations."

    license="BSD"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    source_subfolder = "source"
    install_dir = "install"

    def source(self):
        zip_name = "petsc-lite-%s.tar.gz" % self.version
        tools.get("http://ftp.mcs.anl.gov/pub/petsc/release-snapshots/{0}".format(zip_name))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        tools.download("https://raw.githubusercontent.com/petsc/petsc/a3e07f7d98935102301a2849d6c5439db2167066/configure",
            "source/configure", overwrite=True)

    def system_requirements(self):
        pack_names = None
        if tools.os_info.linux_distro == "ubuntu":
            pack_names = [
                "libopenmpi-dev",
                "libblas-dev",
                "liblapack-dev",
                "openmpi-bin",
                "openssh-server"
            ]

        if pack_names:
            installer = tools.SystemPackageTool()
            installer.update()
            installer.install(" ".join(pack_names))

    def _build_linux(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        with tools.environment_append(env_build.vars):
            configure_args = ['--with-fc=0', '--download-f2cblaslapack=1', '--prefix=../%s' % self.install_dir]
            with tools.chdir(self.source_subfolder):
                env_build.configure(args=configure_args)
                env_build.make(args=["-j", "1", "all"])
                env_build.make(args=["install"])

    def _build_mingw(self):
        pass

    def _build_visual_studio(self):
        pass

    def build(self):
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            self._build_visual_studio()
        elif self.settings.os == "Windows" and self.settings.compiler == "gcc":
            self._build_mingw()
        elif self.settings.os == "Linux":
            self._build_linux()
        else:
            # macOS
            self._build_linux()

    def package(self):
        self.copy(pattern="LICENSE", src=self.source_subfolder)
        self.copy(pattern="*", src=self.install_dir)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
